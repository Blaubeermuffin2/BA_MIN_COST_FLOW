import numpy as np
from BF_shortest_path import belfor, shortest_path

# G: graph as a dict of dicts of dicts with 'capacity', 'cost', 'flow' as keys
# i.e. G[u][v]['capacity']: capacity of edge (u,v) (int)
# path: list of vertices on path (list of int)
# flow: amount of flow to send along path (int)
# returns: residual graph R after sending flow along path
def residual_graph(G, path, flow):
    # create a copy of G to work on
    R = G.copy() 

    for i in range(len(path)-1): # walk along the path
        u = path[i]
        v = path[i+1]

        # augment flow along edge (u,v)
        R[u][v]['capacity'] -= flow
        R[u][v]['flow'] += flow

        # handle residual edge (v,u)
        if u not in R[v]: # add if not present
            R[v][u] = {'capacity': flow, 'cost': -G[u][v]['cost'], 'flow': 0} 
        else:
            R[v][u]['capacity'] += flow
            R[v][u]['cost'] =- G[u][v]['cost']
   
    return R






# G: graph as a dict of dicts of dicts with 'capacity', 'cost', 'flow' as keys
# i.e. G[u][v]['capacity']: capacity of edge (u,v) (int)
# source: releasing vertex flow
# sink: absorbing vertex flow
# target_flow: amount of flow to send from source to sink (int)
# returns: total cost of flow, edges with positive flow as dict with (u,v) as keys and 
# a dict containing 'flow' and 'cost' of edge
def succ_shortest_paths(G, source, sink, target_flow):
    

    # create a copy of G to work on
    R = G.copy()
    # initialize all flows to 0
    for u in R.keys():
        for v in R[u].keys():
            R[u][v]['flow'] = 0
    
    
    flow_left = target_flow.copy()

    while flow_left != 0:


        # use Bellman-Ford to find shortest path from source to sink 
        _, predecessors = belfor(R, source)
        path = shortest_path(predecessors, source, sink)
        if path is None:
            break # No more augmenting paths


        # calculate minimal capaity of edges on path
        min_capacity = np.inf
        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]
            if min_capacity > R[u][v]['capacity']:
                min_capacity = R[u][v]['capacity']

        
        # need this minimum, because if flow_left < min_capacity, we send more flow than allowed
        delta = min(min_capacity, flow_left)

        # update residual graph by sending delta flow along a shortest path
        R = residual_graph(R, path, delta)

        flow_left -= delta
        
    # extract total cost of flow 
    # and edges sending that flow
    # from residual graph R
    # additionally, set flow in original graph G
    cost = 0
    edges_with_flow = {}
    for u in G.keys():
        for v in G[u].keys():
            # copy flow from R to G
            G[u][v]['flow'] = R[u][v]['flow']
            # add edge costs to total costs
            cost += G[u][v]['flow']*G[u][v]['cost']
            # save edges with positive flow
            if G[u][v]['flow'] > 0:
                edges_with_flow[(u,v)] = {'flow': G[u][v]['flow'], 'cost':  G[u][v]['flow']*G[u][v]['cost']}

    return cost, edges_with_flow


 

            
        