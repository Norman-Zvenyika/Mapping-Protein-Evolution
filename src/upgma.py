from read_distance_matrix import *

# function for generating the upgam tree
def upgma(matrix, headers, output_file_path):
    clusters = [[header] for header in headers]

    while len(clusters) > 1:
        # Find the pair of clusters with the smallest distance
        min_distance = float('inf')
        min_pair = (0, 1)

        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix[i])):
                if matrix[i][j] < min_distance:
                    min_distance = matrix[i][j]
                    min_pair = (i, j)

        # Merge the clusters
        i, j = min_pair
        new_cluster = (clusters[i], clusters[j], min_distance / 2)
        clusters.append(new_cluster)

        # Remove the merged clusters from the list
        clusters.pop(max(i, j))
        clusters.pop(min(i, j))

        # Update the distance matrix
        new_row = []
        for k in range(len(matrix)):
            if k != i and k != j:
                new_distance = (matrix[i][k] * len(clusters[i]) + matrix[j][k] * len(clusters[j])) / (len(clusters[i]) + len(clusters[j]))
                new_row.append(new_distance)

        matrix.append(new_row)
        matrix.pop(max(i, j))
        for row in matrix:
            row.pop(max(i, j))
            row.pop(min(i, j))

        # Write the updated distance matrix to the output file
        write_distance_matrix(headers, matrix, output_file_path, "a")

    return clusters[0]
