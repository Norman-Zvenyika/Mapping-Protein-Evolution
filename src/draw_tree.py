# Function to parse the input lines and create a tree representation as a dictionary
def parse_input(lines):
    tree = {}
    for line in lines:
        node1, node2, _ = line.split(', ')
        
        # Add nodes to the tree dictionary if not already present
        if node1 not in tree:
            tree[node1] = []
        if node2 not in tree:
            tree[node2] = []
        
        # Add the connections between nodes
        tree[node1].append(node2)
        tree[node2].append(node1)
    return tree
    

# Function to find the root of the tree
def find_root(tree):
    for node, children in tree.items():
        
        # The root node will have more than one child
        if len(children) > 1:
            return node


# Function to read input file, skipping the first two lines
def read_input_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [line.strip() for line in lines[2:]]


# Function to save the tree to a file, with proper formatting
def save_tree_to_file(tree, node, depth, visited, output_file, is_sibling=False):
    visited.add(node)
    
    # Write the node with the correct padding, depending on its depth in the tree
    if depth > 0:
        padding = "  " * (depth - 1)
        if is_sibling:
            output_file.write(padding + "|" + "\n")
            output_file.write(padding + "+--" + node + "\n")
        else:
            output_file.write(padding + "+--" + node + "\n")
    else:
        output_file.write(node + "\n")
    
    # Recursively call the function for all unvisited children of the node
    children = [child for child in tree[node] if child not in visited]
    for i, child in enumerate(children):
        save_tree_to_file(tree, child, depth + 1, visited, output_file, i < len(children) - 1)


# Main function to draw the tree from an input file and save it to an output file
def draw_tree(input_path, output_path):
    input_lines = read_input_file(input_path)
    tree = parse_input(input_lines)
    root = find_root(tree)
    
    # Save the tree to the output file
    with open(output_path, "w") as output_file:
        output_file.write("The tree generated is shown below: \n\n")
        save_tree_to_file(tree, root, 0, set(), output_file)