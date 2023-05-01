import subprocess
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator

# Set the ClustalW2 executable path
# Replace './clustalw2' with the path to the ClustalW2 executable on your system
clustalw2_path = './clustalw2'

# Perform multiple sequence alignment using ClustalW2
def run_clustalw2(input_file, output_file):
    command = [clustalw2_path, "-INFILE=" + input_file, "-OUTFILE=" + output_file, "-OUTPUT=FASTA"]
    subprocess.run(command, check=True)

# Generate a distance table from the aligned sequences
def generate_distance_table(alignment):
    calculator = DistanceCalculator("identity")
    distance_matrix = calculator.get_distance(alignment)
    return distance_matrix

# Load the input FASTA file
input_file = "example.fasta"

# Perform multiple sequence alignment
aligned_output_file = "aligned.fasta"
run_clustalw2(input_file, aligned_output_file)

# # Load the aligned sequences
# alignment = AlignIO.read(aligned_output_file, "fasta")

# # Generate the distance table
# distance_matrix = generate_distance_table(alignment)

# # Print the distance table
# print(distance_matrix)
