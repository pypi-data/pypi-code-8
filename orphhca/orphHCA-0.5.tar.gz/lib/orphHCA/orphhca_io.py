#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Function of orphHCA relative to IO management
"""

from __future__ import print_function
import os, shutil, sys
from orphhca_util import config, execute_cmd
from Bio import SeqIO
from orphhca_sequence import unmsa_characters, transform_seq

__author__  = "Tristan Bitard-Feildel"
__email__   = "tristan.bitard.feildel@uni-muenster.de"
__year__    = 2014
__licence__ = "MIT"
__version__ = 0.1

    
def read_multifasta(path):
    """ use Bio.SeqIO to read the fasta file and convert it into a dictionary
    
    Parameter
    =========
    path : string
        path to the fasta file
        
    Return
    ======
    record_dict : dict
        a dictionary containing the Bio sequence object
    """
    handle = open(path, "rU")
    record_dict = SeqIO.to_dict(SeqIO.parse(handle, "fasta"))
    handle.close()
    return record_dict


def write_msa_domains(dfasta, domains, workdir, output):
    """ write the sequences corresponding to putative new domains
    
    Parameters
    ==========
    dfasta : dict
        dictionary of MSA protein sequences
    domains : dict
        dictionary containing for each protein the position of the domain
    params: object
        argparse parameter object
        
    Returns
    =======
    domlist : list
        a list of orphan domain names
    storedir: string
        the directory storing the MSA per new domains
    cnt: int
        the number of new orphan domains
    """
    storedir = os.path.join(workdir, "orphan_domains")
    if not os.path.isdir(storedir):
        os.makedirs(storedir)
    
    domlist = []
    doms2prot = {}
    for cnt, dom in enumerate(domains):
        pathout = os.path.join(storedir, "orphan_{}.msa".format(cnt))
        domlist.append("orphan_{}.msa".format(cnt))
        min_start, min_msastart = 0,  0
        max_stop, max_msastop = 1e6, 1e6
        for prot in domains[dom]:
            start, stop, msastart, msastop = domains[dom][prot]
            if msastart > min_msastart:
                min_start = start
                min_msastart = msastart
            if msastop < max_msastop:
                max_stop = stop
                max_msastop = msastop
        with open(pathout, "w") as outf:
            for prot in domains[dom]:
                start, stop, msastart, msastop = domains[dom][prot]
                tmp_seq = str(dfasta[prot].seq[min_msastart: max_msastop])
                doms2prot.setdefault(prot, []).append((dom, min_start, max_stop,
                                        start, stop, min_msastart, max_msastop))
                seq = unmsa_characters(tmp_seq)
                outf.write(">{} orph_{} {}-{}\n{}\n".format(prot, cnt, 
                                                   min_start+1, max_stop, seq))
    with open(output+".out", "w") as outfile:
        for prot in doms2prot:
            tmp_seq = str(dfasta[prot].seq)
            seq_ = unmsa_characters(tmp_seq)
            seq = transform_seq(tmp_seq)
            outfile.write(">{} {}\n".format(prot, len(seq)))
            for dom, start, stop, oristart, oristop, min_msastart, max_msastop in doms2prot[prot]:
                # TODO make it more efficient -> function
                new_start = min_msastart - seq_[:min_msastart].count("-")
                new_stop = max_msastop - seq_[:max_msastop].count("-")
                outfile.write("{} {} orph_{} Nan # {} {} \n".format(new_start+1, new_stop, 
                                                        dom, oristart, oristop))
    return domlist, storedir, len(domlist)
    

#def write_domains(dfasta, domains, output):
    #""" write the sequences corresponding to putative new domains
    
    #Parameters
    #==========
    #dfasta : dict
        #dictionary of protein sequences
    #domains : dict
        #dictionary containing for each protein the position of the domain
    #output: string
        #output path of domains per proteins
    #"""
    
    #doms2prot = {}
    #for cnt, dom in enumerate(domains):
        #min_start, min_msastart = 0,  0
        #max_stop, max_msastop = 1e6, 1e6
        #for prot in domains[dom]:
            #start, stop, msastart, msastop = domains[dom][prot]
            #if msastart > min_msastart:
                #min_start = start
                #min_msastart = msastart
            #if msastop < max_msastop:
                #max_stop = stop
                #max_msastop = msastop
        #for prot in domains[dom]:
            #doms2prot.setdefault(prot, []).append((dom, min_start+1, max_stop,
                                                   #start, stop))
            
    #with open(output+".out", "w") as outfile:
        #for prot in doms2prot:
            #outfile.write(">{} {}\n".format(prot, len(str(dfasta[prot].seq))))
            #for dom, start, stop, oristart, oristop in doms2prot[prot]:
                #outfile.write("{} {} orph_{} Nan # {} {} \n".format(start, stop, 
                                                        #dom, oristart, oristop))

    #return domlist, storedir, len(domlist)
    
def read_hmmscan(path):
    """ read the hmmscan domtblout ouput file and store domain annotation for 
    each proteins
    
    Parameter
    =========
    path : string
        path to the hmmscan domtblout output
    
    Return
    ======
    annotation : dict
        domain annotation
    """
    annotation = {}
    with open(path) as inf:
        for line in inf:
            if line[0] == "#":
                continue
            tmp = line.split()
            prot = tmp[3]
            start = int(tmp[19])
            stop = int(tmp[20])
            annotation.setdefault(prot, []).append((start, stop))
    return annotation

def create_database(pathhmms, pathdb):
    """ create a hmm database from hmm path
    
    Parameters
    ==========
    pathhmms: list
        list of path, one per hmm files
    pathdb : string
        filename of the new database
    """
    with open(pathdb, "w") as inf:
        for tmp_file in pathhmms:
            with open(tmp_file) as tmpf:
                inf.write(tmpf.read())
    #hmmpress_cmd = config.get("HMM", "hmmpress")
    #cmd = "{} -f {}".format(hmmpress_cmd, pathdb)
    #execute_cmd(cmd)


def clean_path(path):
    """ clean a directory
    
    Parameter
    =========
    path : string
        the path to the directory or the file to clean
    """
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        print ("Warning : cannot delete {}, check if path exist" .format(path), file=sys.stderr)

