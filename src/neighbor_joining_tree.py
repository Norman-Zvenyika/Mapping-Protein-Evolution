import sys
import subprocess
import numpy as np

# Function to check and install NumPy if not available
def install_numpy():
    # Check if NumPy is installed
    try:
        import numpy as np
        print("\nNumPy is already installed.")
    except ImportError:
        print("\nNumPy not found. Attempting to install NumPy...")

        # Try to install NumPy using pip
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
            print("\nNumPy installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Error while installing NumPy: {e}")
            sys.exit(1)


# Main neighbor joining function
def neighbor_joining(labels, distance_matrix, outputFile):

    # Process input and create a new distance matrix
    n, disMatrix = process_input(labels, distance_matrix)

    # Create new labels for the internal nodes
    new_labels = labels + ['U' + str(i) for i in range(1, n - 1)]

    # Run the neighbor joining algorithm
    adj = runNeighborJoining(disMatrix, n, new_labels)

    # Save the result to the specified output file
    saveResult(adj, new_labels, outputFile)


# Process input distance matrix and labels
def process_input(labels, distance_matrix):
    
    # get the number of labels
    n = len(labels)

    # Initialize an empty distance matrix
    distMatrix = [[0] * n for _ in range(n)]

    # Populate the new distance matrix with the provided values
    for i in range(n):
        for j in range(i + 1, n):
            distMatrix[i][j] = distance_matrix[j][i]
            distMatrix[j][i] = distance_matrix[j][i]
    return n, distMatrix


# Function to save the result of the neighbor-joining algorithm to a file
def saveResult(adj, labels, outputFilePath):
    with open(outputFilePath, 'w') as f:
        
        # empty set for visited nodes
        visited = set()
        
        # Write the header of the output file
        f.write("The distances between pairs of artificial and concrete nodes: \n\n")

        # Loop through adjacency list and write the distances between nodes
        for i, nodes in enumerate(adj):
            for d, w in nodes:
                if d not in visited:
                    f.write(f"{labels[d]}, {labels[i]}, {w:.5f}\n")
            visited.add(i)


# Function to run the neighbor-joining algorithm
def runNeighborJoining(disMatrix, n, new_labels):
    
    # Convert the distance matrix to a NumPy array
    D = np.array(disMatrix, dtype=float)

    # Initialize clusters and adjacency list
    clusters = [i for i in range(n)]
    adj = [[] for i in range(n)]

    # Return an empty adjacency list if the matrix has only one element
    if len(D) <= 1:
        return adj

    while True:
        # If there are only two nodes left, add the final edge and break
        if 2 == n:
            adj[len(adj) - 1].append((len(adj) - 2, D[0][1]))
            adj[len(adj) - 2].append((len(adj) - 1, D[0][1]))
            break

        # Calculate the total distance of each node to all other nodes
        totalDist = np.sum(D, axis=0)

        # Calculate the Q matrix (D1)
        D1 = (n - 2) * D
        D1 = D1 - totalDist
        D1 = D1 - totalDist.reshape((n, 1))
        np.fill_diagonal(D1, 0.0)

        # Find the indices of the minimum element in the Q matrix
        index = np.argmin(D1)
        i = index // n
        j = index % n

        # Calculate the branch lengths and new node distances
        delta = (totalDist[i] - totalDist[j]) / (n - 2)
        li = (D[i, j] + delta) / 2
        lj = (D[i, j] - delta) / 2
        d_new = (D[i, :] + D[j, :] - D[i, j]) / 2

        # Update the distance matrix with the new node
        D = np.insert(D, n, d_new, axis=0)
        d_new = np.insert(d_new, n, 0.0, axis=0)
        D = np.insert(D, n, d_new, axis=1)
        D = np.delete(D, [i, j], 0)
        D = np.delete(D, [i, j], 1)

        # Update the adjacency list with the new edges
        m = len(adj)
        adj.append([])
        adj[m].append((clusters[i], li))
        adj[clusters[i]].append((m, li))
        adj[m].append((clusters[j], lj))
        adj[clusters[j]].append((m, lj))

        # Remove the old clusters and add the new cluster
        if i < j:
            del clusters[j]
            del clusters[i]
        else:
            del clusters[i]
            del clusters[j]
        clusters.append(m)

        # Decrease the number of nodes
        n -= 1

    return adj
