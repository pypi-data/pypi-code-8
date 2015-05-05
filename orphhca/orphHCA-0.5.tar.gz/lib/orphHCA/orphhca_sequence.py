#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Function of orphHCA relative to sequence processing
"""

from __future__ import print_function
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Alphabet import generic_protein
 
__author__  = "Tristan Bitard-Feildel"
__email__   = "tristan.bitard.feildel@uni-muenster.de"
__year__    = 2014
__licence__ = "MIT"
__version__ = 0.1

__all__ = ["transform_seq", "unmsa_characters", "read_multifasta", "msa2flat"]

#AA1 = ['C', 'Q', 'I', 'S', 'V', 'G', 'N', 'P', 'K', 'D', 'T', 'F', 'A', 'M', 'H', 'L', 'R', 'W', 'E', 'Y', 'X']
msa_characters = ["-", "?", "!", "*", "."]

def compute_offset_pos(seq, pos):
    """ compute the offset from a position in a MSA to the normal sequence
    
    Parameters
    ==========
    seq : string
        the sequence from the MSA 
    pos : int
        the position to convert
        
    Return
    ======
    k : int
        the position in the MSA
    """

    k = 0 
    cnt = 0 if seq[k] not in msa_characters else -1
    while cnt != pos and k+1 < len(seq):
        k += 1 
        if seq[k] not in msa_characters:
            cnt += 1
    return k


def new_startstop(seq, start, stop):
    """ Compute new starting positions, taking into account gaps and other 
    non amino acids characters
    
    Parameters
    ==========
    seq : string
        the sequence from the MSA
    start : int
        the start index
    stop : int
        the stop index
        
    Return
    ======
    offstart : int
        the new start
    offstop : int
        the new stop
    size : int
        the size of the segment
    """
    size = stop - start
    # need to add 1 to start, converting list indexes to positions
    offstart = compute_offset_pos(seq, start)
    offstop = compute_offset_pos(seq, stop)
    return offstart, offstop, size


def transform_seq(seq):
    """ replace all characters that are not part of a protein sequence by 
    emptiness
    """
    # TODO add character checking based on ASCII code
    return "".join("" if aa in msa_characters else aa for aa in seq)
    

def unmsa_characters(seq):
    return seq.replace("*", "-").replace("?", "-").replace("!","-").replace(".", "-")


def msa2flat(dfasta):
    """ Transform an MSA sequence to a full protein sequence
    
    Parameter
    =========
    dfasta : dict
        a dictionary containing the MSA fasta sequences
        
    Return
    ======
    dfasta_flat : dict
        a dictionary containing the fasta sequence without MSA characters
    """
    dfasta_flat = {}
    for prot, seqobj in dfasta.iteritems():
        seq = str(seqobj.seq)
        new_seq = Seq(transform_seq(seq), generic_protein)
        record = SeqRecord(new_seq, seqobj.id, seqobj.name, seqobj.description)
        dfasta_flat[prot] = record
    return dfasta_flat

