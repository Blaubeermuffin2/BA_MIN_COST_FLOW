import numpy as np
from BF_shortest_path import belfor, shortest_path

# G: graph as a dict of dicts of dicts with 'capacity', 'cost', 'flow' as keys
# i.e. G[u][v]['capacity']: capacity of edge (u,v) (int)
def succ_shortest_paths(G, source, sink, target_flow):
    
    # Initialization:
    n = len(G)
    for u in G.keys():
        for v in G[u].keys():
            G[u][v]['flow'] = 0
    b_flow = target_flow.copy()

    while b_flow != 0:

        _, predecessors = belfor(G, source)
        path = shortest_path(predecessors, source, sink)

        min_capacity = np.inf
        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            if min_capacity > G[u][v]['capacity']:
                min_capacity = G[u][v]['capacity']