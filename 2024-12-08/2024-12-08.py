from copy import deepcopy

input_file = "2024-12-08_task.txt"

def read_matrix_from_file(file_path):
    matrix = []
    char_positions = {}

    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            matrix.append([x for x in line.strip()])
            for col, char in enumerate(line.strip()):
                if char.isalnum():
                    if char not in char_positions:
                        char_positions[char] = []
                    char_positions[char].append((row, col))

    return matrix, char_positions

def get_antinodes(a, b, leny, lenx):
    y1 = a[0]
    y2 = b[0]
    x1 = a[1]
    x2 = b[1]
    dy = y1-y2
    dx = x1-x2
    result = []
    if (y1 + dy) >= 0 and (y1 + dy < leny) and (x1 + dx) >= 0 and (x1 + dx < lenx):
        result.append((y1+dy, x1+dx))
    if (y2 - dy) >= 0 and (y2 - dy < leny) and (x2 - dx) >= 0 and (x2 - dx < lenx):
        result.append((y2-dy, x2-dx))
    return result

def get_antinodes_task2(a, b, leny, lenx):
    y1 = a[0]
    y2 = b[0]
    x1 = a[1]
    x2 = b[1]
    dy = y1-y2
    dx = x1-x2
    result = []
    while (y1) >= 0 and (y1 < leny) and (x1) >= 0 and (x1 < lenx):
        result.append((y1, x1))
        y1 += dy
        x1 += dx
    while (y2) >= 0 and (y2 < leny) and (x2) >= 0 and (x2 < lenx):
        result.append((y2, x2))
        y2 -= dy
        x2 -= dx
    return result

def pretty_print(matrix):
    for i in range(len(matrix)):
        print("".join([x for x in matrix[i]]))

if __name__ == "__main__":
    matrix, char_positions = read_matrix_from_file(input_file)
    matrix2 = deepcopy(matrix)

    print(matrix)

    antinodes = {}
    antinodes_task2 = {}

    all_antinodes = set([])
    all_antinodes_task2 = set([])
    leny = len(matrix)
    lenx = len(matrix[0])
    for char in char_positions:
        antinodes[char] = []
        antinodes_task2[char] = []
        for i in range(len(char_positions[char])):
            for j in range(i+1, len(char_positions[char])):
                newantinodes = get_antinodes(char_positions[char][i], char_positions[char][j], leny, lenx)
                antinodes[char] += newantinodes
                all_antinodes = all_antinodes.union ({(x,y) for x,y in newantinodes})

                newantinodes_task2 = get_antinodes_task2(char_positions[char][i], char_positions[char][j], leny, lenx)
                antinodes_task2[char] += newantinodes_task2
                all_antinodes_task2 = all_antinodes_task2.union({(x, y) for x, y in newantinodes_task2})

                # just to be able print the board:
                for x in newantinodes:
                    if matrix2[x[0]][x[1]] == ".":
                        matrix2[x[0]][x[1]] = '#'

    # pretty_print(matrix2)
    print(f"Task 1: {len(all_antinodes)}")
    print(f"Task 2: {len(all_antinodes_task2)}")