# **Phylogenetic Tree Construction**

This program constructs phylogenetic trees using UPGMA and Neighbor Joining algorithms, and generates a tree illustration based on the Neighbor Joining output.

## **Requirements**

- Python 3.6 or later
- NumPy (The program will check if NumPy is installed and attempt to install it if it's not available)

## **How the program works**

1. The user is prompted to select an input file containing ClustalW output data.
2. The program generates a distance matrix from the ClustalW alignment file.
3. The distance matrix is used as input for the UPGMA and Neighbor Joining algorithms.
4. The program outputs the distance matrix, pairs of nodes and their heights (UPGMA), distances between pairs of artificial and concrete nodes (NJ) and textual illustration of the trees in separate text files.

## **Input**

The input file should be a ClustalW alignment output file containing sequence alignment data (see `example_clustalw.output` in the `data` directory). Start by adding this file to the data directory before you run the program.

## **Output**

The program generates the following output files in the `results` directory:

1. `distance_matrix.txt` - A distance matrix generated from the ClustalW alignment input file.
2. `upgmatree.txt` - The resulting tree from the UPGMA algorithm.
3. `upgma_nodes_and_heights.txt` - specify pairs of nodes and their heights:
4. `nj_distances_between_nodes.txt` - specify distances between pairs of artificial and concrete nodes
5. `njtree.txt` - A tree illustration based on the Neighbor Joining output.

## **Running the program**

1. Ensure you have Python 3.6 or later installed on your system (Sunlab version should work).
2. In the root directory (the one with a makefile), type `make run`

