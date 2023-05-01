import re

# function for extracting label and row information
def process_line(line_parts):

    # Compile a regex pattern to match the label and the first float value (if any)
    pattern = re.compile(r'(\w+)\|PDB(?:([\d.]+))?$')

    # Search for the pattern in the first part of line_parts
    match = pattern.search(line_parts[0])

    # Extract the label from the match
    label = match.group(1)

    # Check if there's a float value after the "PDB" string
    if match.group(2):
        first_value = float(match.group(2))
        row = [first_value] + list(map(float, line_parts[1:]))
    else:
        row = list(map(float, line_parts[1:]))

    return label, row

# function for parsing the distance matrix
def read_distance_matrix(file_path):
    
    # open the file and read lines
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Extract the number of lines from the first line
    num_lines = int(lines[0].strip())

    # Initialize the distance matrix as a list of lists
    matrix = []
    labels = []

    # Iterate through the lines (excluding the first line with num_lines)
    for line in (lines[1:num_lines+1]):
        
        # Split the line by whitespace
        line_parts = line.strip().split()

        #get the label and row information
        label, row = process_line(line_parts)

        #append the label
        labels.append(label)

        # Append the row to the matrix
        matrix.append(row)

    return labels, matrix