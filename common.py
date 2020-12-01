def file_to_lines(filename):
    lines = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines