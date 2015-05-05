#!/usr/bin/env python
# -*- coding: utf-8 -*-
# START LICENCE ##############################################################
#
# <one line to give the program's name and a brief idea of what it does.>
# Copyright (C) <year>  <name of author>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# END LICENCE ##############################################################
""" filteringOrphHCA is a sub program of the orphHCA package with purpose
to filter for redundancy a bunch of hmm.
It requires hhsearch.
"""

from __future__ import print_function
import sys, os, shlex, argparse, glob, tempfile
import subprocess, multiprocessing
import ConfigParser

__author__  = "Tristan Bitard-Feildel"
__email__   = "tristan.bitard.feildel@uni-muenster.de"
__year__    = 2014
__licence__ = "MIT"
__version__ = 0.1

__all__ = ["filter_hmm", "process_parameters"]

# checking that the environment variable is present
if not os.environ.get('ORPHHCA_DATA'):
    print("Please set the ORPHHCA_DATA environ variable to the location of "
          "PATH.ini", file=sys.stderr)
    sys.exit(1)
    
config = ConfigParser.ConfigParser()
config.read(os.path.join(os.getenv("ORPHHCA_DATA"),"PATH.ini"))


def execute_cmd(cmd, pathout=os.devnull, patherr=os.devnull):
    """ run subprocess on a cmd string
    
    Parameter
    ---------
    cmd: string
        the command line to execute
    """
    cmd = shlex.split(cmd)
    try:
        with open(pathout, "w") as ouf, open(patherr, "w") as erf:
            subprocess.check_call(cmd, stderr=erf, stdout=ouf)
    except:
        print("Failed to execute :\n{}".format(" ".join(cmd)), file=sys.stderr)
        raise RuntimeError
    
    
def process_parameters():
    """ process input parameters
    
    Return
    ------
    params: object
        argparse object containing the user parameters
    """
    parser = argparse.ArgumentParser( 
                                 formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", "--fastadir", action="store", dest="fastadir", 
        help="the directory with fasta alignments", required=True, metavar="DIR")
    parser.add_argument("-i", "--inputfile", action="store", dest="inhmmdb",
        help="the hmm database corresponding to the fasta alignments", 
        metavar="FILE")
    parser.add_argument("-w", "--workdir", action="store", dest="workdir",
        help="the working directory", required=True, metavar="DIR")
    parser.add_argument("-d", "--database", action="store", nargs="+", 
        dest="hmmdb", help="the list of hmm database to which the fasta "
        "alignments are compared to", required=True)
    parser.add_argument("-o", "--output", action="store", dest="outputfile",
        help=("the list of model that are similar to an other model in a "
        "database"), required=True, metavar="FILE")
    parser.add_argument( "-c", "--cutoff", action="store", dest="cutoff", 
        help="the similarity cutoff", default=80, type=float)
    parser.add_argument( "-v", "--verbose", action="store_true", dest="verbose",
        help="activate verbose mode", default=False)
    params = parser.parse_args()    
    if not os.path.isdir(params.workdir):
        os.makedirs(params.workdir)
    return params

    
def create_hhm(fastafiles, params):
    """ create hmm models using hhmaker from the fasta alignments
    
    Parameters
    ----------
    fastafiles: list
        the names of the fasta files
    params: object
        argparse parameters object of the script
        
    Return
    ------
    pathmodels: list
        the path to the hhm models
    """
    pathmodels = []
    for fastafile in fastafiles:
        pathfasta = os.path.join(params.fastadir, fastafile)
        workdir = os.path.join(params.workdir, "fasta2hhm")
        if not os.path.isdir(workdir):
            os.makedirs(workdir)
        name = os.path.splitext(fastafile)[0]
        pathhmm = os.path.join(workdir, name+".hhm")
        pathmodels.append(pathhmm)
        hhmaker_cmd = config.get("HMM", "hhmaker")
        cmd = "{} -i {} -o {} -M 50 -name {} ".format(hhmaker_cmd, pathfasta, pathhmm, name)
        try:
            execute_cmd(cmd)
        except:
            print("Error running {}".format(cmd), file=sys.stderr)
            sys.exit(1)
    return pathmodels


def check_database_names(hmmdb):
    """ check if name in databases are unique
    
    Parameter
    ---------
    hmmdb: string
        the path to the hmm model database
    
    Return
    ------
    size: int 
        number of models found
    """
    names = set([])
    with open(hmmdb) as inf:
        for line in inf:
            if line.startswith("NAME"):
                tmp = line.split()
                name = tmp[1]
                if name not in names:
                    names.add(name)
                else:
                    print ("Error : names should be unique between HMM, {}".format(name), file=sys.stderr)
                    sys.exit(1)
    if names == set([]):
        print ("Error : no HMM found in {}".format(hmmdb), file=sys.stderr)
        sys.exit(1)
    size = len(names)
    return size, names

    
def compare_models(list_of_models, params):
    """ compare hmm models using hhsearch software
    
    Parameters
    ----------
    list_of_models: list
        the path ot the individual domain hmm
    params: object
        argparse parameters object
        
    Return
    ------
    scores: dictionary
        the path to the hhsearch scores 
    """
    default_cmd = config.get("HMM", "hhsearch")
    default_cmd += " -i {} -d {} -M 50 -scores {}"
    scores = {}
    for hmmdb in params.hmmdb:
        scores[hmmdb] = []
        # create working directory per target database
        hmmdb_name = os.path.basename(hmmdb)
        workdir = os.path.join(params.workdir, hmmdb_name)
        if not os.path.isdir(workdir):
            os.makedirs(workdir)
        # run comparison for each models against the target database
        for path_model in list_of_models:
            name = os.path.splitext(os.path.basename(path_model))[0]
            pathout = os.path.join(workdir, name+".scores")
            scores[hmmdb].append(pathout)
            cmd = default_cmd.format(path_model, hmmdb, pathout)
            try:
                execute_cmd(cmd)
            except:
                print ("Error runnning {}".format(cmd), file=sys.stderr)
                sys.exit(1)
    return scores


def select_models(pathscores, params):
    """ read reasult files, get scores and select models above the cutoff
    
    Parameters
    ----------
    pathscores: list
        list of path to the hhsearch results
    params: object
        the argparse object storing arguments for this script
        
    Return
    ------
    selected: dict
        the dict of selected models and against which models they failed
    """
    selected = {}
    for hmmdb in pathscores:
        for scores in pathscores[hmmdb]:
            with open(scores) as inf:
                # header
                name = os.path.splitext(os.path.basename(scores))[0]
                line = inf.readline() # read name
                #name = inf.readline().strip()[5:]
                fam = inf.readline().strip()[5:]
                pathfile = inf.readline().strip()[5:]
                length = inf.readline().strip()[5:]
                # results
                line = inf.readline()# blank
                line = inf.readline()# result header
                for line in inf:
                    target_name = line.split()[0]
                    score = float(line[61:67]) 
                    # check if above cutoff
                    if score > params.cutoff:
                        selected.setdefault(name, []).append((hmmdb, target_name, score))
    return selected

def write_selected(selected_models, params):
    """ write an output line for each model above the cutoff when compared to an
    other model of an other database
    
    Parameters
    ----------
    selected_models: dict
        result dictionary
    params: object
        the argparse object storing arguments for this script
        
    """
    with open(params.outputfile, "w") as outf:
        for model in selected_models:
            for hmmdb, target, score in selected_models[model]:
                outf.write("{}\t{}\t{}\t{}\n".format(model, target, score, hmmdb))

    
def filter_main():
    """ the main function, process parameter and call the appropriated functions
    """
    # read parameters
    params = process_parameters()
    
    # get path to the fasta alignments, (generated by OrphHCA --keep-fasta option)
    if params.verbose:
        print ("Get fasta files")    
    fastafiles = [f for f in os.listdir(params.fastadir) if os.path.splitext(f)[1] == ".fasta"]
    if params.verbose:
        print("Number of fasta files selected {}".format(len(fastafiles)))

    # built hmm from fasta alignments with hhmaker 
    #if params.verbose:
    #    print("Create HMM to search with hhsearch the sequence database")
    #list_of_hmm = create_hhm(fastafiles, params)
    
    # check that we only have individual models names
    if params.verbose:
        print("Check the models of the input database")
    sizedb, model_names = check_database_names(params.inhmmdb)
    
    # run hmm models against targeted databases
    if params.verbose:
        print ("Compare models")
    scores = compare_models([os.path.join(params.fastadir, fastafile) for fastafile in fastafiles], params)
    
    # select models
    if params.verbose:
        print("Select models")
    selected = select_models(scores, params)
    
    # write in a file models with a high similarity and against with other hmms
    if params.verbose:
        print("Write selected models")
    write_selected(selected, params)
    
    # if the database is provided, removed models with a high similarity
        
    sys.exit(0)


if __name__ == "__main__":
    filter_main()


