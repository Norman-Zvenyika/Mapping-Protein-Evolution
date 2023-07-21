import os
from read_distance_matrix import *
from upgma import *
from neighbor_joining_tree import *
from nj_draw_tree import *
from upgma_draw_tree import *
import subprocess


# display possible file input in data and allow the user to choose
def getInputFile(dataDirectory):
    # List all files in the data directory
    files = [f for f in os.listdir(dataDirectory) if os.path.isfile(os.path.join(dataDirectory, f))]
    
    # If there are no files in the directory, print a message and return None
    if len(files) == 0:
        print("No files found in the data directory.")
        return None

    # Print the list of available files in the data directory
    print("Available files in the data directory:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")

    # Initialize the selected_file variable to None
    selected_file = None
    print("\n")
    
    # Keep prompting the user for input until a valid file is selected
    while selected_file is None:
        try:
            # Get the user's choice as an integer
            choice = int(input("Enter the number corresponding to the input file you want to use: "))
            
            # If the choice is within the valid range, set the selected_file variable
            if 1 <= choice <= len(files):
                selected_file = files[choice - 1]
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Return the full path to the selected input document
    return os.path.join(dataDirectory, selected_file)


# main method
def main():
    # Get the path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the path to the data directory relative to the script directory
    # input_data_dir = os.path.join(script_dir, '..', 'clustalW2Output')
    input_data_dir = os.path.join(script_dir, '..', 'data')

    # Set the directory name relative to the current directory
    output_dir_name = os.path.join(script_dir, '..', 'results')

    # Set file to the output file
    nj_output_file_name = "nj_distances_between_nodes.txt"
    upgma_output_file_name = "upgma_nodes_and_heights.txt"
    nj_tree_output_file_name = "njtree.txt"
    upgma_tree_output_file_name = "upgmatree.txt"
    matrix_output_file_name = "distance_matrix.txt"

    # set path to the output file
    nj_output_file_path = os.path.join(output_dir_name,nj_output_file_name)
    upgma_output_file_path = os.path.join(output_dir_name,upgma_output_file_name)
    nj_tree_output_file_path = os.path.join(output_dir_name,nj_tree_output_file_name)
    upgma_tree_output_file_path = os.path.join(output_dir_name,upgma_tree_output_file_name)
    distance_matrix_output_file_path = os.path.join(output_dir_name,matrix_output_file_name)

    try:
        # Prompt the user for the file name
        print("\nEnter the name of file from clustalW output (see example titled \"example_clustalw.output\" in the data directory)\n")
        input_file_clustalW = getInputFile(input_data_dir) 
        
        if input_file_clustalW is not None:

            # generate the distance matrix
            script_path = os.path.join(script_dir, 'clustal2Matrix.py')

            print("\nGenerating the distance matrix........\n")
            subprocess.run(['python3', script_path, input_file_clustalW, distance_matrix_output_file_path])

            # get the distance matrix generated
            input_file_path = distance_matrix_output_file_path

            # if valid file input selected
            if input_file_path is not None:
                from copy import deepcopy
                
                # read the distance matrix
                print("\nParsing the distance matrix........")
                labels, matrix = read_distance_matrix(input_file_path)

                # Create a copy of the labels list
                upgma_labels = labels.copy() 

                # Create a deep copy of the matrix 
                upgma_matrix = deepcopy(matrix)  
                
                # generate nodes and their respective heights
                print("\nRunning the upgma algorithm........")
                upgma(upgma_labels, upgma_matrix, upgma_output_file_path)

                # drwa the upgma tree representation using the newick format
                print("\nDrawing the upgma tree........")
                upgma_draw_tree(upgma_output_file_path, upgma_tree_output_file_path)

                # Call the install_numpy function to ensure NumPy is installed
                install_numpy()

                # build a Neighbor Joining tree
                print("\nRunning the neighbor join algorithm........")
                neighbor_joining(labels,matrix,nj_output_file_path)

                # build a tree illustration
                print("\nDrawing the tree using the neighbor joining algorithm output........")
                nj_draw_tree(nj_output_file_path, nj_tree_output_file_path)

                print("\nDone\n")

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")

if __name__ == '__main__':
    main()