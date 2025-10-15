import numpy as np

# ----------------------------------------------------------
# !!!!!!!!!!!!!!!!!!!! CURRENTLY UNUSED !!!!!!!!!!!!!!!!!!!!
# ----------------------------------------------------------
# G: graph as a dict of dicts
# returns: new Graph with vertices renamed to 0,1,...,n-1 and the corresponding mapping dict
def rename_vertices(G):
    # build mapping dict
    mapping = {}
    for i, v in enumerate(G.keys()): # enumerate gives (index i, value v)
        mapping[v] = i

    # build new graph with renamed vertices according to mapping
    new_G = {}
    for v in G.keys():
        new_v = mapping[v]
        new_G[new_v] = {}
        for u in G[v].keys():
            new_u = mapping[u]
            new_G[new_v][new_u] = G[v][u]

    return new_G, mapping

# # G: graph as a dict of dicts of dicts with 'capacity', 'cost', 'flow' as keys
# i.e. G[u][v]['capacity']: capacity of edge (u,v) (int)
# s: index of start vertex (int)
# returns: distances, predecessors
def initialize(G,s):
    distances = np.array([])
    predecessors = np.array([])
    # sets all distances to infinity and all predecessors to None
    for _ in range(len(G)):
        distances = np.append(distances, np.inf)
        predecessors = np.append(predecessors, None)
    distances[s] = 0
    return distances, predecessors

# u: index of vertex u (int)
# v: index of vertex v (int)   
# cost: cost of edge (u,v) (float)
# distances: array of distances (np.array) 
# predecessors: array of predecessors (np.array)
#
# relaxes edge (u,v) if possible
def relax(u, v, cost, distances, predecessors):
    if distances[v] > distances[u] + cost:
        distances[v] = distances[u] + cost
        predecessors[v] = u

# G: graph as a dict of dicts of dicts with 'capacity', 'cost', 'flow' as keys
# i.e. G[u][v]['capacity']: capacity of edge (u,v) (int)
# s: index of start vertex (int)
# returns: distances, predecessors as arrays
# or None, None if negative cycle detected
def belfor(G,s):
    distances, predecessors = initialize(G,s)
    # relax all edges |V|-1 times
    for _ in range(len(G)-1):
        for u in G.keys():
            for v in G[u].keys():
                relax(u, v, G[u][v]['cost'], distances, predecessors)

    # check for negative cycles
    for u in G.keys():
        for v in G[v].keys():
            if v not in G[u]:
                continue
            if distances[v] > distances[u] + G[u][v]['cost']:
                return None, None
            
    return distances, predecessors

# predecessors: array of predecessors (np.array or list)
# start: index of starting vertex (int)
# end: index of destination vertex (int)
# returns: list of vertices on shortest path from start to end (including start and end)
def shortest_path(predecessors,start,end):
    assert isinstance(predecessors, (list, np.ndarray)), "Predecessors must be a list or numpy array."
    assert start in predecessors, "Starting vertex not in predecessors."

    if end > len(predecessors) or predecessors[end] is None:
        return None # No path from start to end

    current = end
    path = [end]
    # iteration counter to prevent infinte loop
    i = 0
    # backtrack from end to start using predecessors
    while current != start:
        current = predecessors[current]
        path = path + [current]
        i += 1
        if i > len(predecessors):
           raise Exception("Could not reach starting vertex from destination vertex. Check predecessors.")            
    
    return path[::-1] # reverse path since we built it backwards

if __name__ == "__main__":
    G = {
        0: {2: {'flow': 0, 'capacity': 0, 'cost': 2},   # 0→2 mit Kosten 2, Flow & Kapazität 0
            1: {'flow': 0, 'capacity': 0, 'cost': 2}},  # 0→1 mit Kosten 2, Flow & Kapazität 0
        1: {2: {'flow': 0, 'capacity': 0, 'cost': -1}}, # 1→2 mit Kosten -1, Flow & Kapazität 0
        2: {3: {'flow': 0, 'capacity': 0, 'cost': 3}},  # 2→3 mit Kosten 3, Flow & Kapazität 0
        3: {1: {'flow': 0, 'capacity': 0, 'cost': 5},   # 3→1 mit Kosten 5, Flow & Kapazität 0
            0: {'flow': 0, 'capacity': 0, 'cost': 2}},  # 3→0 mit Kosten 2, Flow & Kapazität 0
    }
    start = 0

    distances, predecessors = belfor(G,start)
    print(f"Distanzen ausgehend von {start}: {distances}")
    print(f"Kürzester Pfad von {start} nach 3:")
    print(shortest_path(predecessors,0,3))