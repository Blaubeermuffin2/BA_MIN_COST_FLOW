import numpy as np
from BF_shortest_path import belfor, shortest_path

def residual_graph(G, path, flow):
    R = G.copy()
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        R[u][v]['capacity'] -= flow
        if R[u][v]['capacity'] == 0:
            del R[u][v]
        else:
            R[u][v]['flow'] += flow
        
        R[v][u] = {'capacity': flow, 'cost': -G[u][v]['cost'], 'flow': 0} #Was ist der flow an der Residualkante?
    return R






# G: graph as a dict of dicts of dicts with 'capacity', 'cost', 'flow' as keys
# i.e. G[u][v]['capacity']: capacity of edge (u,v) (int)
def succ_shortest_paths(G, source, sink, target_flow):
    
    # Initialization:
    R = G.copy()
    for u in R.keys():
        for v in R[u].keys():
            R[u][v]['flow'] = 0
    source_potential = target_flow.copy()
    sink_potential = -target_flow.copy()

    while source_potential != 0 or sink_potential != 0:

        _, predecessors = belfor(R, source)
        path = shortest_path(predecessors, source, sink)
        if path is None:
            break # No more augmenting paths
        
        min_capacity = np.inf
        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            if min_capacity > R[u][v]['capacity']:
                min_capacity = R[u][v]['capacity']

        R = residual_graph(R, path, min(min_capacity, source_potential, -sink_potential))
            
        