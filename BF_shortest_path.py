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
    dists = np.array([])
    preds = np.array([])
    for _ in range(len(G)):
        dists = np.append(dists, np.inf)
        preds = np.append(preds, None)
    dists[s] = 0
    return dists, preds

# u: index of vertex u (int)
# v: index of vertex v (int)   
# weight: weight of edge (u,v) (float)
# dists: array of distances (np.array) 
# preds: array of predecessors (np.array)
# relaxes edge (u,v) if possible
def relax(u,v,weight,dists,preds):
    if dists[v] > dists[u] + weight:
        dists[v] = dists[u] + weight
        preds[v] = u

# G: graph as a dict of dicts
# s: index of start vertex (int)
# returns: distances, predecessors
# or None, None if negative cycle detected
def belfor(G,s):
    dists, preds = initialize(G,s)
    # relax all edges |V|-1 times
    for _ in range(len(G)-1):
        for u in G.keys():
            for v in G[u].keys():
                relax(u,v,G[u][v],dists,preds)

    # check for negative cycles
    for u in G.keys():
        for v in G[v].keys():
            if dists[v] > dists[u] + G[u][v]:
                return None, None
            
    return dists, preds

def shortest_path(preds,start,end):
    assert isinstance(preds, (list, np.ndarray)), "Predecessors must be a list or numpy array."
    assert start in preds, "Starting vertex not in predecessors."
    assert end in preds, "Destination vertex not in predecessors."
    
    current = end
    path = [end]
    # iteration counter to prevent infinte loop
    i = 0
    while current != start:
        current = preds[current]
        path = path + [current]
        i += 1
        if i > len(preds):
           raise Exception("Could not reach starting vertex from destination vertex. Check predecessors.")            
    
    return path[::-1]

if __name__ == "__main__":
    G = {
        0: {2: 2, 1: 2},   # 0→2 mit Kosten 2, 0→1 mit Kosten 2
        1: {2: -1},        # 1→2 mit Kosten -1
        2: {3: 3},        # 2→3 mit Kosten 3
        3: {1: 5, 0: 2},  # 3→1 mit Kosten 5, 3→0 mit Kosten 2
    }
    start = 0

    dists, preds = belfor(G,start)
    print(f"Distanzen ausgehend von {start}: {dists}")
    print(f"Kürzester Pfad von {start} nach 3:")
    print(shortest_path(preds,0,3))