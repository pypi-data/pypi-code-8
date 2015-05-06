from pygenenet import CausalNetwork, Experiment, DataIO
from pygenenet.CausalNetwork import *
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

def evaluate_network(cnet, ref_net):
    d = np.abs(cnet) - np.abs(ref_net)
    false_pos = np.sum(d[d>0].count())
    false_neg = np.sum(d[d<0].count())
    return (false_pos, false_neg)
    
if __name__ == '__main__':
   
    filelist = ['net3_ssa_10/run-%s.tsd' % i for i in range(1, 21)]
    exp_set = Experiment.ExperimentSet(Experiment.read_experiments_from_files(filelist, format='sequential') )
    exp_set.drop(['P0', 'P1', 'P2'], axis=1, inplace=True)
    
    cnet = CausalNetwork(exp_set.species())
    thresholds =  { 'Tr': 0.75, 'Ta': 1.15, 'Tj': 2, 'Ti': 0.5, 'Tm': 0.}  # Tj: max # of parents in an influence vector, Ti: score for empty influence vector, Tm: merging influence vectors if their max-min score is <= Tm
    t  = time.time()
    learned = learn(exp_set, cnet, thresholds, nbins=3, bin_assignment = 1)
    t = time.time() -t 
    print "Learned causal network in %ss" % t
    print learned
    DataIO.draw_graph(learned, 'net3_ssa_10.gv' )


