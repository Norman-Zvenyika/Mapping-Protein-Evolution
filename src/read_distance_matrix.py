import re

# Function to get the regex pattern based on user input
def get_label_pattern():
    return re.compile(r'^([^\s.]*)(\d+(\.\d+)?)?$')


# function for extracting label and row information
def process_line(line_parts, pattern, line_number):
    # Apply the pattern to the first part of line_parts
    match = pattern.match(line_parts[0])

    # If the pattern matches, extract the label and value
    if match:
        label = match.group(1)
        first_value = match.group(2) if match.group(2) else None
    else:
        label = line_parts[0]
        first_value = None

    # Initialize row
    row = []
    
    # If a value was extracted with the label, add it to the row
    if first_value:
        row.append(float(first_value))
    
    # Convert the rest of line_parts to float, ignoring invalid inputs
    for part in line_parts[1:]:
        try:
            row.append(float(part))
        except ValueError:
            continue

    return label, row

# function for parsing the distance matrix
def read_distance_matrix(file_path):
    # Get the regex pattern based on user input
    pattern = get_label_pattern()

    # Open the file and read lines
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Extract the number of lines from the first line
    num_lines = int(lines[0].strip())

    # Initialize the distance matrix as a list of lists
    matrix = []
    labels = []

    # Iterate through the lines (excluding the first line with num_lines)
    for line_number, line in enumerate(lines[1:num_lines+1], start=1):
        # Split the line by whitespace
        line_parts = line.strip().split()

        # Get the label and row information
        label, row = process_line(line_parts, pattern, line_number)

        # Append the label
        labels.append(label)

        # Append the row to the matrix
        matrix.append(row)
    
    return labels, matrix