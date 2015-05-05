#!/usr/bin/env python
# -*- coding: utf-8 -*-
# START LICENCE ##############################################################
#
# orphHCA - protein domain detection of unusual properties
# Copyright (c) 2015  Tristan Bitard-Feildel
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# END LICENCE ##############################################################
""" orphHCA is a python program to detect putative orphan domain in a MSA.
The program compare the putative domain with known domain models provided
by the user.
If not overlapping or similarity are constated, the MSA segment is reported
as an orphan domain.
Alternatively, orphHCA can be used to produce domain model based on HCA 
segments without comparison against known models
"""

from __future__ import print_function, division
import sys, os, shlex, argparse, glob, tempfile
import subprocess, multiprocessing
import multiprocessing.pool

from orphhca_sequence import msa2flat
from orphhca_annotation import make_hca, make_domains, filter_domains
from orphhca_io import write_msa_domains, create_database, read_multifasta
from orphhca_io import clean_path
from orphhca_util import check_program_config
from orphhca_hmm import dom_enrichment


__author__  = "Tristan Bitard-Feildel"
__email__   = "tristan.bitard.feildel@uni-muenster.de"
__year__    = 2015
__licence__ = "MIT"
__version__ = 0.1

__all__ = ["galohiHCA_main", "process_parameters"]

    

def process_one_msa(path, workdir, output,  params, hmmdb=[], verbose=False):
    """ process one MSA for annotation
    
    Parameters
    ----------
    
    path: string
        input path of the MSA file
        
    params: object
        argparse parameters object
        
    Return
    ------
    
    path_hmm: list
        the list of hmm path
    """
    
    # get attribures
    
    cores = params.cores if hasattr(params, "cores") else 1
    hca_size = params.hca_size if hasattr(params, "hca_size") else 30
    if hasattr(params, "nbover_hmm"):
        cut_hmm = True
        nbover_hmm = params.nbover_hmm
    elif hasattr(params, "cut_hmm"):
        cut_hmm = params.cut_hmm 
        nbover_hmm = True
    else:
        cut_hmm = 0
        nbover_hmm = True
    
    if hasattr(params, "nbover_dom"):
        cut_dom = True
        nbover_dom = params.nbover_dom
    elif hasattr(params, "cut_dom"):
        cut_dom = params.cut_dom
        nbover_dom = True
    else:
        cut_dom = 0.8
        nbover_dom = True
    
    if hasattr(params, "nbover_hca"):
        nbover_hca = params.nbover_hca
        cut_hca = True
    elif hasattr(params, "cut_hca"):
        cut_hca = params.cut_hca
        nbover_hca = True
    else:
        cut_hca = 0.2
        nbover_hca = True
    
    keepfasta = params.keepfasta if hasattr(params, "keepfasta") else False
    name = params.name
    seqdb = params.seqdb
    
    # extract protein sequence from MSA
    dfasta = read_multifasta(path)
    if dfasta == {}:
        print ("Error: MSA file {} is empty".format(path), file=sys.stderr)
        return []
        
    dfasta_flat = msa2flat(dfasta)
    
    # create Seg-HCA annotation
    if verbose:
        print("HCA sannotation")
    seghca_domains = make_hca(dfasta_flat, workdir, cores)
    
    hmm_domains = {}
    # with annotation or wihtout
    if hmmdb :
        if verbose:
            print("Domain annotation")
        check_program_config(["HMM"])
        # with annotation, check that hmmscan is installed
        hmm_domains = make_domains(dfasta_flat, hmmdb, workdir, cores)
        
    # filter overlapping domain and HCA domain too short or with not enough 
    # coverage
    if verbose:
        print("Filtering HCA annotation")
    domains = filter_domains(dfasta, seghca_domains, hmm_domains, hca_size, 
                             cut_hmm, nbover_hmm, cut_dom, 
                             nbover_dom, cut_hca, nbover_hca)
    # write selected domains in output file
    if verbose:
        print("Looking for domains")
    domlist, storedir, cnt_orph = write_msa_domains(dfasta, domains, workdir, output)

    if keepfasta:
        workdir_kfasta = os.path.join(workdir, "kept_fasta")
        if verbose:
            print("The fasta alignments to use for filtering against other databases "
                  "would be stored in {}".format(workdir_kfasta))
    
    path_hmm = []
    if cnt_orph == 0:
        print ("Exiting, no orphan domain found")
    else:
        # enrichment of domains
        if verbose:
            print("Creation and enrichment of orphan hmm models")
        path_hmm = dom_enrichment(domlist, workdir, name, seqdb, keepfasta=keepfasta, cutid=50, nbiter=5)

    return path_hmm

def clean_workdir(workdir, keepfasta):
    """ remove temporary working directory
    
    Parameter
    ---------
    
    workdir: string
        path to the working directory
    keepfasta: bool
        True, keep the fasta directory, needed for filtering, False, delete it
    """
    workdir_hca = os.path.join(workdir, "hca_annotation")
    workdir_hmm = os.path.join(workdir, "hmm_annotation")
    workdir_a3m = os.path.join(workdir, "alignment_a3m")
    workdir_kfasta = os.path.join(workdir, "kept_fasta")
    workdir_orph = os.path.join(workdir, "orphan_domains")
    #clean_path(workdir_hca)
    #clean_path(workdir_hmm)
    #if not keepfasta:
    #    clean_path(workdir_kfasta)
    #clean_path(workdir_orph)


def process_parameters():
    """ process input parameters
    
    Return
    ------
    
    params: object
        argparse object containing the user parameters
    """
    parser = argparse.ArgumentParser( 
                                 formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-i", "--input", action="store", dest="inputmsa", 
        metavar="FILE", help="the MSA input file", required=True)
    parser.add_argument("-d", "--database", action="store", dest="hmmdatabase",
        help="the domain hmm database to use", nargs="+", metavar="FILE", 
        default=[])
    parser.add_argument( "-o", "--output", action="store", dest="output", 
        metavar="FILE", help="output file prefix [<output>.out : list of "
        " domains, <output>.hmm : hmmdatabase]", default=None, required=True)
    parser.add_argument("-s", "--seqdb", action="store", dest="seqdb", 
        help="path to the sequence database used for enrichment", 
        metavar="FILE", 
        default="/data/tbita_01/work/Data/HHsuite/database/nr20_12Aug11")
    parser.add_argument("-w", "--workdir", action="store", dest="workdir", 
        metavar="DIR", help="working directory", required=True)
    parser.add_argument("-c", "--core", action="store", dest="cores", 
        metavar="INT", help="number of cores to use", type=int, default=1)
    grp_hca = parser.add_mutually_exclusive_group()
    grp_hca.add_argument("--perc-hca", action="store", dest="cut_hca", 
         help=("minimal percentage of sequences in the MSA that should have "
               "a domain"), default=20, metavar="FLOAT", type=float)
    grp_hca.add_argument("--nb-hca", action="store", dest="nbover_hca",
        help=("minimal number of sequences in the MSA that should have a"
              " domain"),  metavar="INT", type=int)
    grp_over = parser.add_mutually_exclusive_group()
    grp_over.add_argument("--perc-over", action="store", dest="cut_dom", 
        help=("minimal percentage of overlap allowed between hca segment for "
              "them to be considered as part of the same domain"), default=80, 
              metavar="FLOAT", type=float)
    grp_over.add_argument("--nb-over", action="store", dest="nbover_dom",
        help=("miniaml number of overlapping amino-acids between two hca segments"
              " to consider them as the same"), metavar="INT", 
        type=int)
    parser.add_argument("--hca-size", action="store", dest="hca_size", type=int,
        help="minimal size to consider a hca segment as a domain",
        default=30, metavar="FLOAT")
    grp_hmm = parser.add_mutually_exclusive_group()
    grp_hmm.add_argument("--perc-hmm", action="store", dest="cut_hmm", 
        help=("maximal percentage of overlap allowed between a hca segment and "
             "a hmm domain"), default=0, metavar="FLOAT", type=float)
    grp_hmm.add_argument("--nb-hmm", action="store", dest="nbover_hmm",
        help=("maximal number of overlapping amino-acids allowed between an"
              " hca segment and an hmm domain"), metavar="INT",
         type=int)
    parser.add_argument("--keep-fas", action="store_true", dest="keepfasta", 
        help="keep fasta results, fasta alignment are needed by hhsearch in the "
              "filtering program", default=False)
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", 
        default=False, help="active/inactive verbose mode")
    params = parser.parse_args()
    
    # transform to 0-1 ratio
    if params.cut_hca > 1.0:
        params.cut_hca /= 100.
    if params.cut_hmm > 1.0:
        params.cut_hmm /= 100.
    if params.cut_dom > 1.0:
        params.cut_dom /= 100.
    return params

class Parameters(object):
    def __init__(self):
        pass
    
def orphHCA_main(inputmsa, workdir, output, hmmdb=[], verbose=False, **kwargs):
    """ the main function, process parameter and call the appropriated functions
    """
    
    name = os.path.splitext(os.path.basename(output))[0]
    
    # set parameters
    params = Parameters()
    setattr(params, "name", name)
    for arg, val in kwargs.iteritems():
        if val != None:
            setattr(params, arg, val)
        
    
    # process io file
    if verbose:
        print("Check I/O file/directory")
        
    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    
    if not params.seqdb:
        print("Error, a sequence database is required (-s)", file=sys.stderr)
        return 1
                  
    all_path_hmm = process_one_msa(inputmsa, workdir, output, params, 
                                   hmmdb=hmmdb, verbose=verbose)
    
    # create database
    if verbose:
        print("Create database")   
    if all_path_hmm != []:
        outputdb = output+".hmm"
        create_database(all_path_hmm, outputdb)
    
    # cleanning
    clean_workdir(workdir, params.keepfasta)
    
    return 0


if __name__ == "__main__":
    params = process_parameters()
    ret = orphHCA_main(params.inputmsa, params.workdir, params.output, 
                hmmdb=params.hmmdatabase, keepfasta=params.keepfasta, 
                verbose=params.verbose, seqdb=params.seqdb, cores=params.cores,
                cut_hca=params.cut_hca, nbover_hca=params.nbover_hca,
                cut_dom=params.cut_dom, nbover_dom=params.nbover_dom,
                hca_size=params.hca_size, cut_hmm=params.cut_hmm, 
                nbover_hmm=params.nbover_hmm)
    sys.exit(ret)

