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

# def find_distance_1(matrix, labels, node_i, node_j):
#     if isinstance(node_i, tuple):
#         distance = 0
#         for i in range(len(node_i)):
#             distance += find_distance(matrix, labels, node_i[i], node_j[i])
#         return distance / len(node_i)
#     else:
#         i, j = labels.index(node_i), labels.index(node_j)
#         if i > j:
#             i, j = j, i
#         return matrix[j][i]

def update_distance_matrix(old_matrix, old_labels, new_labels, merged_nodes):
    new_matrix = []

    for new_label in new_labels:
        row = []
        for other_new_label in new_labels:
            if new_label == other_new_label:
                row.append(None)
                continue

            if new_label == merged_nodes[0] or new_label == merged_nodes[1]:
                label_1, label_2 = merged_nodes
            else:
                label_1, label_2 = new_label, new_label

            if other_new_label == merged_nodes[0] or other_new_label == merged_nodes[1]:
                other_label_1, other_label_2 = merged_nodes
            else:
                other_label_1, other_label_2 = other_new_label, other_new_label

            distance = (find_distance(old_matrix, old_labels, label_1, other_label_1) +
                        find_distance(old_matrix, old_labels, label_1, other_label_2) -
                        find_distance(old_matrix, old_labels, label_2, other_label_2))
            row.append(distance)

        new_matrix.append(row)

    return new_matrix

# Example usage:
labels = ["3MXE_A", "3MXE_B", "3PJ6_A", "3QIN_A", "3QIO_A"]
distance_matrix = [[], [0.0], [0.14, 0.14], [0.95, 0.95, 0.95], [0.95, 0.95, 0.95, 0.0]]
displayDistanceTable(labels, distance_matrix)
print("\n")

# calculate matrix with R1
matrix_with_r1 = r1Values(labels, distance_matrix)
print("\n")

# compute the new distance table
updated_matrix = updateQTable(labels, matrix_with_r1)
displayDistanceTable(labels, updated_matrix)
print("\n")
nodes = mincell(labels,updated_matrix)
print("The nodes are: ")
print(nodes)

# compute branch lengths
branch_lengths = calculate_branch_lengths(matrix_with_r1, labels, nodes)

# merge lables
merged_label = nodes[0] + " - " + nodes[1]

# update labels
new_labels = [label for label in labels if label not in nodes]
new_labels.append(merged_label)

print("Labels:", new_labels)
print("Branch lengths:", branch_lengths)

print("\n")
ups = update_distance_matrix(distance_matrix, labels, new_labels, nodes)
displayDistanceTable(new_labels, ups)

# recreate an updated matrix using new labels, and old matrix values
# use the 
# for eaxmple, use the old matrix to find the distance between 3MXEA and 3MXE_B and all other values. Remember, the 
# diagonal (3MXEA, 3MXEA) should be left as None. 
# to find the distance between 3MXEA and ('3QIO_A', '3QIN_A'), we use the old distance matrix formula:
# d(('3QIO_A', '3QIN_A') and 3MXEA) = d(3MXEA, '3QIO_A') + d(3MXEA, '3QIN_A') - d('3QIO_A', '3QIN_A'))
# this function should return a distance marix using the new labels.