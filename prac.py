def insertR1(distance_matrix):
    new_column = [None] * len(distance_matrix)
    matrix = [row + [col_value] for row, col_value in zip(distance_matrix, new_column)]
    return matrix

def r1Values(labels, distance_matrix):
    n = len(distance_matrix)
    dist_matrix_R1 = insertR1(distance_matrix)

    r1_row = []

    r1_row = []
    for i in range(n):
        r1_sum = 0
        count = 0
        for j in range(n):
            if i != j:
                if i > j:
                    if dist_matrix_R1[i][j] is not None:
                        r1_sum += dist_matrix_R1[i][j]
                        count += 1
                else:
                    if dist_matrix_R1[j][i] is not None:
                        r1_sum += dist_matrix_R1[j][i]
                        count += 1
        r1_value = r1_sum / (n-2)
        r1_value_rounded = round(r1_value, 3)
        r1_row.append(r1_value_rounded)
    
    dist_matrix_R1.append(r1_row)
    displayQTable(labels,dist_matrix_R1)
    return dist_matrix_R1


def displayQTable(labels, matrix):
    max_width = max(len(str(value)) for row in matrix for value in row if value is not None)

    # Remove 'R1' from the header
    header = " " * (max_width + 4)
    for label in labels:
        header += "{:^{width}}".format(label, width=max_width + 4)
    print(header)

    for row_label, row in zip(labels, matrix):
        row_str = "{:<{width}}".format(row_label, width=max_width + 4)
        for value in row:
            if value is not None:
                row_str += "{:<{width}}".format(value, width=max_width + 4)
            else:
                row_str += " " * (max_width + 4)
        print(row_str)

    # Print the 'R1' row at the bottom
    row_str = "{:<{width}}".format("R1", width=max_width + 4)
    r1_row = matrix[-1]
    for value in r1_row:
        if value is not None:
            row_str += "{:<{width}}".format(value, width=max_width + 4)
        else:
            row_str += " " * (max_width + 4)
    print(row_str)

def displayDistanceTable(labels, matrix):
    max_width = max(len(str(value)) for row in matrix for value in row if value is not None)

    header = " " * (max_width + 4)
    for label in labels:
        header += "{:^{width}}".format(label, width=max_width + 4)
    print(header)

    for row_label, row in zip(labels, matrix):
        row_str = "{:<{width}}".format(row_label, width=max_width + 4)
        for value in row:
            if value is not None:
                row_str += "{:<{width}}".format(value, width=max_width + 4)
            else:
                row_str += " " * (max_width + 4)
        print(row_str)

def updateQTable(labels, matrix):
    r1_row = matrix[-1]
    updated_matrix = []
    for i, row in enumerate(matrix[:-1]):
        updated_row = []
        for j, value in enumerate(row):
            if value is not None:
                updated_value = value - r1_row[i] - r1_row[j]
                updated_row.append(updated_value)
            else:
                updated_row.append(None)
        updated_matrix.append(updated_row)
    return updated_matrix

def mincell(labels, matrix):
    min_value = float('inf')
    min_i = None
    min_j = None

    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value is not None and value < min_value:
                min_value = value
                min_i = i
                min_j = j

    return (labels[min_i], labels[min_j])

def finalNodes(labels, matrix):
    min_value = float('inf')
    min_i = None
    min_j = None

    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value is not None and value < min_value:
                min_value = value
                min_i = i
                min_j = j

    return (labels[min_i], labels[min_j], min_value)

def find_distance(matrix, labels, node_i, node_j):
    i, j = labels.index(node_i), labels.index(node_j)
    if i < j:
        return matrix[j][i]
    else:
        return matrix[i][j]

def calculate_branch_lengths(matrix, labels, nodes):
    node_i, node_j = nodes
    distance = find_distance(matrix, labels, node_i, node_j)
    r1_i = matrix[-1][labels.index(node_i)]
    r1_j = matrix[-1][labels.index(node_j)]

    branch_length_i = 0.5 * (distance + r1_i - r1_j)
    branch_length_j = 0.5 * (distance + r1_j - r1_i)

    return branch_length_i, branch_length_j

def update_distance_matrix(old_matrix, old_labels, new_labels, merged_nodes):
    new_matrix = []

    for i, new_label in enumerate(new_labels):
        row = []
        for j, other_new_label in enumerate(new_labels):
            if j >= i:
                row.append(None)
                continue

            if new_label in merged_nodes and other_new_label in merged_nodes:
                label_1, label_2 = merged_nodes[new_label]
                other_label_1, other_label_2 = merged_nodes[other_new_label]

                distance = (find_distance(old_matrix, old_labels, label_1, other_label_1) +
                            find_distance(old_matrix, old_labels, label_1, other_label_2) -
                            find_distance(old_matrix, old_labels, label_2, other_label_2)) / 2
            elif new_label in merged_nodes:
                label_1, label_2 = merged_nodes[new_label]

                distance = (find_distance(old_matrix, old_labels, label_1, other_new_label) +
                            find_distance(old_matrix, old_labels, label_2, other_new_label) -
                            find_distance(old_matrix, old_labels, label_1, label_2)) / 2
            elif other_new_label in merged_nodes:
                other_label_1, other_label_2 = merged_nodes[other_new_label]

                distance = (find_distance(old_matrix, old_labels, new_label, other_label_1) +
                            find_distance(old_matrix, old_labels, new_label, other_label_2) -
                            find_distance(old_matrix, old_labels, other_label_1, other_label_2)) / 2
            else:
                distance = find_distance(old_matrix, old_labels, new_label, other_new_label)

            row.append(distance)

        new_matrix.append(row)

    return new_matrix




from pprint import pprint

def print_tree(tree,branch_lengths_map):
    for node, children in tree.items():
        child1, child2 = children
        branch_length1 = branch_lengths_map[(node, child1)]
        branch_length2 = branch_lengths_map[(node, child2)]
        print(f"{child1}, {node}, {branch_length1}")
        print(f"{child2}, {node}, {branch_length2}")

def nj_tree_building(labels, distance_matrix):
    nodes_val = {}
    branch_lengths_map = {}
    internal_node_count = 1

    original_matrix = [row.copy() for row in distance_matrix]
    old_labels = labels.copy()

           
    displayDistanceTable(labels, distance_matrix)
    print("\n")

    while len(labels) > 2:

        # Calculate matrix with R1
        matrix_with_r1 = r1Values(labels, distance_matrix)
        print("\n")

        # Compute the new distance table
        updated_matrix = updateQTable(labels, matrix_with_r1)
        displayDistanceTable(labels, updated_matrix)
        print("\n")

        # Find the nodes with the minimum value in the updated matrix
        nodes = mincell(labels, updated_matrix)

        # Compute branch lengths
        branch_lengths = calculate_branch_lengths(matrix_with_r1, labels, nodes)

        # Create a hashmap to store the nodes and their corresponding values
        new_label = f"U{internal_node_count}"
        nodes_val[new_label] = nodes

        # Update the branch_lengths_map
        branch_lengths_map[(new_label, nodes[0])] = branch_lengths[0]
        branch_lengths_map[(new_label, nodes[1])] = branch_lengths[1]

        # Update labels
        new_labels = [label for label in labels if label not in nodes]
        new_labels.append(new_label)

        # Update the distance matrix
        distance_matrix = update_distance_matrix(original_matrix, old_labels, new_labels, nodes_val)

        # Update labels and internal_node_count
        labels = new_labels
        internal_node_count += 1
        displayDistanceTable(labels, distance_matrix)
        print("\n")

    # # Handle the final two nodes
    final_nodes = finalNodes(labels, distance_matrix)
    return nodes_val, branch_lengths_map, final_nodes


# Example usage:
labels = ["A", "B", "C", "D"]
distance_matrix = [[], [17], [26, 12], [27, 18, 14]]
# labels = ["3MXE_A", "3MXE_B", "3PJ6_A", "3QIN_A", "3QIO_A"]
# distance_matrix = [[], [0.0], [0.14, 0.14], [0.95, 0.95, 0.95], [0.95, 0.95, 0.95, 0.0]]
tree, branch_lengths_map,final_nodes = nj_tree_building(labels, distance_matrix)
print("Neighbor Joining Tree:")
print(f"{final_nodes[0]}, {final_nodes[1]}, {final_nodes[2]}")
print_tree(tree, branch_lengths_map)

# displayDistanceTable(labels, distance_matrix)
# print("\n")

# # calculate matrix with R1
# matrix_with_r1 = r1Values(labels, distance_matrix)
# print("\n")

# # compute the new distance table
# updated_matrix = updateQTable(labels, matrix_with_r1)
# displayDistanceTable(labels, updated_matrix)
# print("\n")
# nodes = mincell(labels,updated_matrix)


# # compute branch lengths
# branch_lengths = calculate_branch_lengths(matrix_with_r1, labels, nodes)

# # create a hashmap to store the nodes and their corresponding values
# nodes_val = {}
# new_label = "U1"
# nodes_val[new_label] = nodes

# # update labels
# new_labels = [label for label in labels if label not in nodes]
# new_labels.append(new_label)

# print("Labels:", new_labels)
# print("Branch lengths:", branch_lengths)

# print("\n")
# ups = update_distance_matrix(distance_matrix, labels, new_labels, nodes_val)
# displayDistanceTable(new_labels, ups)