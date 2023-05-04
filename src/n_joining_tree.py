import sys
import numpy as np

def neighbor_joining(labels, distance_matrix, outputFile):
    n, disMatrix = process_input(labels, distance_matrix)
    new_labels = labels + ['U' + str(i) for i in range(1, n - 1)]
    adj = runNeighborJoining(disMatrix, n, new_labels)
    saveResult(adj, new_labels,outputFile)

def process_input(labels, distance_matrix):
    n = len(labels)
    distMatrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            distMatrix[i][j] = distance_matrix[j][i]
            distMatrix[j][i] = distance_matrix[j][i]
    return n, distMatrix

def saveResult(adj, labels, outputFilePath):
    with open(outputFilePath, 'w') as f:
        visited = set()
        f.write("distances between pairs of artificial and concrete nodes: \n")
        for i, nodes in enumerate(adj):
            for d, w in nodes:
                if d not in visited:
                    f.write(f"{labels[d]}, {labels[i]}, {w:.1f}\n")
            visited.add(i)

    
def printGraph(adj, labels):
    visited = set()
    for i, nodes in enumerate(adj):
        for d, w in nodes:
            if d not in visited:
                print(f"{labels[d]}, {labels[i]}, {w:.1f}")
        visited.add(i)

def runNeighborJoining(disMatrix, n, new_labels):
    D = np.array(disMatrix, dtype=float)
    clusters = [i for i in range(n)]
    adj = [[] for i in range(n)]
    if len(D) <= 1:
        return adj
    while True:
        if 2 == n:
            adj[len(adj) - 1].append((len(adj) - 2, D[0][1]))
            adj[len(adj) - 2].append((len(adj) - 1, D[0][1]))
            break
        totalDist = np.sum(D, axis=0)
        D1 = (n - 2) * D
        D1 = D1 - totalDist
        D1 = D1 - totalDist.reshape((n, 1))
        np.fill_diagonal(D1, 0.0)
        # print(D1)
        index = np.argmin(D1)
        i = index // n
        j = index % n
        delta = (totalDist[i] - totalDist[j]) / (n - 2)
        li = (D[i, j] + delta) / 2
        lj = (D[i, j] - delta) / 2
        d_new = (D[i, :] + D[j, :] - D[i, j]) / 2
        D = np.insert(D, n, d_new, axis=0)
        d_new = np.insert(d_new, n, 0.0, axis=0)
        D = np.insert(D, n, d_new, axis=1)
        D = np.delete(D, [i, j], 0)
        D = np.delete(D, [i, j], 1)
        # print(D)

        m = len(adj)
        adj.append([])
        adj[m].append((clusters[i], li))
        adj[clusters[i]].append((m, li))
        adj[m].append((clusters[j], lj))
        adj[clusters[j]].append((m, lj))
        if i < j:
            del clusters[j]
            del clusters[i]
        else:
            del clusters[i]
            del clusters[j]
        clusters.append(m)

        n -= 1

    return adj
