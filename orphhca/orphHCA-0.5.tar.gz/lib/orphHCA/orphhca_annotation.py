#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Function of orphHCA relative to annotation processing
"""

from __future__ import print_function, division
import sys, os, shlex, subprocess, tempfile
from Bio import SeqIO
from SegHCA import runner
from orphhca_util import config, execute_cmd
from orphhca_io import read_hmmscan
from orphhca_sequence import new_startstop, msa_characters


__author__  = "Tristan Bitard-Feildel"
__email__   = "tristan.bitard.feildel@uni-muenster.de"
__year__    = 2014
__licence__ = "MIT"
__version__ = 0.1

__all__ = ["read_seghca", "makeHCA"]


def read_seghca(results):
    """ Read pfam annotation and take : domain name, seq start, seq stop
    
    Parameter
    =========
    results : dictionary
        contain the path of the seghca results for each protein
    
    Return
    ======
    annotation : dictionary
        annotation for each protein
    """
    annotation = {}
    for prot in results:
        pathf, pathabsf = results[prot]
        annotation[prot] = []
        with open(pathabsf+".domains.domain") as f:
            for line in f:
                if line[0] == "\n" or line[0] =="#": continue
                tmp = map(int,line.split("-"))
                annotation[prot].append((tmp[0]-1, tmp[1]))
                # annotation start at 1
    return annotation

def make_hca(dfasta, workdir, cores=1):
    """ Run pfam annotation on amino acid sequence
    
    Parameters
    ==========
    dfasta : dict
        dictionary containing the protein sequences
    workdir : string
        path to working directory
    cores: int
        number of cpu to use
    
    Return
    ======
    annotations : dictionary
        seghca annotations
    """
    # init parameters
    nbcpu = cores
    workdir = os.path.join(workdir, "hca_annotation")
    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    results={}
    # start to create SegHCA results
    for cnt, prot in enumerate(dfasta):
        bioseq = dfasta[prot]
        prot_workdir = os.path.join(workdir, "prot_{}".format(cnt))
        if not os.path.isdir(prot_workdir):
            os.makedirs(prot_workdir)
        # create temporary file
        outputf, outputpath = tempfile.mkstemp(dir=prot_workdir)
        runner(prot, str(bioseq.seq), outputpath)
        results[prot] = (outputf, outputpath)
        os.close(outputf)
    
    annotations = read_seghca(results)

    return annotations    

def make_domains(dfasta, hmmdatabase, workdir, cores=1):
    """ Start domain annotation with all databases
    
    Parameters
    ==========
    dfasta: dict
        the fasta sequences of the proteins
    hmmdatabase: list
        list of hmmdatabases to used
    workidr: string
        path to working directory
    cores: int
        number of cpu to use
        
    Return
    ======
    annotations : dictionary
        the annotation for each protein
    """
    annotations = {}
    # initialise annotations
    for prot in dfasta:
        annotations[prot] = []
    nbcpu = cores
    # create temporary file to store the sequences
    workdir = os.path.join(workdir, "hmm_annotation")
    if not os.path.isdir(workdir):
        os.makedirs(workdir)
    # create temporary file to store the sequences
    fastaf, fastapath = tempfile.mkstemp(dir=workdir)
    SeqIO.write(dfasta.values(), fastapath, "fasta")
    os.close(fastaf)
    hmmscan_cmd = config.get("HMM", "hmmscan")
    basename = os.path.basename(fastapath)
    for database in hmmdatabase:
        # create output file for the annotation
        hmm_base= os.path.basename(database)
        output = os.path.join(workdir, basename+"."+hmm_base+".out")
        domoutput = os.path.join(workdir, basename+"."+hmm_base+".domout")
        # create annotation
        cmd = "{} -o {} --domtblout {} --cpu {} --cut_ga {} {}".format(
                     hmmscan_cmd, output, domoutput, nbcpu, database, fastapath)
        try: 
            execute_cmd(cmd)
        except :
            sys.exit(1)
        # read annotation
        db_annotation = read_hmmscan(domoutput)
        for prot in db_annotation:
            annotations[prot].extend(db_annotation[prot])
    os.remove(fastapath)
    return annotations

def filter_domains(dfasta, hca_domains, hmm_domains, hca_size, cut_hmm, nb_hmm, cut_dom, nb_dom, cut_hca, nb_hca):
    """ filter hca domain annotation based and overlaps with hmm domain 
    annotation
    
    Parameters
    ==========
    dfasta : dict
        the dictionary containing MSA protein sequences
    hca_domains : dict
        positions for each protein of hca domains
    hmm_domains : dict
        positions for each protein of hmm domains
    hca_size; int
        minimal size of the hca domain
    cut_hmm; float
        maximal allowed coverage between domains from the input databases and
        hca-domains
    nb_hmm: int
        maximal allowed number of amino-acids covering domains from the input 
        databases and hca-domains
    cut_dom: float
        minimal required coverage between hca-domains to consider them to be the
        same domain
    nb_dom: int
        minimal number of MSA corresponding amino-acids between hca-domains to 
        consider them to be the same domain
    cut_hca: float
        minimal percentage of presence across proteins of the MSA for an 
        hca-domain to be considered as conserved (and kept)
    nb_hca: int
        minimal number of proteins of the MSA for an hca-domain to be 
        considered as conserved (and kept)
    
    Return
    ======
    annotations : dict
        the selection of new domains with their positions on each proteins
    """
    # get orphan
    orphans = compute_hca_orphan(dfasta, hca_domains, hmm_domains, hca_size, cut_hmm, nb_hmm)
    # get conserved orphan
    annotations =  conserved_orphan(dfasta, orphans, cut_dom, nb_dom, cut_hca, nb_hca)
    return annotations


def hca_orphan(hca_domains, hmm_domains, seq_size, hca_size, cut_hmm, nb_hmm):
    """ HCA orphans domains are protein sequence area defined as domain 
    by SegHCA but without any known pfam domain annotation
    
    Parameters
    ==========
    hca_domains : list
        list of start and stop positions of HCA domain for a protein
    hmm_domains : list
        list of start and stop positions of HMM domain for a protein
    seq_size : int
        the length of the protein
    hca_size; int
        minimal size of the hca domain
    cut_hmm; float
        maximal allowed coverage between domains from the input databases and
        hca-domains
    nb_hmm: int
        maximal allowed number of amino-acids covering domains from the input 
        databases and hca-domains
    
    Return
    ======
    orphans : list
        kept positions of putative orphan domains
    """
    hmm_pos = [0] * seq_size
    for start, stop in hmm_domains:
        for i in range(start, stop):
            hmm_pos[i] = 1

    orphans = []
    for start, stop in hca_domains:
        size = float(stop-start)
        if size >= hca_size:
            hmm_cov = sum(hmm_pos[start:stop])
            ratio = hmm_cov / size
            if (((ratio <= cut_hmm and cut_hmm != True) or 
                 (hmm_cov <= nb_hmm and nb_hmm != True)) and 
                  start != stop):
                orphans.append((start, stop))
    return orphans
    
def compute_hca_orphan(dfasta, hca, pfam, hca_size, cut_hmm, nb_hmm):
    """ for all protein compute hca orphans
    
    Parameters
    ==========
    dfasta : dict
        fasta sequences of each proteins
    hca : dict
        dict of start and stop positions of HCA domain for all proteins
    pfam : dict
        dict of start and stop positions of HMM domain for all proteins
    hca_size; int
        minimal size of the hca domain
    cut_hmm; float
        maximal allowed coverage between domains from the input databases and
        hca-domains
    nb_hmm: int
        maximal allowed number of amino-acids covering domains from the input 
        databases and hca-domains
    
    Return
    ======
    orphans : dict
        kept positions of putative orphan domains for each proteins
        
    """
    orphans = {}
    for prot in dfasta:
        seq_size = len(str(dfasta[prot].seq))
        orphans[prot] = hca_orphan(hca[prot], pfam.get(prot, []), seq_size, hca_size, cut_hmm, nb_hmm)
    return orphans

class SegOrph:
    def __init__(self, id, name, start, stop, msastart, msastop):
        self.id = id
        self.name = name
        self.start = start
        self.stop = stop
        self.msastart = msastart
        self.msastop = msastop
    def __eq__(self, other):
        return all([self.name==other.name, self.start==other.start, 
            self.stop==other.stop, self.msastart==other.msastart,
            self.msastop==other.msastop])
    def __hash__(self):
        return hash((self.name, self.start, self.stop, self.msastart, self.msastop))

def conserved_orphan(dfasta, orphans, cut_dom, nb_dom, cut_hca, nb_hca):
    """ Look at each hca orphan and compute the number of sequence that share
    the same hca orphan in the msa
    
    Parameters
    ==========
    dfasta : dict
        fasta sequences of each proteins
    orphans : dict
        kept positions of putative orphan domains for each proteins
    cut_dom: float
        minimal required coverage between hca-domains to consider them to be the
        same domain
    nb_dom: int
        minimal number of MSA corresponding amino-acids between hca-domains to 
        consider them to be the same domain
    cut_hca: float
        minimal percentage of presence across proteins of the MSA for an 
        hca-domain to be considered as conserved (and kept)
    nb_hca: int
        minimal number of proteins of the MSA for an hca-domain to be 
        considered as conserved (and kept)
    
    Return
    ======
    conserved : dict
        conserved domains for each proteins
    """
    nb_seq = float(len(dfasta))
    conserved, dorphans = {}, {}
    iorphans = 0
    for prot1 in dfasta:
        seq1 = str(dfasta[prot1].seq)
        orph1 = orphans[prot1]
        for o1, (start1, stop1) in enumerate(orph1):
            # compute segment position on MSA
            msastart1, msastop1, size1 = new_startstop(seq1, start1, stop1)
            seg1 = SegOrph(iorphans, prot1, start1, stop1, msastart1, msastop1)
            if seg1 not in dorphans:
                dorphans[seg1] = iorphans
                for prot2 in dfasta:
                    if prot1 != prot2:
                        seq2 = str(dfasta[prot2].seq)
                        orph2 = orphans[prot2]
                        for o2, (start2, stop2) in enumerate(orph2):
                            # check that no domains has been assigned to this 
                            # segment
                            
                            # compute segment position on MSA                                
                            msastart2, msastop2, size2 = new_startstop(seq2,
                                                                start2, stop2)
                            seg2 = SegOrph(iorphans, prot2, start2, stop2, 
                                                        msastart2, msastop2)
                            if seg2 not in dorphans:
                                msastart = max(msastart1, msastart2)
                                msastop = min(msastop1, msastop2)
                                common_aa = 0.0
                                size = max(size1, size2)
                                # compute number of amino acid matching
                                for k in range(msastart, msastop):
                                    if (seq1[k] not in msa_characters and 
                                        seq2[k] not in msa_characters):
                                        common_aa += 1.0
                                # if enought tag the segments are being part of 
                                # the same domain
                                cov = common_aa / size
                                if ((cov > cut_dom and cut_dom != True) or 
                                    (common_aa > nb_dom and nb_dom != True)):
                                    dorphans[seg2] = iorphans
                iorphans += 1
                
    # check how many proteins there is for each putative orphan domains    
    cnt_dorphans = {}
    for seg, num in dorphans.iteritems():
        cnt_dorphans.setdefault(num, []).append(seg)
    
    to_keep = []
    for num in cnt_dorphans:
        if (len(cnt_dorphans[num]) > 1 and
            ((len(cnt_dorphans[num]) / nb_seq >= cut_hca and cut_hca != True) or
             (len(cnt_dorphans[num]) > nb_hca and nb_hca != True))):
                to_keep.append(num)
    # final dictionary        
    for new_num, num in enumerate(to_keep):
        for seg in cnt_dorphans[num]:
            conserved.setdefault(new_num, {}).setdefault(seg.name, (seg.start,    
                                           seg.stop, seg.msastart, seg.msastop))
    return conserved
