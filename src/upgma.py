
# for locating the smallest cell in the table
def lowest_cell(table):
    
    # Set default to infinity
    min_cell_val = float("inf")
    x, y = -1, -1

    # Go through every cell, looking for the lowest
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] < min_cell_val:
                min_cell_val = table[i][j]
                x, y = i, j

    # Return the x, y co-ordinate of cell and the min_cell_val
    return min_cell_val, x, y


# for combining two labels in a list of labels
def join_labels(labels, a, b, height):
    
    # Swap if the indices are not ordered
    if b < a:
        a, b = b, a

    # Join the labels in the first index, together with each leg distance
    labels[a] = "(" + labels[a] + "," + labels[b] + ", " + str(height) + ")"

    # Remove the (now redundant) label in the second index
    del labels[b]


# for joining the entries of a table on the cell (a, b) by averaging their values
def join_table(table, a, b):
    
    # Swap if the indices are not ordered
    if b < a:
        a, b = b, a

    # For the lower index, reconstruct the entire row (A, i), where i < A
    row = []
    for i in range(0, a):
        row.append((table[a][i] + table[b][i])/2)
    table[a] = row
    
    # Then, reconstruct the entire column (i, A), where i > A
    #   Note: Since the matrix is lower triangular, row b only contains values for indices < b
    for i in range(a+1, b):
        table[i][a] = (table[i][a]+table[b][i])/2
        
    #   We get the rest of the values from row i
    for i in range(b+1, len(table)):
        table[i][a] = (table[i][a]+table[i][b])/2
        
        # Remove the (now redundant) second index column entry
        del table[i][b]

    # Remove the (now redundant) second index row
    del table[b]


# for running the UPGMA algorithm on a labelled table
def upgma(labels, table,upgmaResults):
    
    # Until all labels have been joined
    while len(labels) > 1:
        
        # Locate lowest cell in the table
        min_val, x, y = lowest_cell(table)

        # calculate height of the leg of each entry (x, y)
        height = min_val /2.0

        # Join the table on the cell co-ordinates
        join_table(table, x, y)

        # Update the labels accordingly
        join_labels(labels, x, y, height)


    # write to a file
    with open(upgmaResults, 'w') as upgma_file:
        upgma_file.write("The respective nodes and their heights are: \n")
        upgma_file.write(str(labels[0]) + '\n')


