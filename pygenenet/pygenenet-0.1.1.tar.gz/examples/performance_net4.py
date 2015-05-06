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
 
    refnet = CausalNetwork(['CI','GFP', 'LacI', 'TetR'])
    refnet['CI']   = [0, 0, 0, 0]
    refnet['GFP']  = [0, 0, 0, 0]
    refnet['LacI'] = [-1, 1, -1, -1]
    refnet['TetR'] = [0, 0, 0, 0]

    nexps =  [2, 3, 4, 5, 10, 15, 20]
    datafreqs = [10, 100]

    for fq in datafreqs:
        times = []
        incorrect = []
        for ne in nexps:
            filelist = ['net4_ssa_%s/run-%s.tsd' % (fq, i) for i in range(1,ne+1)]
            exp_set = Experiment.ExperimentSet(Experiment.read_experiments_from_files(filelist, format='sequential') )
            exp_set.drop(['Promoter_CI', 'Promoter_LacI', 'Promoter_GFP', 'Promoter_TetR'], axis=1, inplace=True)
            cnet = CausalNetwork(exp_set.species())
            thresholds =  { 'Tr': 0.75, 'Ta': 1.15, 'Tj': 2, 'Ti': 0.5, 'Tm': 0.}  # Tj: max # of parents in an influence vector, Ti: score for empty influence vector, Tm: merging influence vectors if their max-min score is <= Tm
            t  = time.time()
            learned = learn(exp_set, cnet, thresholds, nbins=4, bin_assignment = 1)
            t = time.time() -t 
            times.append(t)
            (fp, fn) = evaluate_network(learned, refnet)
            incorrect.append(fp+fn)
            # print "Learned causal network in %ss" % t
            # print learned
            DataIO.draw_graph(learned, 'demo4.gillespie_%s.%sexps.gv' % (fq, ne) )

        fig, ax1 = plt.subplots()
        ax1.plot(nexps, times, linestyle='-', marker='o', color='b')
        ax1.set_ylabel('Calculating time (s)')
        for tl in ax1.get_yticklabels(): tl.set_color('b')

        ax2 = ax1.twinx()
        ax2.plot(nexps, incorrect, linestyle='-', marker='o', color='r')
        ax2.set_ylabel('# of incorrect connections (false positive + false negative)')
        ax2.set_ylim(-0.02, np.max(incorrect)+0.02)
        for tl in ax2.get_yticklabels(): tl.set_color('r')
        fig.suptitle("Data set: net4_ssa_%s" % fq)
        fig.set_size_inches((10,3.5))
        plt.savefig("performance-net4_ssa_%s.png" % fq)
        fig.show()
