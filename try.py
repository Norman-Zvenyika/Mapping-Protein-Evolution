import copy

table = [
    [' ', 'A', 'B', 'C', 'D'],
    ['A', None, 2.0, 2.0, 2.0],
    ['B', None, None, 3.0, 2.0],
    ['C', None, None, None, 2.0],
    ['D', None, None, None, None]
]

# Create leaf nodes for each element in the matrix
leaf_nodes = []
for i in range(1, len(table)):
    leaf_nodes.append({'name': table[i][0], 'distance': 0})

# Compute the pairwise distances between all pairs of leaf nodes
distances = copy.deepcopy(table)
for i in range(len(leaf_nodes)):
    for j in range(i+1, len(leaf_nodes)):
        distances[i+1][j+1] = distances[j+1][i+1] = leaf_nodes[i]['distance'] + leaf_nodes[j]['distance'] + table[i+1][j+1]

# Build the tree using the UPGMA algorithm
nodes = copy.deepcopy(leaf_nodes)
while len(nodes) > 1:
    # Find the pair of nodes with the smallest distance
    min_distance = float('inf')
    min_i, min_j = None, None
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if distances[i+1][j+1] < min_distance:
                min_distance = distances[i+1][j+1]
                min_i, min_j = i, j
    # Create a new node as their parent
    new_node = {'name': f"({nodes[min_i]['name']},{nodes[min_j]['name']})", 'distance': min_distance/2}
    # Compute the distances from the new node to all other nodes
    new_distances = []
    for i in range(len(nodes)):
        if i not in (min_i, min_j):
            new_distances.append((distances[min_i+1][i+1] + distances[min_j+1][i+1]) / 2)
    new_distances.append(0)
    for i in range(len(distances)):
        if i not in (min_i+1, min_j+1):
            new_distances.insert(i, (distances[min_i+1][i] + distances[min_j+1][i]) / 2)
    # Remove the two nodes from the list of leaf nodes and add the new node
    nodes.pop(max(min_i, min_j))
    nodes.pop(min(min_i, min_j))
    nodes.append(new_node)
    # Update the distance matrix
    distances = []
    for i in range(len(new_distances)):
        distances.append([table[i][0]] + [new_distances[i] if j in (i, len(new_distances)-1) else None for j in range(1, len(new_distances)+1)])

# Print the final UPGMA tree
print(nodes[0]['name'])
