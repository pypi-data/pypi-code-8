import pandas as pd
import numpy as np
from DataIO import read_TimeSeries

__metaclass__ = type

def read_experiments_from_files(file_list, format='csv'):
    col, dat = read_TimeSeries(file_list[0], format=format)
    d = pd.DataFrame(dat, columns = col)
    d['experiment'] = 0
    for i in range(1,len(file_list)):
        col, dat= read_TimeSeries(file_list[i], format=format)
        b = pd.DataFrame(dat, columns = col) 
        b['experiment'] = i
        d = pd.concat([d,b], ignore_index=True)
    return d

def determine_levels(data, nbins=4, bin_assignment=1):
    if bin_assignment:
        percentiles = np.arange(1,nbins) * (1. / nbins)
        levels = [data.quantile(p) for p in percentiles]
    else:
        interval = (data.max() - data.min() )  / nbins
        levels = [data.min() + i*interval for i in range(1,nbins)]
    return levels

class TimeSeriesData(pd.DataFrame):
    def __init__(self, inputfile, format='csv'):
        columns, data = read_TimeSeries(inputfile, format=format)
        super(TimeSeriesData,self).__init__(data, columns = columns)
        self.index = self['time']
    def snapshot(self,time):
        return self.loc[time]

class ExperimentSet(pd.DataFrame):
    def __init__(self,data=None):
        super(ExperimentSet,self).__init__(data=data)
        # if list_of_tsd is None:
        #     super(ExperimentSet, self).__init__(data=None)
        # elif type(list_of_tsd[0]) == str:
        #     d = read_experiments_from_files(list_of_tsd, format=format)
        #     super(ExperimentSet,self).__init__(data=d)
        # else:   # NOT WORK YET
        #     print "getting objects"
        #     d= list_of_tsd[0]
        #     d['experiment'] = 0
        #     for i in range(1,len(list_of_tsd)):
        #         b = list_of_tsd[i]
        #         b['experiment'] = i
        #         d = pd.concat([d,b], ignore_index=True)
        #     super(ExperimentSet,self).__init__(d)
    def datapoint(self,experiment, time, species):
        return self[(self['experiment'] == experiment) & (self['time'] == time)][species]
    def species(self):
        return [c for c in self.columns if c not in ('time', 'experiment')]
    def copy(self, **kwargs):
        return ExperimentSet(super(ExperimentSet,self).copy(**kwargs))
    def digitize(self,nbins=4, bin_assignment=1):
        '''bin_assignment: 1: equal data level, 0: equal spacing level'''
        # if bin_assignment:
        #     pass
        # else:
        #     pass

        digitized = self.copy()
        for sp in self.species():
            digitized[sp] = np.digitize(self[sp], determine_levels(self[sp], nbins=nbins, bin_assignment=bin_assignment) )
        return digitized
       
    def compress(experiments, digitized = False):
        binned = experiments
        if not digitized: binned = experiments.digitize()
        CD = []
        for sp in experiments.species():
            for l in np.unique(binned[sp]): 
                count = len(binned.query('%s == %s' % (sp, l)))
                count_incr = 0
                for eid in np.unique(binned['experiment']):
                    exp = binned.query('experiment == %s' % eid )
                    changed = np.zeros((len(exp),))
                    changed[:-1] = exp[sp][1:].as_matrix() - exp[sp][:-1].as_matrix()
                    incr = exp[(exp[sp] == l) & (changed > 0) ]
                    count_incr += len(incr)
                CD.append({'species' : sp, 'level': l, 'count': count, 'count_incr': count_incr } )
        c = pd.DataFrame(CD)
        c.set_index(['species', 'level'], inplace=True)
        return c

    def project(self, species, subset):
        '''Given a digitized experimental data set, count the occurences and 
number of time increasing of a species, for all the bin assignments of species
specified in 'subset'.
For example, to get projected compress data for LacI, given CI and GFP levels:

    binned = experiment_set.digitize()
    pcd_lacI = binned.project('LacI', ['CI', 'GFP'])

The result should look like this


Note that the experimental data set must be digitized before projecting.
'''
        S = np.unique(subset[:])
        levels = ( [ np.unique(self[sp]) for sp in S] )
        # subset_query = [ sp + ' == ' + str(sp_lvl) for (sp, sp_lvl) in zip(subset, subset_levels) ]
        import itertools
        level_comb = list(itertools.product(*levels))
        pcd = pd.DataFrame(level_comb, columns = S)
        pcd['count'] = 0
        pcd['count_incr'] = 0
        for i in pcd.index:
            query_str = " & ".join([ sp + ' == ' + str(pcd.loc[i,sp]) for sp in S ] )
            pcd.loc[i, 'count'] = len(self.query( query_str  ))
            pcd.loc[i, 'count_incr'] = 0
            for eid in np.unique(self['experiment']):
                exp = self.query('experiment == %s' % eid )
                changed = np.zeros((len(exp),))
                changed[:-1] = exp[species][1:].as_matrix() - exp[species][:-1].as_matrix()
                #query_str = "%s == %s & %s" % (species, levels[i], " & ".join(subset_query) )
                incr = exp[(changed > 0)].query( query_str)
                pcd.loc[i,'count_incr'] += len(incr)
            # CD.append({'level': levels[i], 'count': count, 'count_incr': count_incr } )
        #pcd.set_index(S, inplace=True)
        return pcd
