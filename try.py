input_lines = [
    "U2, 3MXE_A, 0.0",
    "U2, 3MXE_B, 0.0",
    "U3, 3PJ6_A, 0.1",
    "U1, 3QIN_A, 0.0",
    "U1, 3QIO_A, 0.0",
    "U3, U1, 0.9",
    "U3, U2, 0.1",
]

def parse_input(lines):
    tree = {}
    for line in lines:
        node1, node2, _ = line.split(', ')
        if node1 not in tree:
            tree[node1] = []
        if node2 not in tree:
            tree[node2] = []
        tree[node1].append(node2)
        tree[node2].append(node1)
    return tree

def find_root(tree):
    for node, children in tree.items():
        if len(children) > 1:
            return node

def print_tree(tree, node, depth, visited, is_sibling=False):
    visited.add(node)
    if depth > 0:
        padding = "  " * (depth - 1)
        if is_sibling:
            print(padding + "|")
            print(padding + "+--" + node)
        else:
            print(padding + "+--" + node)
    else:
        print(node)
    children = [child for child in tree[node] if child not in visited]
    for i, child in enumerate(children):
        print_tree(tree, child, depth + 1, visited, i < len(children) - 1)

tree = parse_input(input_lines)
root = find_root(tree)
print_tree(tree, root, 0, set())