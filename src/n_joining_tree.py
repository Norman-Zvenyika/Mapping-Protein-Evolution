def insertR1(distance_matrix):
    new_column = [None] * len(matrix)
    matrix = [row + [col_value] for row, col_value in zip(matrix, new_column)]
    return matrix

def r1Values(labels, distance_matrix):
    
    # find the length of the matrix
    n = len(distance_matrix)

    dist_matrix_R1 = insertR1(distance_matrix)

    # insert an additional r1 column to the table

    #(we can modify this function so that it inserts an r1 column and return the table)

    # calculate the value of r1 for each column
    
    #example: column labelled 3MXE_A:
    (0.0 + 0.14 + 0.95 + 0.95 )/(n-2)

    # repeate this for the remaining columns

    # display the resulting table

    # return the table

def calculate_q_matrix(distance_matrix):
    n = len(distance_matrix)
    q_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i != j:
                q_matrix[i][j] = (n - 2) * distance_matrix[i][j] - sum(distance_matrix[i]) - sum(distance_matrix[j])
    return q_matrix

def find_min_q(q_matrix):
    min_q = float('inf')
    min_i = -1
    min_j = -1
    n = len(q_matrix)
    
    for i in range(n):
        for j in range(i + 1, n):
            if q_matrix[i][j] < min_q:
                min_q = q_matrix[i][j]
                min_i = i
                min_j = j
    return min_i, min_j

def update_distance_matrix(distance_matrix, min_i, min_j):
    new_row = [(distance_matrix[min_i][k] + distance_matrix[min_j][k]) / 2 for k in range(min(min_i, min_j))]

    for k in range(min(min_i, min_j) + 1, max(min_i, min_j)):
        new_row.append((distance_matrix[min_i][k] + distance_matrix[min_j][k]) / 2)

    for k in range(max(min_i, min_j) + 1, len(distance_matrix)):
        new_row.append((distance_matrix[min_i][k] + distance_matrix[min_j][k - 1]) / 2)

    distance_matrix.pop(max(min_j, min_i))
    distance_matrix.pop(min(min_j, min_i))

    for i in range(len(distance_matrix)):
        if i < min(min_i, min_j):
            distance_matrix[i].pop(max(min_i, min_j))
            distance_matrix[i].pop(min(min_i, min_j))
            distance_matrix[i].append(new_row[i])
        elif i < max(min_i, min_j):
            distance_matrix[i].pop(max(min_i, min_j))
            distance_matrix[i].append(new_row[i])
        else:
            distance_matrix[i].append(new_row[i])

    distance_matrix.append(new_row)


# function to display table during the neighbor join algorithm
def displayQTable(labels, matrix):
    new_column = [None] * len(matrix)
    matrix = [row + [col_value] for row, col_value in zip(matrix, new_column)]

    # Find the maximum width of a column
    max_width = max(len(str(value)) for row in matrix for value in row if value is not None)

    # Print the header row
    header = " " * (max_width + 4)
    for label in labels:
        header += "{:^{width}}".format(label, width=max_width + 4)
    print(header)

    # Print the table
    for row_label, row in zip(labels + ["R1"], matrix + [new_column]):
        row_str = "{:<{width}}".format(row_label, width=max_width + 4)
        for value in row:
            if value is not None:
                row_str += "{:<{width}}".format(value, width=max_width + 4)
            else:
                row_str += " " * (max_width + 4)
        print(row_str)

def neighbor_joining(labels, distance_matrix):
    nodes = labels.copy()
    n = len(labels)
    internal_nodes = n
    tree = {label: [] for label in labels}
    distances = []

    displayQTable(labels, distance_matrix)

    # while len(distance_matrix) > 2:
        # q_matrix = calculate_q_matrix(distance_matrix)
    #     min_i, min_j = find_min_q(q_matrix)
        
    #     distance_i_j = distance_matrix[min_i][min_j]
    #     new_label = f"U{internal_nodes}"
        
    #     distance_new_min_i = (distance_i_j + sum(distance_matrix[min_i]) - sum(distance_matrix[min_j])) / 2
    #     distance_new_min_j = distance_i_j - distance_new_min_i
        
    #     distances.append((nodes[min_i], new_label, distance_new_min_i))
    #     distances.append((nodes[min_j], new_label, distance_new_min_j))
        
    #     tree[nodes[min_i]].append(new_label)
    #     tree[nodes[min_j]].append(new_label)
    #     tree[new_label] = [nodes[min_i], nodes[min_j]]
        
    #     nodes.pop(min_j)
    #     nodes.pop(min_i)
    #     nodes.append(new_label)
        
    #     update_distance_matrix(distance_matrix, min_i, min_j)
    #     internal_nodes += 1

    # distances.append((nodes[0], nodes[1], distance_matrix[0][1]))
    # tree[nodes[0]].append(nodes[1])
    # tree[nodes[1]].append(nodes[0])
    
    return tree, distances