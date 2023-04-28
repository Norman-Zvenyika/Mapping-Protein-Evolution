def read_distance_matrix(file_path):
    headers = []
    matrix = []

    with open(file_path, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            row = line.strip().split()

            if not headers:
                headers = row
                continue

            species = row[0]
            row_data = [float(x) if x != '-' else 0.0 for x in row[1:]]
            matrix.append(row_data)

    n = len(matrix)
    
    for i in range(n):
        for j in range(i + 1, n):
            if len(matrix[i]) <= j:
                matrix[i].append(matrix[j][i])
            elif len(matrix[j]) <= i:
                matrix[j].insert(i, matrix[i][j])

    return headers, matrix


def write_distance_matrix(headers, matrix, output_file_path, mode='w',table_title=None):
    with open(output_file_path, mode) as file:
        if mode == 'a':
            # Add an empty line to separate the distance matrices if appending
            file.write('\n\n')
        
        if table_title:
            file.write(table_title + '\n')

        # Write the headers (species names) to the first line
        formatted_headers = '          \t' + '\t'.join([header.ljust(10) for header in headers]) + '\n'
        file.write(formatted_headers)

        # Write the distance matrix to the remaining lines
        for idx, row in enumerate(matrix):
            # Fill in the missing values in the lower or upper triangle with "-"
            if len(row) < len(headers):
                missing_values = ['-'.ljust(10)] * idx
                complete_row = missing_values + [f"{x:.8f}".ljust(10) for x in row]
            else:
                missing_values = ['-'.ljust(10)] * (len(headers) - len(row))
                complete_row = [f"{x:.8f}".ljust(10) for x in row] + missing_values

            # Ensure that the index is within the range of headers before writing to file
            if idx < len(headers):
                file.write(headers[idx].ljust(10) + '\t'.join(complete_row) + '\n')