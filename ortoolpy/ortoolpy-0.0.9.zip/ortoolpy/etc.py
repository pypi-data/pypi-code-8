# coding: utf-8
"""
Copyright: Saito Tsutomu
License: Python Software Foundation License
"""
from __future__ import print_function, division
from pulp import *

def addvar(lowBound=0, var_count=[0], *args, **kwargs):
    """変数作成"""
    var_count[0] += 1
    return LpVariable('v%d' % var_count[0], lowBound=lowBound, *args, **kwargs)

def min_node_cover(g):
    import networkx
    return list(set(g.nodes()) - set(networkx.maximal_independent_set(g)))

def set_covering(n, cand, is_partition=False):
    m = LpProblem()
    vv = [addvar(cat=LpBinary) for c in cand]
    m += lpDot([w for w, c in cand], vv) # obj func
    ee = [[] for j in range(n)]
    for v, (w, c) in zip(vv, cand):
        for k in c: ee[k].append(v)
    for e in ee:
        if e:
            if is_partition:
                m += lpSum(e) == 1
            else:
                m += lpSum(e) >= 1
    if m.solve() != 1: return None
    return [i for i, v in enumerate(vv) if value(v) > 0.5]

def set_partition(n, cand):
    return set_covering(n, cand, True)

def binpacking(c, w):
    """
    列生成法
        ビンパッキング問題を解く
    入力
        c: ビンの大きさ
        w: 荷物の大きさのリスト
    出力
        ビンごとの荷物の大きさリスト
    """
    n = len(w)
    rn = range(n)
    mkp = LpProblem('knapsack', LpMaximize) # 子問題
    mkpva = [addvar(cat=LpBinary) for i in rn]
    mkp.addConstraint(lpDot(w, mkpva) <= c)
    mdl = LpProblem('dual', LpMaximize) # 双対問題
    mdlva = [addvar() for i in rn]
    for i, v in enumerate(mdlva): v.w = w[i]
    mdl.setObjective(lpSum(mdlva))
    for i in rn:
        mdl.addConstraint(mdlva[i] <= 1)
    while True:
        mdl.solve()
        mkp.setObjective(lpDot([value(v) for v in mdlva], mkpva))
        mkp.solve()
        if mkp.status != 1 or value(mkp.objective) < 1 + 1e-6: break
        mdl.addConstraint(lpDot([value(v) for v in mkpva], mdlva) <= 1)
    nwm = LpProblem('primal', LpMinimize) # 主問題
    nm = len(mdl.constraints)
    rm = range(nm)
    nwmva = [addvar(cat=LpBinary) for i in rm]
    nwm.setObjective(lpSum(nwmva))
    dict = {}
    for v, q in mdl.objective.items():
        dict[v] = LpAffineExpression() >= q
    const = list(mdl.constraints.values())
    for i, q in enumerate(const):
        for v in q:
            dict[v].addterm(nwmva[i], 1)
    for q in dict.values(): nwm.addConstraint(q)
    nwm.solve()
    if nwm.status != 1: return None
    result = [[] for i in range(len(const))]
    for i, va in enumerate(nwmva):
        if value(va) < 0.5: continue
        for v in const[i]: result[i].append(v.w)
    return [r for r in result if r]