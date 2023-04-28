from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

# Read the aligned sequences
alignment = AlignIO.read("clustalW2Output/aligned.fasta", "fasta")

# Calculate the distance matrix
calculator = DistanceCalculator("identity")
distance_matrix = calculator.get_distance(alignment)

# Extract the names of the sequences
sequence_names = distance_matrix.names

# Create a nested list to store the distance table
distance_table = [['   \t\t' for _ in range(len(sequence_names) + 1)] for _ in range(len(sequence_names) + 1)]

# Fill the distance table with the sequence names and distances
for i, name1 in enumerate(sequence_names):
    distance_table[i + 1][0] = name1.ljust(10)
    distance_table[0][i + 1] = name1.ljust(10)
    for j, name2 in enumerate(sequence_names):
        distance_table[i + 1][j + 1] = '{:.8f}'.format(distance_matrix[name1, name2]).rjust(10)

# Save the distance table to a file
with open("clustalW2Output/distance_table.txt", "w") as f:
    for row in distance_table:
        f.write(' \t\t\t'.join(map(str, row)))
        f.write('\n')
