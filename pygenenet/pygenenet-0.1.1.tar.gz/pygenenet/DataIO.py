import numpy as np
import pandas as pd

from graphviz import Digraph

def read_TimeSeries(inputfile, format='csv'):
    if format=='csv':
        return pd.read_csv(inputfile,sep='\t')
    elif format=='sequential':
        a = open(inputfile, 'r').read()
        if (a[0:2] == '((' and a[-1] == ')'):
            a = a[1:-1]
        h1 = a[a.find('(') + 1: a.find(')')].split(',')
        headers = [h.strip('"') for h in h1]
        a = a[ a.find('(', a.find(')')) :]
        a = a.strip('()')
        dat = a.split('),(')
        dat = [ s.split(',') for s in dat]
        m = np.array(dat, dtype=float)
        # tab = np.fromregex(inputfile, ("\(" + "(\d+),\W+"*(len(headers)) + "\)") , dtype= ([float]*len(headers)) )
        return (headers, m)

def draw_graph(causal_network, outfile='network.gv', view=False):
    g = Digraph('G', filename=outfile)
    for c in causal_network.columns:
        for i in causal_network.index:
            if causal_network.at[i,c] == 1: g.edge(c,i, arrowhead="vee")
            elif causal_network.at[i,c] == -1: g.edge(c,i, arrowhead="tee")
    g.render(outfile, view=view)

if __name__ == '__main__':
    h, a = read_TimeSeries('../test_data/prob1/run-1.tsd', format='sequential')
