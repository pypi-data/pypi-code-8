import pandas as pd
import numpy as np
import itertools

__metaclass__ = type

def prob_incr(species, proj_compressed_data, min_occurences = 10):
    p = proj_compressed_data['count_incr']/ proj_compressed_data['count']
    p[proj_compressed_data['count'] < min_occurences] = -1
    return p

def score(species,IV, G, exp_digitized, bins, thresholds):  # G: control species set
    (v_f, v_a, v_n) = (0, 0, 0)
    IV[IV.isnull()] = 0
    if (IV == 0).all(): return thresholds['Ti']
    n_repressors = IV[IV == -1].count()
    n_activators = IV[IV == 1].count()
    # G.extend(parents(IV) )
    GG = G[:]
    GG.extend(parents(IV))
    GG = np.unique(GG)

    pcd = exp_digitized.project(species,GG)
    pcd['prob_incr'] = prob_incr(species, pcd, min_occurences = 1)
    # if (GG == ['CI','LacI']).all(): print pcd
    query_parents= ""
    if n_repressors > n_activators:
        query_parents = " & ".join(['%s == %s' %(sp,  bins[sp][0] ) for sp in IV[IV == -1].index ] )    # lowest level for repressors
        query_act = " & ".join(['%s == %s' %(sp,  bins[sp][-2])  for sp in IV[IV == 1].index ] )    # highest level for activators
        if query_act != "": query_parents += (" & " +  query_act )
    else:
        query_parents = " & ".join(['%s == %s' %(sp,  bins[sp][0] ) for sp in IV[IV == 1].index ] )    # lowest level for activators
        query_rep = " & ".join(['%s == %s' %(sp,  bins[sp][-1])  for sp in IV[IV == -1].index ] )    # highest level for repressors
        if query_rep != "": query_parents += (" & " +  query_rep)

    for g in G:
        if (len(parents(IV) == 1) and g == parents(IV)[0]):     # single-influence and self-regulating
            idx_base = pcd.query(query_parents).index
            p_base = pcd.at[idx_base[0], 'prob_incr']
            idx_test = np.setdiff1d(pcd.index, idx_base)

            if p_base != -1:
                for i in idx_test: 
                    p_a  = pcd.loc[i,'prob_incr']
                    # print "p_a / p_base = %s / %s" % (p_a, p_base)
                    if p_a != -1 :
                        if n_repressors < n_activators:
                            if (p_a / p_base) > thresholds['Ta']:   v_f += 1;   # print "Voted for"
                            elif (p_a / p_base) < thresholds['Tr']: v_a +=1;    # print "Voted against"
                            else: v_n += 1;                                     # print "Voted neutral"
                        else:
                            if (p_a / p_base) < thresholds['Tr']:  v_f += 1;    # print "Voted for"
                            elif (p_a / p_base) > thresholds['Ta']: v_a +=1;    # print "Voted against"
                            else: v_n += 1;                                     # print "Voted neutral"

        else:
            for b in bins[g]:
                query_cntl = '%s == %s' % (g,b)
                if ( g in parents(IV)):
                    query_str = query_cntl
                else:
                #p_base = float(pcd.query(query_parents+ ' & ' + query_cntl )['prob_incr'])
                    query_str = (query_parents+ ' & ' + query_cntl, query_cntl)[query_parents == ""]

                idx_base = pcd.query(query_str).index
                p_base = pcd.at[idx_base[0], 'prob_incr']
                if p_base != -1:
                    # if p_base == 0: p_base += pseudo_count
                    idx_test = np.setdiff1d(pcd.query(query_cntl).index, idx_base)
                    for i in idx_test: 
                        # pcd.loc[i, 'ratio'] = pcd.loc[i,'prob_incr'] / p_base
                        p_a  = pcd.loc[i,'prob_incr']
                        # print "p_a / p_base = %s / %s" % (p_a, p_base)
                        if p_a != -1 :
                        # print pcd.loc[idx, 'prob_incr']/ p_base
                            if n_repressors < n_activators:
                                if (p_a / p_base) > thresholds['Ta']:   v_f += 1;   # print "Voted for"
                                elif (p_a / p_base) < thresholds['Tr']: v_a +=1;    # print "Voted against"
                                else: v_n += 1;                                     # print "Voted neutral"
                            else:
                                if (p_a / p_base) < thresholds['Tr']:  v_f += 1;    # print "Voted for"
                                elif (p_a / p_base) > thresholds['Ta']: v_a +=1;    # print "Voted against"
                                else: v_n += 1;                                     # print "Voted neutral"

    # print "IV: %s" % IV
    # print (v_f, v_a, v_n)
    if (v_f + v_a + v_n == 0): return 0.
    score = (v_f - v_a + 0.) / (v_f + v_a + v_n )
    if (len(parents(IV) == 1) and g == parents(IV)[0]): score *= 0.75     # down weight single-influence and self-regulating
    return  score


def parents(infl):
    return infl[(infl.notnull()) & (infl != 0 )].index

def createIVSet(species, exp_digitized,IV0, bins, thresholds):
    I = []
    scores = []
    idx_unknown = IV0[IV0.isnull()].index    # species name
    iv = IV0.copy()
    iv[idx_unknown] = 0
    G = [species]
    score_zero = score(species,iv, G, exp_digitized, bins, thresholds)
    # print "%s \t  Background score: %s" % (list(iv), score_zero)
    for u in idx_unknown: 
        iv1 = iv.copy()
        iv1.loc[u] = 1  # set activators
        # print "scoring %s" % iv1
        score_a = score(species ,iv1, G, exp_digitized, bins, thresholds)
        # print "%s \t  Activator score: %s" % (list(iv1), score_a)
        if score_a >= score_zero: 
            I.append(iv1)
            scores.append(score_a)
        else:
            iv1.loc[u] = -1
            # print "scoring %s" % iv1
            score_r = score(species ,iv1, G, exp_digitized, bins, thresholds)
            # print "%s \t  Repressor score: %s" % (list(iv1), score_r)
            if score_r >= score_zero: 
                I.append(iv1)
                scores.append(score_r)
    return (I, scores)

    # IV[IV.isnull()] = 0

def combineIVs(species, IVs, IVscores, IV0,exp_digitized, bins, thresholds):
    '''score every possible combination of IV in input IVs'''
    I = []
    scores = []
    to_remove = [] 
    tj = len(IV0[IV0.notnull()])
    bg_score = 0.
    bg_iv = IV0.copy()
    bg_iv[IV0.isnull()] = 0
    bg_score = score(species, bg_iv, [species], exp_digitized, bins, thresholds)

    for i in range(2, min(thresholds['Tj'], len(IV0)- tj+1)):
        K = itertools.combinations(range(len(IVs)), i)
        for k in K:
            old_scores = np.zeros((len(k),))
            added = IVs[0][IV0.isnull()]; added[:] = 0  # combined vector
            for j in range(len(k)): 
                added += IVs[k[j]][IV0.isnull()] 
                old_scores[j] = IVscores[k[j]]
            new_iv = pd.concat((added , IV0[IV0.notnull()])) 
            if (max(old_scores) - min(old_scores)) <= thresholds['Tm']: 
                new_score = score(species, new_iv, [species] ,exp_digitized, bins, thresholds) 
                if ((new_score >= old_scores).all() and (new_score > bg_score)):
                    I.append(new_iv)
                    scores.append(new_score)
                    to_remove.extend(k)
    return (I, scores, set(to_remove))

def competeIVs(species, iv1, iv2, exp_digitized, bins, thresholds):
    G = [species]; G.extend(np.setdiff1d(parents(iv2), parents(iv1)) )
    s1 = score(species, iv1, G, exp_digitized, bins, thresholds)
    G = [species]; G.extend(np.setdiff1d(parents(iv1), parents(iv2)) )
    s2 = score(species, iv2, G, exp_digitized, bins, thresholds)
    if s1 > s2: return (0, s1)
    elif s1 < s2:   return  (1, s2)
    else:   return ([0, 1], [s1, s2] )
    
       
def learn(experiments, initialNetwork, thresholds = { 'Tr': 0.75, 'Ta': 1.15, 'Tj': 2, 'Ti': 0.5, 'Tm': 0.} , nbins=4, bin_assignment = 1):
    '''Learning of causal network from a set of time series data, each resulted from an independent experiment
    The algorithm learn influence vectors for one gene at a time.
    For each gene, there are 3 main stages of learning:
        (1) Adding single influence to create set of new influence vectors
        (2) Combining influence vectors from stage (1) to create  new influence vectors (with more than 1 parents)
        (3) competing between influence vectors to determine the best one

'''
    cnet = initialNetwork.copy()
    binned = experiments.digitize(nbins=nbins, bin_assignment = 1)
    bins = { sp:  np.unique(binned[sp]) for sp in initialNetwork }
    for sp in initialNetwork:
        # print "----------------------------\nLearning influence vector for %s" % sp
        initial = initialNetwork.influences(sp)
        (IVs, scores) =  createIVSet(sp,binned, initial, bins, thresholds)
        # if sp == 'LacI':
        #     print "Initial IVs"
        #     print IVs
        #     print scores
        (cIVs, cScores, to_remove) = combineIVs(sp, IVs, scores, initial,binned, bins, thresholds)
        # if sp == 'LacI':
        #     print "Combined IVs"
        #     print cIVs
        #     print cScores
        for i in np.setdiff1d(range(len(IVs)), to_remove):
            cIVs.append(IVs[i])
            cScores.append(scores[i])
        while len(cIVs) > 1:
            sorted_idx = np.argsort(-np.array(cScores)) # ranking IVs from highest scores
            winnerId, wScore = competeIVs(sp, cIVs[0], cIVs[-1], binned, bins, thresholds)
            if winnerId == 1:
                cIVs[0] = cIVs[-1]
                cScores[0] = cScores[-1]
            cIVs = cIVs[:-1]
            cScores = cScores[:-1]
        if len(cIVs) > 0: cnet.loc[sp] = cIVs[0] 
        else: 
            cnet.loc[sp] = initial.copy()
            cnet.loc[sp][initial.isnull()] = 0
           
    return cnet
            
class CausalNetwork(pd.DataFrame):
    def __init__(self, species):
        '''store influence vectors of each gene in a row, with value indicating relationship of gene in the column --> gene in the row. Example
n = CausalNetwork(...)
    A   B   C
A   0   -1  0
B   0   1   1
C   -1  None 0

0: no relation ship
1: activate
-1: repress
None: unknown
''' 
        super(CausalNetwork,self).__init__(np.zeros((len(species), len(species)), dtype=int)/ 0., columns = species, index=species)

    def activators(self,i):
        ''' return the activators of i'''
        pass
    def repressors(self,i): 
        ''' return the repressors of i'''
        pass
    def influences(self,i):
        '''return the influence vector of i'''
        return self.loc[i]
    def __getitem__(self, i):
        return self.loc[i]

