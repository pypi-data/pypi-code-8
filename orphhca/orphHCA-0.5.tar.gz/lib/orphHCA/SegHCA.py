#!/usr/bin/env python

description = """ SegHCA Segmentation HCA delineates segments with a High Hydrophobic Cluster Density (H2CD)

REQUIREMENT: networkx

@author: Guilhem FAURE @ Callebaut's Team 2013
"""

import sys
import optparse
import os
import shutil
import string
import subprocess
import tempfile
import re
import networkx as pgv
import bisect

def readSequence(fseq):
    """
    brief read a sequence file and put sequence into a string chain
    param fseq is the address of the file
    return seq is the sequence in a string chain
    """
    #===========================================================================
    # read the sequence
    #===========================================================================
    f = open(fseq)
    seq = ""
    for line in f:
        if line[0] == ">":
            header = line.strip()
        else:
            seq += line.strip()
    
    return seq

def transformSequence(seq, low_complexity=False):
    """
    brief transforme amino acid string chain into kind of HCA code as 1-> YIMLFWV  P-> P  0-> other 
    param seq is sequence as a string chain
    param low_complexity is a list or not to identify low complexity segment
    return setrans is a code of the sequence as a string chain such as 1-> YIMLFWV  P-> P  0-> other 
    """
    #===========================================================================
    # get the binary code 
    # 1-> YIMLFWV 
    # P-> P
    # 0-> other 
    #===========================================================================
    hydrophobe = "YIMLFWVC" # as the HCA method
    seqtrans = ""
    for ite, aa in enumerate(list(seq)):
        if low_complexity and ite+1 in low_complexity:
            seqtrans += "0"
        elif aa  in hydrophobe:
            seqtrans += "1"
        elif aa == "P":
            seqtrans += "P"
        else:
            seqtrans += "0"
    return seqtrans


def _getPosition(match, start):
    """
    """
    
    lite = []
    for ite, ii in enumerate(match):
        if ii == "1":
            lite.append(ite+start)
    return lite

def manageReplacement(seqtrans):
    """
    brief this step delete small cluster 1 and 11 by connectivity distance or Proline breaker
    param seqtrans is a string of sequence code 1-> hydrophobe P-> Proline and 0-> other
    return seqtrans is a string without small cluster there are replaced by 0 or 00
    """
    
    lsmall_cluster = [] # contains the position of small cluster 1 or 11
    
    #===========================================================================
    # 1/ small cluster 1 and 11
    #===========================================================================
    # #===========================================================================
    #===========================================================================
        
    #===========================================================================
    # we want to delete 000010000 and 0000110000
    # we proceed in 2 steps because of overlapping sometime like 000001000001100000000
    #===========================================================================
    for i in re.finditer(r"(?=(0{4}1{1,2}0{4}))", seqtrans):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        
        lsmall_cluster += _getPosition(match, start)
        
        #=======================================================================
        # replacement
        #=======================================================================
        seqtrans = seqtrans[:start] + "0"*lmatch + seqtrans[stop:]
    
    #===========================================================================
    # 2/ Proline surrounded
    #===========================================================================
    # #===========================================================================
    #===========================================================================
    
    #===========================================================================
    # we want to delete every 1 or 11 surounded by 2 prolines
    #===========================================================================
    for i in re.finditer(r"(?=(P0{0,3}1{1,2}0{0,3}P))", seqtrans):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        
        lsmall_cluster += _getPosition(match, start)
        
        #=======================================================================
        # replacement
        #=======================================================================
        seqtrans = seqtrans[:start+1] + "0"*(lmatch-2) + seqtrans[stop-1:]
    
    #===========================================================================
    # we want to delete every 1 or 11 surounded by 1 proline and 0000
    #===========================================================================
    # PX0000
    for i in re.finditer(r"(?=(P0{0,3}1{1,2}0{4}))", seqtrans):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        
        lsmall_cluster += _getPosition(match, start)
        
        #=======================================================================
        # replacement
        #=======================================================================
        seqtrans = seqtrans[:start+1] + "0"*(lmatch-5) + seqtrans[stop-4:]
        
    # 0000XP 
    for i in re.finditer(r"(?=(0{4}1{1,2}0{0,3}P))", seqtrans):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        
        lsmall_cluster += _getPosition(match, start)
        
        #=======================================================================
        # replacement
        #=======================================================================
        seqtrans = seqtrans[:start+4] + "0"*(lmatch-5) + seqtrans[stop-1:]
    
    #===========================================================================
    # remove begin + ruptor    
    #===========================================================================
    # P ruptor
    for i in re.finditer(r"(?=^(0{0,3}1{1,2}0{0,3}P))", seqtrans):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        seqtrans = "0"*(lmatch-1) + seqtrans[stop-1:]
    # 0000 ruptor
    for i in re.finditer(r"(?=^(0{0,3}1{1,2}0{4}))", seqtrans):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        seqtrans = "0"*(lmatch-1) + seqtrans[stop-4:]
    
    #===========================================================================
    # remove ruptor+end    
    #===========================================================================
    # 0000 ruptor
    for i in re.finditer(r"(?=(0{4}1{1,2}0{0,3})$)", seqtrans):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        seqtrans = seqtrans[:start]+"0"*(lmatch) 
    
    # P ruptor
    for i in re.finditer(r"(?=(P0{0,3}1{1,2}0{0,3})$)", seqtrans):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        seqtrans = seqtrans[:start+1]+"0"*(lmatch-1) 
    
    # print lsmall_cluster
    
        
    return seqtrans, lsmall_cluster
    
def getAmas(seqtrans):
    """ the old getAmas seems to be buggy, this new implementation is faster
    and safer
    """
    new_seq = seqtrans[:]
    seq_buffer, amas = [], []
    list_amas = []
    start = -1
    for i, aa in enumerate(seqtrans):
        # if proline check if existing amas and add it to the list
        if aa == "P":
            # replace hydrophilic buffer by Ruptor in the new sequence
            if seq_buffer:
                new_seq = new_seq[:i-len(seq_buffer)] + "R" * len(seq_buffer) + new_seq[i:]
                seq_buffer = []
            new_seq = new_seq[:i] + "R"  + new_seq[i+1:]
            if amas:
                list_amas.append([start, "".join(amas)])
                amas = []
        elif aa == "0":
            # add hydrophilic to buffer
            seq_buffer.append(aa)
        elif aa == "1" and amas == []:
            # replace hydrophilic buffer by Ruptor in the new sequence
            if seq_buffer:
                new_seq = new_seq[:i-len(seq_buffer)] + "R" * len(seq_buffer) + new_seq[i:]
                seq_buffer = []
            start = i
            amas.append(aa)
        elif aa == "1" and amas != []:
            # should we create a new amas or not ? check the length of the buffer
            if len(seq_buffer) > 3:
                list_amas.append([start, "".join(amas)])
                new_seq = new_seq[:i-len(seq_buffer)] + "R" * len(seq_buffer) + new_seq[i:]
                start = i
                amas, seq_buffer = [], []
            amas.extend(seq_buffer)
            amas.append(aa)
            seq_buffer = []
        else:
            if amas != []:
                list_amas.append([start, "".join(amas)])
            new_seq = new_seq[:i-len(seq_buffer)] + "R" * len(seq_buffer) + new_seq[i:]
            seq_buffer, amas = [], []
    # don't forget last one
    if amas:
        list_amas.append([start, "".join(amas)])
    if seq_buffer:
        new_seq = new_seq[:i-len(seq_buffer)+1] + "R" * len(seq_buffer)
    list_amas.sort()
    return list_amas, new_seq

def old_getAmas(seqtrans):
    """
    brief this step identify ruptor as 0{4 or more}, the no hydrophobe at the begining or the end and proline 0{0,3}
    param seqtrans is a string chain with 1 -> hydrophobe 0-> the other
    return new_seq is a strng chain with R-> ruptor 1 -> hydrophobe 0-> the other
    return list_amas is a list [pos, amas] containint the amas and the position amas is 1X1 X not contains any ruptro
    """
    #===========================================================================
    #===========================================================================
    # # RUPTOR
    #===========================================================================
    #===========================================================================
    
    #===========================================================================
    # 0000 ruptor
    #===========================================================================
    list_match = re.finditer(r"(?=(0{4}))", seqtrans)
    new_seq = seqtrans[:]
    ite = 0
    for i in  list_match:
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        new_seq = new_seq[:start]+ 4* "R" + new_seq[start+4:]
    
    #===========================================================================
    # P ruptor after - replace R0 R00 R000 by RR RRR RRRR
    #===========================================================================
    new_seq = new_seq.replace("P", "R")
    list_match = re.finditer(r"(?=(R0{1,3}))", new_seq)
    for i in  list_match:
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        new_seq = new_seq[:start]+ lmatch* "R" + new_seq[start+lmatch:]
        
    #===========================================================================
    # P ruptor before - replace 0R 00R 000R by RR RRR RRRR
    #===========================================================================
    list_match = re.finditer(r"(?=(0{1,3}R))", new_seq)
    for i in  list_match:
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        new_seq = new_seq[:start]+ lmatch* "R" + new_seq[start+lmatch:]
        
    
    #===========================================================================
    # begin - replace 00010101 by RRR10101 (or more than 3 0 at the beginning)
    #===========================================================================
    new_seq = list(new_seq)
    for ite, i in enumerate(new_seq):
        if i == '0':
            new_seq[ite] = "R"
        else:
            break
    new_seq = string.join(new_seq, "")
    
    #===========================================================================
    # end - replace 10101000 by 10101RRR (or more than 3 0 at the end)
    #===========================================================================
    new_seq = list(new_seq)
    for ite, i in enumerate(new_seq[::-1]):
        if i == '0':
            new_seq[len(new_seq)-ite-1] = "R"
        else:
            break
    
    new_seq = string.join(new_seq, "")
    
    #===========================================================================
    #===========================================================================
    # # GET AMAS
    #===========================================================================
    #===========================================================================
    list_amas = []
    
    #===========================================================================
    # amas border
    #===========================================================================
    # beg
    for ite, i in enumerate(new_seq):
        if i == "R":
            break
    if ite != 0:
        list_amas.append([0, new_seq[0:ite]])
        
    # end
    for ite, i in enumerate(new_seq[::-1]):
        if i == "R":
            break
    if ite != 0:
        list_amas.append([len(new_seq)-ite, new_seq[len(new_seq)-ite:]])
        
    # buggy here, try sequence "MTQTLKYASRV"
    
    #===========================================================================
    # amas middle
    #===========================================================================
    list_match = re.finditer(r"(?=(R[^R]+R))", new_seq)
    for i in  list_match:
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        list_amas.append([start+1, match[1:-1]]) # +1 to delete the R match
    list_amas.sort()
    return list_amas, new_seq
    

def removeSmallAmas(list_amas, seq, output = None):
    """
    brief this step remove the small cluster 1 or 11 if any big cluster are close before or after 7 amino acids. seq is modified this cluster is replace by R or RR
          a new list is generated containing each amas what we kept
    param list_amas is a list [position, amas]
    param seq is a list R -> ruptor(Proline, 0{4 or more}) 1 -> hydrophobe 0 -> the other
    return keepCluster is a list of cluster that we kept
    return seq is a list R -> ruptor(Proline, 0{4 or more}, 1 and 11 close a big cluster) 1 -> hydrophobe 0 -> the other
    """
    
    if output != None:
        fout = open(output, "w")
    
    keepCluster = []
    for ite, pos_amas in enumerate(list_amas):
        pos, amas = pos_amas
        add = False
        
        
        #=======================================================================
        # only amas 1 or 11
        #=======================================================================
        if len(amas) > 2:
            ##print pos_amas
            keepCluster.append(pos_amas)
            if output != None : fout.write("%s\t%s\n"%(pos+1, amas))
            continue
        
        #=======================================================================
        #=======================================================================
        # # is there a big amas close?
        #=======================================================================
        #=======================================================================
        
        #=======================================================================
        # can we search after?
        #=======================================================================
        if ite != len(list_amas)+1:
            # after?  ite+1 we search 1 amas to n after the current
            for next_pos_amas in list_amas[ite+1:]:
                next_pos, next_amas = next_pos_amas
                
                distance = next_pos - pos + len(amas) # next_pos is the begin of the next amas pos+len(amas) is the end of the current amas
                
                if distance > 7:
                    break
                
                if len(next_amas) > 2:
                    keepCluster.append(pos_amas)
                    if output != None : fout.write("%s\t%s\n"%(pos+1, amas))
                    add = True
                    break
            
        #=======================================================================
        # can we search before
        #=======================================================================
        # we do not add if we already find a big cluster after
        if ite != 0 and add == False:
            # before? [::-1] -> reverse the list_amas len(list_amas)-ite begin at the first previous amas
            for prev_pos_amas in list_amas[::-1][len(list_amas)-ite:]:
                
                prev_pos, prev_amas = prev_pos_amas
                
                distance = pos - (prev_pos+len(prev_amas)) # pos is the begining of the current amas prev_pos+len(prev_amas) is the end of the previous amas
                
                if distance > 7:
                    break
                
                if len(prev_amas) > 2:
                    keepCluster.append(pos_amas)
                    if output != None : fout.write("%s\t%s\n"%(pos+1, amas))
                    add = True
                    break
        
        
        # small amas is transform in RUPTOR
        if add == False:
            seq = seq[:pos]+len(amas)*"R"+seq[pos+len(amas):]
            if output != None : fout.write("%s\t%s\tD\n"%(pos+1, amas))
    
    if output != None : fout.close()
    return keepCluster, seq



def codeSequence(keepCluster, seq, smooth = False):
    """
    brief for each amas, we put only 1 as a code, example 10001 -> 11111
    param keepCluster is a list [pos, amas] contains each amas and their position
    return seq is the sequence R -> ruptor and 1-> amas with transformation R -> 0 and 1-> 1 in integer
    """
    
    for pos, amas in keepCluster:
        if smooth:
            seq = seq[:pos]+len(amas)*"1"+seq[pos+len(amas):]
        pass
    #print seq, len(seq)
    return map(int, list(seq.replace("R", "0")))
    
    
    

def removeProline(seqtransclean):
    """
    brief this function replace Proline by 0 to obtain a perfect binary string, after we redelete 1 or 11 surounded by 0000
    param seq is a string chain 1-> hydrophobe P->Proline and 0->other
    return seq is a binary code 1->hydrophobe 0-> other
    """
    
    seqtransclean
    for i in re.finditer(r"(?=(P))", seqtransclean):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        
        
    seqpro = seqtransclean.replace("P", "0")
    
    
    #===========================================================================
    # we remove 1 or 11 surounded by 0000 because P becomes now 0
    # for instance 0P001000011001000 -> becomes 00001000011001000 so we can remove the first 1 like  00000000011001000
    #===========================================================================
    for i in re.finditer(r"(?=(0{4}1{1,2}0{4}))", seqpro):
        match  = i.group(1)
        lmatch = len(match)
        start  = i.start()
        stop   = start + lmatch
        
        #=======================================================================
        # replacement
        #=======================================================================
        seqpro = seqpro[:start] + "0"*lmatch + seqpro[stop:]
    
    
    
    return seqpro



def listBinarize(seq):
    """
    brief here all the string sequence become an integer list
    param seq is the string of "0"/"1"
    return seq is the list of 0/1
    """
    return map(int, list(seq))
      

def smoothCluster(seqbin):
    """
    brief link the cluster if the connectivity distance is inferior to 0000
    param seqbin is the string code of the sequence
    return seqbin the cluster are linked 101 becomes 111
    """
    
    
    # add Proline as a ruptor
    ite_i=0
    noiterate = False
    for ite, i in enumerate(seqbin):
        if ite_i >= len(seqbin):
            break
        
        start_mover = False
        
        #=======================================================================
        # we find a 0000 ruptor
        #=======================================================================
        if seqbin[ite_i:ite_i+5] == "00001":
            start_mover = 5
        
        #=======================================================================
        # we find a Proline ruptor
        #=======================================================================
        if seqbin[ite_i] == "P": 
            #===================================================================
            # direct ruptor? P0000 or PP
            #===================================================================
            if seqbin[ite_i:ite_i+5] == "P0000" or seqbin[ite_i+1] == "P":
                ite_i+=1
                continue
            
            start_mover = 1 
            
        #=======================================================================
        # we find a rutpor let is search for the end of ruptor
        #=======================================================================
        if start_mover:
            for ite_j in range(ite_i + start_mover, len(seqbin)):
                
                stop_mover = False
                
                if seqbin[ite_j:ite_j+5] == "10000":
                    stop_mover = 5
                
                if seqbin[ite_j] == "P":
                    #===========================================================
                    # is there hydrophobe amas? P00000P or PXP with X contains 1
                    #===========================================================
                    if "1" not in seqbin[ite_i+start_mover:ite_j]:
                        break
                    stop_mover = 1
                
                #===============================================================
                # the end of the sequence
                #===============================================================
                if ite_j >= len(seqbin)-1:
                    stop_mover = ite_j
                
                if stop_mover:
                    seqbin = seqbin[:ite_i+start_mover]+ len(seqbin[ite_i+start_mover:ite_j])*'1' + seqbin[ite_j:]
                    ite_i = ite_j
                    noiterate = True
                    break
        if noiterate == False:
            ite_i+=1
        else:
            noiterate = False
                    
    return seqbin

  
def getDensity(seqbin):
    """
    brief computes the number of hydrophobe in a window
    param seqbin is a string code of the sequence 0 or 1
    return hydrotable is a table containing for each window and position the number of hydrophobe
    """
    
    #===========================================================================
    # iterator for the sequence
    #===========================================================================
    cutting = range(0, len(seqbin))
    
    #===========================================================================
    # each size of word
    #===========================================================================
    hydrotable = []
    begin = True
    
    # we reduce the windows if sequence are too small
    if len(seqbin) <17:
        lwindows = [len(seqbin)]
    else:
        lwindows = [17]#range(10,51)#[10, 20, 30, 40, 50]
    for size_word in lwindows:
        #tmppath, tmpout= tempfile.mkstemp()
        #fout = open(tmpout, "w")
        #fout = open("%s"%(size_word), "w")
        lscore= []
        
        # improvement lscore += [-1] * (size_word/2)
        begin = True
        l2 = [] # to try alignment in the begining of the windows
        for iter_seq in cutting:
            
            if iter_seq + size_word > len(seqbin):
                break
            
            score = sum(seqbin[iter_seq: iter_seq + size_word])/float(size_word)
            
            
            if begin:
                # for the begining of the window we put the first score
                lscore += [score] * (size_word/2)
                begin = False
            else:
                lscore.append(score)
                
            l2.append(sum(seqbin[iter_seq: iter_seq + size_word]))
        
        # for the end of the position in the window we put the same score
        lscore+= [score] * (size_word- size_word/2)#(size_word- size_word/2)   lscore+= [score] * (size_word- size_word/2)
        #lscore_inverse+= [score_inverse] * (len(seqbin_inverse)-1-iter_seq)#(size_word- size_word/2)
        # check print size_word, size_word/2, len(lscore), len(lscore)+size_word- size_word/2, iter_seq, lscore
        #fout.write(string.join(map(str, lscore))+"\n")
        
        hydrotable.append(lscore[:])
        
        #fout.close()
        #os.remove(tmpout)
    return hydrotable#, linkertable
    
    
def sumDensityWindow(hydrotable, output = None):
    """
    brief sym density for each position in each window
    param hydrotable is a table containing [[density for each position for window1], [density for each position for window2], ...]
    return list_score_position for each position of sequence sum of hydrophobe computed by all windows
    """
    
    if len(hydrotable[0]) <17:
        lwindows = [len(hydrotable[0])]
    else:    
        lwindows = [17]#range(10,51)
        
    #===========================================================================
    # SUM HYDROPHOBE WINDOWS
    #===========================================================================
    list_score_position = []
    if output != None : fout = open(output, "w")
    for position in range(len(hydrotable[0])):
        """
        if position+1 in lwindows:
            nbcurve = float(position +1)
        elif len(hydrotable[0])-position in lwindows:
            nbcurve = float(len(hydrotable[0])-position)
        else:
            nbcurve = float(len(hydrotable))
        """
        scorebyposition = 0 # sum the score for the current position
        scorebypositionlinker = 0 # sum the score for the current position
        lscorebyposition = [] # to count the position score of windows match
        for ite, window in enumerate(hydrotable):
            score = window[position]
            
            scorebyposition += window[position]
            lscorebyposition.append(window[position])
        list_score_position.append(scorebyposition/float(len(lscorebyposition)))
    if output != None : fout.write(string.join(map(str, list_score_position), "\n")+"\n")
    if output != None : fout.close()
    
    return list_score_position



def ofindMinima(list_score_position, size, t=0.2):
    """
    brief find the position where the curbe throught the threishold. And after find the local minima
    param list_score_position for each position, sum by windows / size windows of hydrophobe after smooth
    param t the threishold
    return limit_domain is the position of minima [beg,end, beg, end, beg, end...]
    """
    
    under_t = []
    upper_t = []
    for ite, i in enumerate(list_score_position):
        if i <= t:
            under_t.append(ite)
        else:
            upper_t.append(ite)
    
    limit = []
    b = under_t[0] # think about test if empty!!!!!
    limit.append(b)
    for ite, i in enumerate(under_t):
        if len(under_t) == ite+1:
            break
        
        n = under_t[ite+1] - i
        
        # small smoothing
        if n <= 2:
            pass
        else:
            limit.append(ite)
            b=under_t[ite+1]
    limit.append(b)
    limit.append(under_t[-1])
    
    
def findMinima(list_score_position, size, t=0.2):
    """
    brief find the position where the curbe throught the threishold. And after find the local minima
    param list_score_position for each position, sum by windows / size windows of hydrophobe after smooth
    param t the threishold
    return limit_domain is the position of minima [beg,end, beg, end, beg, end...]
    """
    
    #===========================================================================
    # SEARCH MINIMA TO FIND LIMITS
    #===========================================================================
    limit_domain = []
    state = ""
    
        
    for ite, i in enumerate(list_score_position):
        if ite == len(list_score_position)-1:
            continue
        
        first = i
        second = list_score_position[ite+1]
        
        # 0.0  .1 [.2 .4] .5 we throught the limit
        if first < t and second >= t:
            ##print "UP", ite, first, second
            findminima = False
            state = "UP"
            # find the local minimal to go this limit
            prev = first
            for j in range(ite-1, -1,-1):
                # check print j, list_score_position[j]    
                if prev <= list_score_position[j]:
                    ##print "minima", j
                    limit_domain.append(j)
                    findminima = True
                    break   
                prev = list_score_position[j]
            if not findminima:
                limit_domain.append(0)
        
        # .5 [.4 .2] .1 we down the limit
        if first >= t and second < t:
            state = "DOWN"
            findminima = False
            
            
            # find the local minimal after the limit
            next = second
            for j in range(ite+2, len(list_score_position)):
                # check print j, list_score_position[j]
                
                if next <= list_score_position[j]:
                    ##print "minima", j
                    findminima = True
                    # we add the first position because we down directly, it means there are hydrophobe in Nter
                    if len(limit_domain) == 0:
                        limit_domain.append(0)
                        
                    limit_domain.append(j)
                    break
                next = list_score_position[j]
            
            # These is the end of the sequence no minima, so we put the last limit
            if findminima==False:
                limit_domain.append(size-1)
            
    # we add the last position (size of the sequence) because the Cter are hydrophobe
    if state == "UP":
        limit_domain.append(size-1)        
    
    
    if len(limit_domain) == 0:
        limit_domain.append(0)
        limit_domain.append(size-1)
    
    return limit_domain    


def findAccurateLimit(limit_domain, list_of_group, threshold, output = None, final_only = False):
    """
    """
    
    #print limit_domain
    list_final_limit = []
    if output != None:
        fout = open(output+".domain", "w")
        fout.write("# Threshold: %s\n"%(str(threshold)))
        for i in range(0,len(limit_domain), 2):
            if i >= len(limit_domain)-1:
                break
            beg, end = limit_domain[i]+1, limit_domain[i+1]+1            
            potential_domain = []
            for j in list_of_group:
                jb, je = map(int,j[1:-1].split(","))
                
                gap = abs(beg-jb) + abs(end-je)
                potential_domain.append([gap, "%s-%s"%(jb, je)])
            if len(potential_domain) == 0:
                if not final_only:
                    fout.write("%s-%s N/A\n"%(beg, end))
                    list_final_limit.append("%s-%s"%(beg, end))
            else:
                size, lim = min(potential_domain)
                if final_only:
                    fout.write("%s\n"%(lim))
                    list_final_limit.append(lim)
                else:
                    fout.write("%s-%s %s\n"%(beg, end, lim))
                    list_final_limit.append(lim)
        fout.close()
    else:
        for i in range(0,len(limit_domain), 2):
            if i >= len(limit_domain)-1:
                break
            beg, end = limit_domain[i]+1, limit_domain[i+1]+1            
            potential_domain = []
            for j in list_of_group:
                jb, je = map(int,j[1:-1].split(","))
                
                gap = abs(beg-jb) + abs(end-je)
                potential_domain.append([gap, "%s-%s"%(jb, je)])
            if len(potential_domain) == 0:
                if not final_only:
                    list_final_limit.append("%s-%s"%(beg, end))
            else:
                size, lim = min(potential_domain)
                if final_only:
                    list_final_limit.append(lim)
                else:
                    list_final_limit.append(lim)
    return list_final_limit

def getSmallClusterDensity(seqbin, lsmall_cluster):
    """
    """
    
    seqbinpro = seqbin[:]
    for i in lsmall_cluster:
        seqbinpro[i] = 2
    
    
    #===========================================================================
    # iterator for the sequence
    #===========================================================================
    cutting = range(0, len(seqbinpro))
    
    #===========================================================================
    # each size of word
    #===========================================================================
    for size_word in [1, 10, 20, 30, 40, 50]:
        #fout = open("r%s"%(size_word), "w")
        lscore= []
        lscore += [0] * (size_word/2)
        for iter_seq in cutting:
            
            if iter_seq + size_word > len(seqbinpro)-1:
                break
            
            small_cluster = 0
            hydrophobe_cluster = 0
            for i in seqbinpro[iter_seq: iter_seq + size_word]:
                if i == 1:
                    hydrophobe_cluster += 1
                if i == 2:
                    small_cluster += 1
            try:
                ratio = float(small_cluster) / float(hydrophobe_cluster)
            except:
                ratio = 0.0
            lscore.append("%f"%(ratio))
        #fout.write(string.join(map(str, lscore))+"\n")
        #fout.close()
        
class Cluster:
    def __init__(self):
        pass
    def __str__(self):
        if hasattr(self, "start") and hasattr(self, "stop"):
            return "[{},{}]".format(self.start, self.stop)
        else:
            return ""

def clusterizeCluster(seqbin):
    """
    """
    #===========================================================================
    # get cluster and central position
    #===========================================================================
    dcluster = {}
    cluster = False
    for ite, is_amas in enumerate(seqbin):
        if cluster == False and is_amas:
            start = ite
            cluster = True
            continue
        if cluster == True and (not is_amas or ite>=len(seqbin)-1):
            stop = ite           
            if ite>=len(seqbin)-1:
                #name = "%s-%s"%(str(start+1), str(stop+1)) # we are at the end python begins 0 so we include the position
                ocluster = Cluster()
                ocluster.start = start+1
                ocluster.stop = stop+1
                dcluster[ite] = ocluster
            else:
                #name = "%s-%s"%(str(start+1), str(stop)) # we stop the cluster we are one position after so +1 but python begins by 0 so we let like that
                ocluster = Cluster()
                ocluster.start = start+1
                ocluster.stop = stop
                dcluster[ite] = ocluster
            cluster = False
    
    # no or one cluster so no need to cluster
    if len(dcluster) <=1:
        l = []
        for ite, ocluster in dcluster.iteritems():
            l.append(str(ocluster))
        return l
    
    ##PGV import pygraphviz as pgv
    ##PGV G=pgv.AGraph()
    G=pgv.Graph()
    selected = set([])
    for ite, ocluster in dcluster.iteritems():
        ##PGV G.add_node(i, fillcolor="blue", style="filled", len="10")
        G.add_node(str(ocluster))
        selected.add(str(ocluster))
    
    nbgroup_previous = len(dcluster)
    nbgroup = 0
    loop = 0
    max_id = len(seqbin)
    remember_dist = {}
    dcluster_indexes = sorted(dcluster.keys())
    while nbgroup_previous != nbgroup:
        
        #=======================================================================
        # update nbgroup_previous
        #=======================================================================
        nbgroup_previous = nbgroup #len(dcluster)
       
        if nbgroup == 1:
            break
        #=======================================================================
        # compute distance between cluster
        #=======================================================================
        name_select, min_new_name, dmin = [[],[]], None, 1e6 
        indexes = []
        #for ite_i, oclusteri in dcluster.iteritems():
            #for ite_j, oclusterj in dcluster.iteritems():
                #if ite_i >= ite_j:
                    #continue
        for i in range(len(dcluster_indexes)-1):
            ite_i = dcluster_indexes[i]
            oclusteri = dcluster[ite_i]
            ite_j = dcluster_indexes[i+1]
            oclusterj = dcluster[ite_j]
        
            #===============================================================
            # search for the way
            #===============================================================
            #if (ite_i, ite_j) in remember_dist:
                #dij = remember_dist[(ite_i, ite_j)]
                #tmp_clust.start = oclusteri.start
                #tmp_clust.stop = oclusterj.stop
            #elif (ite_j, ite_i) in remember_dist:
                #dji = remember_dist[(ite_j, ite_i)]
                #tmp_clust.start = oclusterj.start
                #tmp_clust.stop = oclusteri.stop
            #else:
            if oclusterj.start > oclusteri.stop:
                dij = oclusterj.start - oclusteri.stop
                flag = 0
                #remember_dist[(ite_i, ite_j)] = dij
            else:
                dij = oclusteri.start - oclusterj.stop
                flag = 1
                #remember_dist[(ite_j, ite_i)] = dij
            if dmin > dij:
                dmin = dij
                indexes = [ite_i, ite_j] if flag == 0 else [ite_j, ite_i]
            
        if indexes:
            new_clust = Cluster()
            new_clust.start = dcluster[indexes[0]].start
            new_clust.stop = dcluster[indexes[1]].stop
            #print new_clust
            #=======================================================================
            # graph
            #=======================================================================
            ## PGV G.add_edge(name_select[0], min_new_name, label=str(dmin))
            ## PGV G.add_edge(name_select[1], min_new_name, label=str(dmin))
            selectedi = dcluster[indexes[0]]
            selectedj = dcluster[indexes[1]]
            selected.add(str(selectedi))
            selected.add(str(selectedj))
            selected.add(str(new_clust))
            
            #new_index = min(indexes)
            dcluster_indexes.remove(max(indexes))
            dcluster[min(indexes)] = new_clust
            #===========================================================================
            # delete old composante
            #===========================================================================
            del dcluster[max(indexes)]
            #del dcluster[indexes[1]]
           
            #=======================================================================
            # update nbgroup
            #=======================================================================
            nbgroup = nbgroup_previous - 1
    
    return list(selected) #G.nodes()

def old_clusterizeCluster(seqbin):
    """
    """
    #===========================================================================
    # get cluster and central position
    #===========================================================================
    lcluster = []
    dcluster = {}
    scluster = []
    cluster = False
    for ite, i in enumerate(seqbin):
        if cluster == False and i == 1:
            start = ite
            cluster = True
            continue
        if cluster == True and (i == 0 or ite>=len(seqbin)-1):
            stop = ite
            
            # print start, stop, seqbin[start:stop+2], (float( (stop-1) - start) / 2.0) + start + 1 # -1 because of 0 is not amas it is the end / +1 because python begins by 0 in a list
            
            if ite>=len(seqbin)-1:
                name = "%s-%s"%(str(start+1), str(stop+1)) # we are at the end python begins 0 so we include the position
                scluster.append([start+1, stop+1])
            else:
                name = "%s-%s"%(str(start+1), str(stop)) # we stop the cluster we are one position after so +1 but python begins by 0 so we let like that
                scluster.append([start+1, stop])
            position = (float( (stop-1) - start) / 2.0) + start + 1 # -1 because of 0 is not amas it is the end / +1 because python begins by 0 in a list
            
            lcluster.append([name, position])
            
            dcluster[name] = position
            
            cluster = False
    
    # no or one cluster so no need to cluster
    if len(scluster) <=1:
        l = []
        for i in scluster:
            l.append("[%d,%d]"%(i[0], i[1]))
        return l
    
    ##PGV import pygraphviz as pgv
    ##PGV G=pgv.AGraph()
    G=pgv.Graph()
    for i in scluster:
        ##PGV G.add_node(i, fillcolor="blue", style="filled", len="10")
        G.add_node("[%d,%d]"%(i[0], i[1]))
    
    nbgroup_previous = len(scluster)
    nbgroup = 0
    loop = 0
    history = []
    while nbgroup_previous != nbgroup:
        
        #=======================================================================
        # update nbgroup_previous
        #=======================================================================
        nbgroup_previous = len(scluster)
        
        if nbgroup == 1:
            break
        #=======================================================================
        # compute distance between cluster
        #=======================================================================
        ldist = []
        for ite_i, i in enumerate(scluster):
            for ite_j, j in enumerate(scluster):
                
                
                if ite_i >= ite_j:
                    continue
                
                #===============================================================
                # search for the way
                #===============================================================
                if j[0] > i[1]:
                    dij = j[0] - i[1]
                    new_name = [i[0], j[1]]
                else:
                    dij = i[0] - j[1]
                    new_name = [j[0], i[1]]
                    
                ldist.append([dij, [i, j], new_name])
                
        dmin, name_select, new_name = min(ldist)
        
        ldist.sort()
        #===========================================================================
        # recompute the position
        #===========================================================================
        scluster.append(new_name)
        
        #===========================================================================
        # delete old composante
        #===========================================================================
        scluster.remove(name_select[0])
        scluster.remove(name_select[1])
        
        #=======================================================================
        # graph
        #=======================================================================
        ## PGV G.add_edge(name_select[0], new_name, label=str(dmin))
        ## PGV G.add_edge(name_select[1], new_name, label=str(dmin))
        
        G.add_edge("[%d,%d]"%(name_select[0][0], name_select[0][1]), "[%d,%d]"%(new_name[0], new_name[1]))
        G.add_edge("[%d,%d]"%(name_select[1][0], name_select[1][1]), "[%d,%d]"%(new_name[0], new_name[1]))
        
        scluster.sort()
        history.append(scluster[:])
        #=======================================================================
        # update nbgroup
        #=======================================================================
        nbgroup = len(scluster)
    
    return G.nodes()
    

def belongPrimaryThreshold(list_final_limit, list_score_position):
    """
    brief we search the linker position which are define by position between domain. After, We compute the mean score on no linker position
    param list_final_limit is a list containing refine position of domain
    param list_score_position is a list containing the score (mean of mean of windows) for each position
    return newthreishold the mean score for no linker position
    """
    
    # link the overlap domain?
    
    order_domain = []
    
    domain_position = set()
    for domain in list_final_limit:
        
        beg, end = map(int, domain.split("-"))
        
        seq = range(beg, end+1)
        domain_position.update(set(seq))
    
    # put the real limit?
    allseq = set(range(min(domain_position), max(domain_position)+1))
    
    linker = allseq.difference(domain_position)
    
    s = 0.0
    nolinker = 0
    for ite, i in enumerate(list_score_position):
        if ite+1 in linker:
            continue 
        s += i
        nolinker += 1
    
    # score for position no linker / number of position no linker = mean of score for a no linker position
    newthreshold = s/float(nolinker)
    
    return newthreshold


def runner(prot, seq, output, t=0.1):
    
    #if prot != None:
        #print prot
    #===========================================================================
    # obsolete identify low complexity segment by SEG algorithm
    #===========================================================================
    low_complexity = []#getSEGLW(fseq)
    
    seqori = seq[:]
        
    #===========================================================================
    # transforme sequence
    #===========================================================================
    low_complexity = [] # we remove the low_complexity because we saw error in 123289675 LCLL pos 40-50
    seqtrans = transformSequence(seq, low_complexity)
    
    #===========================================================================
    # get amas
    #===========================================================================
    # list_amas -> [position of the amas, amas]
    #print "--"
    #print seq, len(seq)
    #print seqtrans, len(seqtrans)
    list_amas, seq = getAmas(seqtrans)
    output_amas = output + ".amas"
    keepCluster, seq= removeSmallAmas(list_amas, seq, output = output_amas)
    
    #print seq
    seqbin = codeSequence(keepCluster, seq, smooth = True)
    #print seqbin
    #===========================================================================
    # get density of hydrophobe mean by windows
    #===========================================================================
    hydrotable = getDensity(seqbin)
    
    #===========================================================================
    # mean by position of all windows
    #===========================================================================
    output_dens = output+"_profil17.res"
    list_score_position = sumDensityWindow(hydrotable, output = output_dens)
    
    limit_domain = findMinima(list_score_position, len(seqbin), t)
    
    list_of_group = clusterizeCluster(seqbin)
    output_dom = output + ".domains"
    list_final_limit = findAccurateLimit(limit_domain, list_of_group, t, output = output_dom, final_only=True)
    

def main():
    usage = "usage %prog -s [FILE] OR -m [FILE] [options]"
    parser = optparse.OptionParser(description=description, usage=usage)
    group = optparse.OptionGroup(parser, "Argument",)
    group.add_option("-s", dest="seq", metavar="INPUT FILE",\
                     default=None,\
                     help="sequence file in fasta format")
    group.add_option("-m", dest="mseq", metavar="[INPUT FILE]",\
                     default=None,\
                     help="multi-sequence fasta file. Segment all sequences in the file")
    group.add_option("-o", dest="output", metavar="OUTPUT NAME",\
                     default="myres",\
                     help="root name of the output files (default: myres)")
    group.add_option("-t", dest="t", metavar="[T]",\
                     default=0.1,\
                     help="Threshold of HCP (default: 0.1)")
    group.add_option("-l", dest="limit", metavar="[L]",\
                     default=10000,\
                     help="Limit protein size (default: 10000). Stop analysis of big proteins, a gi.toobig file will be created to track them")
    
    
    parser.add_option_group(group)
    
    options, args = parser.parse_args()
      
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit("an input file given by -s or -m is required")
       
    
    fseq = options.seq
    mseq = options.mseq
    limitprotsize = int(options.limit)
    output = options.output
    t = float(options.t)
    
    
    
    # single sequence in fasta file
    if fseq:
        seq = readSequence(fseq)
        runner(None, seq, output, t)
    
    # multifasta
    if mseq:
        f = open(mseq)
        dseq = {}
        dseq["order"] = []
        for i in f:
            if i[0] == ">":
                header= i.strip()
                gi = i.split("|")[1]
                dseq["order"].append(gi)
                dseq[gi] = ""
            else:
                dseq[gi] += i.strip()
        f.close()
        
        lseq = []
        for i in dseq["order"]:
            if os.path.exists(i+".domain"):
                continue
            else:
                lseq.append([i, dseq[i]])
        
        ite = 0
        size = len(lseq)
        for gi, i in lseq:
            #try:
            print gi
            if len(i) > limitprotsize:
                fout = open("%s.toobig"%(gi), "w")
                fout.close()
                continue
            
            runner(None, i, gi, t)
            ite+=1
            print "%d / %d DONE"%(ite, size) 
        
            
    


if __name__ == "__main__":
    main()
