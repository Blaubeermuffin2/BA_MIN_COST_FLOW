import numpy as np

# G: graph as a dict of dicts
# returns: minimum mean weigth, cycle path or (None, None) if no cycles
def min_mean_cycle(G):
    assert isinstance(G, dict), "Graph must be a dictionary of dictionaries."
    assert all(isinstance(v, dict) for v in G.values()), "Graph must be a dictionary of dictionaries."

    # Initialize distance and predecessor tables as 2D arrays
    n = len(G)
    distances = np.full((n, n + 1), np.inf)
    predecessors = np.full((n, n + 1), None) 
    for k in range(n):
        distances[k][0] = 0

    # Fill distance and predecessor tables
    for k in range(1, n + 1):
        for u in G.keys():
            for v in G[u].keys():
                # Relax edge (u,v) for step k
                if distances[v][k] > distances[u][k - 1] + G[u][v]:
                    distances[v][k] = distances[u][k - 1] + G[u][v]
                    predecessors[v][k] = u
    # If no cycle found
    if distances[:, n].min() == np.inf:
        return None, None
    
    # Compute minimum mean cycle and store vertex
    min_mean = np.inf
    cycle_vertex = None
    for v in range(n):
        curr_max = -np.inf
        for k in range(n):
            if distances[v][k] == np.inf:
                continue
            # average weight of cycle
            mean = (distances[v][n] - distances[v][k]) / (n - k)
            curr_max = max(curr_max, mean)
        
        if curr_max < min_mean:
            min_mean = curr_max
            cycle_vertex = v

    # Backtrack to find the cycle
    path = []
    visited = set()
    curr = cycle_vertex
    k = n
    while curr not in visited:
        path.append(curr)
        visited.add(curr)
        curr = predecessors[curr][k]
        k -= 1
    # Zyklus extrahieren
    cycle_start = path.index(curr)
    cycle_path = path[cycle_start:]

    return min_mean, cycle_path[::-1] # reverse path since we built it backwards

if __name__ == "__main__":
    # Example graph
    G = {
        0: {2: 10, 1: 1},
        1: {2: 3},
        2: {3: 2},
        3: {1: 0, 0: 8}
    }
    result, cycle_path = min_mean_cycle(G)
    if result is not None and cycle_path:
        print(f"Minimum mean cycle weight: {result}")
        print(f"Cycle path: {cycle_path}")
    else:
        print("No cycles in the graph.")