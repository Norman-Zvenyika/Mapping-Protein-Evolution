import os
from read_distance_matrix import *
from upgma import *
from n_joining_tree import *


# display possible file input in data and allow the user to choose
def getInputFile(dataDirectory):
    print("\n")
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
    input_data_dir = os.path.join(script_dir, '..', 'clustalW2Output')

    # Set the directory name relative to the current directory
    output_dir_name = os.path.join(script_dir, '..', 'results')

    # Set file to the output file
    distance_matrix_output_file_name = "distance_matrix.txt"

    # set path to the output file
    output_file_path = os.path.join(output_dir_name,distance_matrix_output_file_name)

    try:
        # Prompt the user for the file name
        input_file_path = getInputFile(input_data_dir)
        
        # if valid file input selected
        if input_file_path is not None:
            
            # read the distance matrix
            labels, matrix = read_distance_matrix(input_file_path)
            
            # # generate nodes and their respective heights
            # nodesAndHeights = upgma(labels, matrix)

            # print("\nThe respective nodes and their heights are: ")
            
            # # print the nodes
            # print(nodesAndHeights)

            # build a Neighbor Joining tree
            tree, distances = neighbor_joining(labels, matrix)

            # # Print the distances between pairs of artificial and concrete nodes
            # for dist in distances:
            #     print(f"{dist[0]}, {dist[1]}, {dist[2]}")

            # output a text illustration of the updated tree


    except FileNotFoundError:
        print(f"File not found: {input_file_path}")

if __name__ == '__main__':
    main()