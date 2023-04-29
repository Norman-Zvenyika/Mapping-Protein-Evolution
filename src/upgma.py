from read_distance_matrix import *

from collections import defaultdict

def find_min_distance(dist_matrix):
    min_value = float('inf')
    min_index = (-1, -1)

    for i in range(len(dist_matrix)):
        for j in range(len(dist_matrix)):
            if i == j:
                continue  # Skip diagonal elements
            if dist_matrix[i][j] != "-" and dist_matrix[i][j] < min_value:
                min_value = dist_matrix[i][j]
                min_index = (i, j)

    return min_index, min_value


def update_distance_matrix(dist_matrix, headers,output_file_path, i, j, new_cluster):
    for k, row in enumerate(dist_matrix):
        if k == i:
            row[j] = new_cluster
        elif k == j:
            dist_matrix[k] = [new_cluster if x == i else value for x, value in enumerate(row)]
    # write_distance_matrix(headers,dist_matrix,output_file_path,"a")



def upgma(headers, dist_matrix, output_file_path):
    clusters = {i: (headers[i], 0.0) for i in range(len(headers))}
    heights = defaultdict(float)

    while len(clusters) > 1:
        
        # find the minimum distance between the two labels
        (i, j), dist = find_min_distance(dist_matrix)

        height = dist / 2.0

        new_cluster = tuple(clusters[x] for x in (i, j))
        heights[new_cluster] = height
        print(height)
        print(new_cluster)

        update_distance_matrix(dist_matrix, headers,output_file_path, i, j, new_cluster)
        break
        
    #     # Replace None values with dashes only when calling write_distance_matrix
    #     dist_matrix_with_dashes = [['-' if x is None else x for x in row] for row in dist_matrix]
    #     write_distance_matrix(headers, dist_matrix_with_dashes, output_file_path)

    #     del clusters[j]
    #     clusters[i] = new_cluster

    # return clusters, heights






# # function for generating the upgam tree
# def upgma(matrix, headers, output_file_path):
#     clusters = [[header] for header in headers]

#     while len(clusters) > 1:
#         # Find the pair of clusters with the smallest distance
#         min_distance = float('inf')
#         min_pair = (0, 1)

#         for i in range(len(matrix)):
#             for j in range(i + 1, len(matrix[i])):
#                 if matrix[i][j] < min_distance:
#                     min_distance = matrix[i][j]
#                     min_pair = (i, j)

#         # Merge the clusters
#         i, j = min_pair
#         new_cluster = (clusters[i], clusters[j], min_distance / 2)
#         clusters.append(new_cluster)

#         # Remove the merged clusters from the list
#         clusters.pop(max(i, j))
#         clusters.pop(min(i, j))

#         # Update the distance matrix
#         new_row = []
#         for k in range(len(matrix)):
#             if k != i and k != j:
#                 new_distance = (matrix[i][k] * len(clusters[i]) + matrix[j][k] * len(clusters[j])) / (len(clusters[i]) + len(clusters[j]))
#                 new_row.append(new_distance)

#         matrix.append(new_row)
#         matrix.pop(max(i, j))
#         for row in matrix:
#             row.pop(max(i, j))
#             row.pop(min(i, j))

#         # Write the updated distance matrix to the output file
#         write_distance_matrix(headers, matrix, output_file_path, "a")

#     return clusters[0]
