#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Function of orphHCA relative to hmm creation and enrichment
"""


from __future__ import print_function
import os, sys
import shutil, shlex, subprocess
from orphhca_util import execute_cmd, config


__author__  = "Tristan Bitard-Feildel"
__email__   = "tristan.bitard.feildel@uni-muenster.de"
__year__    = 2014
__licence__ = "MIT"
__version__ = 0.1


def run_hhblits(dom, pathin, workdir, name, seqdb, percid=50, nbiter=5):
    """ Run the hhblits command to enrich hmm profiles
    
    Parameters
    ==========
    dom : string
        the domain MSA name 
    pathin : string
        the path to the domain MSA file
    params : object
        the argparse parameter object
    percid : int, default=50
        the percent of identity below which a hit is not conserved
    nbiter : int, default=5
        the number of iteration of hhblits
        
    Return
    ======
    pathout : string
        the path to the enriched hmm file
    """
    workdir = os.path.join(workdir, "alignment_a3m")
    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    pathout = os.path.join(workdir, name+"_"+dom+".a3m")
    hhblits_cmd = config.get("HMM", "hhblits")
    cmd = "{} -M 50 -i {} -oa3m {} -n {} -d {} -M 50 -all -noaddfilter -id {} -cpu 1".format(hhblits_cmd, pathin, pathout, nbiter, seqdb, percid)
    try:
        execute_cmd(cmd)
    except:
        print("Error running {}".format(cmd), file=sys.stderr)
        sys.exit(1)
    return pathout


def save_fasta(dom, pathin, workdir, name):
    """ save the fasta files
    
    Parameters
    ----------

    dom : string
        the domain MSA name 
    pathin : string
        the path to the domain MSA file
    params : object
        the argparse parameter object
        
    Return
    ------

    pathout : string
        the path to the reformated alignment
    """
    workdir = os.path.join(os.path.dirname(workdir), "kept_fasta")
    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    pathout = os.path.join(workdir, name+"_"+dom+".fasta")
    #print (workdir, pathout)
    shutil.copyfile(pathin, pathout)
    
def reformat_a3mtofas(dom, pathin, workdir, name):
    """ transform the a3m alignment to a fasta alignment
    
    Parameters
    ==========
    dom : string
        the domain MSA name 
    pathin : string
        the path to the domain MSA file
    params : object
        the argparse parameter object
        
    Return
    ======
    pathout : string
        the path to the reformated alignment
    """
    workdir = os.path.join(workdir, "alignment_a3m")
    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    pathout = os.path.join(workdir, name+"_"+dom+".fas")
    reformat_cmd = config.get("HMM", "reformat.pl")
    cmd = "{} {} {} -uc -noss -l 300".format(reformat_cmd, pathin, pathout)
    try:
        execute_cmd(cmd)
    except:
        print("Error running {}".format(cmd), file=sys.stderr)
        sys.exit(1)
    return pathout


def construct_hmm(dom, pathmsa, workdir, name):
    """ run hmmbuild to construct hmm model
    
    Parameters
    ==========
    dom : string
        the domain MSA name 
    pathin : string
        the path to the domain MSA file
    params : object
        the argparse parameter object

    Return
    ======
    pathhmm : string
        path to the hmm file
    """
    workdir = os.path.join(workdir, "msa2hmm")
    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    pathhmm = os.path.join(workdir, name+"_"+dom+".hmm")
    hmmbuild_cmd = config.get("HMM", "hmmbuild")
    #name = os.path.splitext(os.path.basename(output))[0]+"_"+dom
    name = name+"_"+dom
    cmd = "{} -n {} --amino {} {}".format(hmmbuild_cmd, name, pathhmm, pathmsa)
    try:
        execute_cmd(cmd)
    except:
        print("Error running {}".format(cmd), file=sys.stderr)
        sys.exit(1)
    return pathhmm


def clean_msa(ori_msa, pathmsa):
    """ filter msa by removing redundant sequences to the originals sequences
    
    Parameters
    ==========
    ori_msa : dict
        the dictionary with the original sequence edited
    pathmsa : string
        the path to the enriched msa file, this file will be used as output
    """
    new_msa = {}
    new_seq = {}
    # open enriched msa file and read the proteins sequences
    with open(pathmsa) as inf:
        for line in inf:
            if line[0] == "\n": continue
            if line[0] == ">":
                tmp = line[1:-1].split()
                name = tmp[0]
                new_msa[name] = ""
                new_seq[name] = ""
            else:
                new_msa[name] += line.rstrip()
                new_seq[name] += line.rstrip().replace("-","")
    # look for similar sequence and entries
    to_remove = set([])
    counted = {}
    for prot in ori_msa:
        counted[prot] = 0 
    for prot in new_msa:
        seq = new_seq[prot]
        if prot in ori_msa:
            # we expected the original to be here at least once
            if counted[prot] == 0:
                counted[prot] += 1
            # if they are here multiple time, we check that it's with a diff seq
            elif seq == ori_msa[prot]:
                to_remove.add(prot)
        else:
            # it's a different protein
            for prot_ori in ori_msa:
                seq_ori = ori_msa[prot_ori]
                # but we only keep different sequence (can be a diff name in db)
                if seq_ori == seq:
                    to_remove.add(prot)
    # removing sequences marked as to be removed
    for prot in to_remove:
        del new_msa[prot]
    # writting new MSA
    if new_msa != {}:
        with open(pathmsa, "w") as ouf:
            for prot in new_msa:
                ouf.write(">{}\n{}\n".format(prot, new_msa[prot]))
    else:
        print("Warning, no sequence remaining after filtering {}"
              "".format(pathmsa), file=sys.stderr)

def read_msa(path):
    """ read original msa 
    
    Parameter
    =========
    path : string
        path to the MSA file
    
    Return
    ======
    result : dict
        the dictionary containing the protein sequence without characters linked
        to MSA
    """
    result = {}
    with open(path) as inf:
        for line in inf:
            if line[0] == "\n" : continue
            if line[0] == ">":
                tmp = line[1:-1].split()
                name = tmp[0]
                result[name] = ""
            else:
                result[name] += line.rstrip().replace("-", "")
    return result


def run_enrichment(dom, ori_msa, path_msa, workdir, name, seqdb, keepfasta , cutid, nbiter):
    """ run the pipeline for one msa of an orphan domain
    
    Parameters
    ----------
    
    dom : string
        the domain MSA name 
    ori_msa : string
        the dictionary with the original sequence edited
    path_msa : string
        the path to the domain MSA file
    params : object
        the argparse parameter object
    cutid : int
        the percent of identity below which a hit is not conserved
    nbiter : int
        the number of iteration of hhblits
        
    """
    # run hhblits
    path_a3m = run_hhblits(dom, path_msa, workdir, name, seqdb, percid=cutid, nbiter=nbiter)
    # reformat
    path_reformat = reformat_a3mtofas(dom, path_a3m, workdir, name)
    clean_msa(ori_msa, path_reformat)
    # kept fasta alignment ?
    if keepfasta:
        save_fasta(dom, path_reformat, workdir, name)
    # create hmm
    path_hmm = construct_hmm(dom, path_reformat, workdir, name)
    return path_hmm
    
def dom_enrichment(domlist, workdir, name, seqdb, keepfasta=False, cutid=50, nbiter=5):
    """ Enrichment of previous MSA by hhblist
    
    Parameters
    ----------

    domlist : list
        a list of domain names
    params : object
        the argparse parameter object
    cutid : int, default=50
        the percent of identity below which a hit is not conserved
    nbiter : int, default=5
        the number of iteration of hhblits
        
    Return
    ------

    path_hmm : list
        a list path, one per hmm file
    """
    ori_msa, path_msa = {}, {}
    workdir = os.path.join(workdir, "orphan_domains")
    # read original msa models
    for dom in domlist:
        pathmsa = os.path.join(workdir, dom)
        ori_msa[dom] = read_msa(pathmsa)
        path_msa[dom] = pathmsa
    
    path_hmm = []
    # create the enrichment
    for dom in path_msa:
        path_hmm.append(run_enrichment(dom, ori_msa[dom], path_msa[dom], workdir, name, seqdb, keepfasta, cutid, nbiter))
        
    return path_hmm
