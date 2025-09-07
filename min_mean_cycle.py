import numpy as np

# G: graph as a dict of dicts
# returns: minimum mean weigth, cycle path or (None, None) if no cycles
def min_mean_cycle(G):
    assert isinstance(G, dict), "Graph must be a dictionary of dictionaries."
    assert all(isinstance(v, dict) for v in G.values()), "Graph must be a dictionary of dictionaries."

    # Initialize distance and predecessor tables
    n = len(G)
    dists = np.full((n, n + 1), np.inf)
    preds = np.full((n, n + 1), None) 
    for k in range(n):
        dists[k][0] = 0

    # Fill distance and predecessor tables
    for k in range(1, n + 1):
        for u in G.keys():
            for v in G[u].keys():
                # Relax edge (u,v) for step k
                if dists[v][k] > dists[u][k - 1] + G[u][v]:
                    dists[v][k] = dists[u][k - 1] + G[u][v]
                    preds[v][k] = u

    # Compute minimum mean cycle and store vertex
    min_mean = np.inf
    cycle_vertex = None
    for v in range(n):
        for k in range(n):
            # average weight of cycle
            mean = (dists[v][n] - dists[v][k]) / (n - k)
            if mean < min_mean:
                min_mean = mean
                cycle_vertex = v

    # If no cycle found
    if min_mean == np.inf or cycle_vertex == None:
        return None, None

    # Backtrack to find the cycle
    path = []
    visited = set()
    curr = cycle_vertex
    k = n
    while curr not in visited:
        path.append(curr)
        visited.add(curr)
        curr = preds[curr][k]
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