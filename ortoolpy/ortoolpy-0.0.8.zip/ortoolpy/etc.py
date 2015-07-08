def min_node_cover(g):
    import networkx
    return list(set(g.nodes()) - set(networkx.maximal_independent_set(g)))

def set_covering(n, cand, is_partition=False):
    from pulp import LpProblem, LpVariable, LpBinary, lpDot, lpSum, value
    r = range(len(cand))
    m = LpProblem()
    vv = [LpVariable('v%d'%i, cat=LpBinary) for i in r]
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

