from LearningCausalNetwork import CausalNetwork, Experiment, DataIO
from LearningCausalNetwork.CausalNetwork import *
import numpy as np
import pandas as pd

if __name__ == '__main__':
    
    filelist = ['test_data/gillespie_10/run-%s.tsd' % i for i in range(1,11)]
    thresholds =  { 'Tr': 0.75, 'Ta': 1.15, 'Tj': 2, 'Ti': 0.5, 'Tm': 0.}  # Tj: max # of parents in an influence vector, Ti: score for empty influence vector, Tm: merging influence vectors if their max-min score is <= Tm

    exp_set = Experiment.ExperimentSet(Experiment.read_experiments_from_files(filelist, format='sequential') )
    exp_set.drop(['Promoter_CI', 'Promoter_LacI', 'Promoter_GFP', 'Promoter_TetR'], axis=1, inplace=True)
    cnet = CausalNetwork(exp_set.species())
    binned = exp_set.digitize(nbins= 4, bin_assignment = 1)
    bins = { sp:  np.unique(binned[sp]) for sp in cnet}


    # species_to_test = 'GFP'
    species_to_test = 'LacI'
    iv1 = cnet.influences(species_to_test)
    ivs = []
    scores = []
    pcd = []
    for i in range(0,4):
        iv = iv1.copy()
        iv[:] = 0
        iv[i] = -1
        pcd1 = binned.project(species_to_test, [cnet.columns[i], species_to_test])
        pcd1['prob_incr'] = pcd1['count_incr'] / pcd1['count']
        s1 = score(species_to_test, iv, [species_to_test], binned,  bins, thresholds)
        ivs.append(iv)
        scores.append(s1)
        pcd.append(pcd1)

    # for i in (-1, 1):
    #     iv = iv1.copy()
    #     iv[:] = 0
    #     iv[2] = i
    #     pcd1 = binned.project('GFP', ['LacI', 'GFP'])
    #     p1 = prob_incr('GFP', pcd1, min_occurences = 3)
    #     s1 = score('GFP', iv, ['GFP'], binned,  bins, thresholds)
    #     ivs.append(iv)
    #     scores.append(s1)
    #     pcd.append(pcd1)

    # iv0 = cnet.influences('LacI')
    # # pcd1 = binned.project('LacI', ['LacI', 'CI'])
    # (IVs, scores) = createIVSet('LacI', binned, cnet.influences('LacI'), bins, thresholds) 
    # (cIVs, cScores, to_remove) = combineIVs('LacI', IVs, scores, iv0,binned, bins, thresholds)
    # for i in np.setdiff1d(range(len(IVs)), to_remove):
    #     cIVs.append(IVs[i])
    #     cScores.append(scores[i])
    # print cIVs
    # print cScores
    # while len(cIVs) > 1:
    #     sorted_idx = np.argsort(-np.array(cScores)) # ranking IVs from highest scores
    #     print sorted_idx
    #     winnerId, wScore = competeIVs('LacI', cIVs[0], cIVs[-1], binned, bins, thresholds)
    #     if winnerId == 1:
    #         cIVs[0] = cIVs[-1]
    #         cScores[0] = cScores[-1]
    #     cIVs = cIVs[:-1]
    #     cScores = cScores[:-1]
    # print cIVs[0]
