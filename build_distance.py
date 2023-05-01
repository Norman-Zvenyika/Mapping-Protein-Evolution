from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

# Read the aligned sequences
alignment = AlignIO.read("clustalW2Output/aligned.fasta", "fasta")

# Calculate the distance matrix
calculator = DistanceCalculator("identity")
distance_matrix = calculator.get_distance(alignment)

# Save the distance table to a file
with open("clustalW2Output/distance_table.txt", "w") as f:
    f.write(str(distance_matrix))
