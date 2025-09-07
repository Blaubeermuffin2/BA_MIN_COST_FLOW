import numpy as np
import pandas as pd

# G: dict
# returns: new Graph with vertices renamed to 0,1,...,n-1 and the mapping dict
def rename_vertices(G):
    mapping = {}
    for i, v in enumerate(G.keys()):
        mapping[v] = i
    new_G = {}
    for v in G.keys():
        new_v = mapping[v]
        new_G[new_v] = {}
        for u in G[v].keys():
            new_u = mapping[u]
            new_G[new_v][new_u] = G[v][u]
    return new_G, mapping

# G: dict
# s: index of start vertex (int)
# returns: dists, preds
def initialize(G,s):
    dists = np.array()
    preds = np.array()
    for _ in range(len(G)):
        dists.append(np.inf)
        preds.append(None)
    dists[s] = 0
    return dists, preds

G = {
    0: {2: 2, 1: 2},   # 0→2 mit Kosten 2, 0→1 mit Kosten 2
    1: {2: -5},        # 1→2 mit Kosten -5
    2: {3: -5},        # 2→3 mit Kosten -5
    3: {1: -5, 0: 2},  # 3→1 mit Kosten -5, 3→0 mit Kosten 2
    4: {}              # 4 hat keine ausgehenden Kanten
}