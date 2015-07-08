def min_node_cover(g):
    import networkx
    return list(set(g.nodes()) - set(networkx.maximal_independent_set(g)))

