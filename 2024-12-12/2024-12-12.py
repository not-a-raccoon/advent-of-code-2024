input_file = "2024-12-12_task.txt"

def read_input_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            matrix.append([(x, False) for x in line.strip()])
    return matrix


directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def walk(matrix, x, y, previous_step):
    v, visited = matrix[y][x]
    assert not visited
    matrix[y][x] = (v, True)
    print(f"Visiting field at ({x},{y}) with value {v}.")

    fences = 0
    sides = 0
    area = 1
    for d in directions:
        dx, dy = d
        if 0 <= x + dx < len(matrix[0]) and 0 <= y + dy < len(matrix):
            if matrix[y + dy][x + dx][0] != matrix[y][x][0]:
                # border fence
                fences += 1
                sides += 1 if not(previous_step == "horizontally" and dx == 0) and not(previous_step == "vertically" and dy == 0) else 0
            elif not matrix[y + dy][x + dx][1]:
                f, s, a = walk(matrix, x + dx, y + dy, "horizontally" if dy == 0 else "vertically")
                fences += f
                sides += s
                area += a
            else:
                # neighbouring field of same value has already been visited & counted
                pass
        else:
            fences += 1 # border fence at matrix boundary
            sides += 1 if not (previous_step == "horizontally" and dx == 0) and not (
                        previous_step == "vertically" and dy == 0) else 0
    return fences, sides, area


if __name__ == '__main__':
    matrix = read_input_file(input_file)
    result_fences = 0
    result_sides = 0
    result_area = 0
    result_price_task1 = 0
    result_price_task2 = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if not matrix[i][j][1]:
                f, s, a = walk(matrix, j, i, "none")
                print(f"Field at ({j},{i}) with value {matrix[i][j][0]} has {f} fences, {s} sides and area {a}.")
                result_fences += f
                result_sides += s
                result_area += a
                result_price_task1 += a*f
                result_price_task2 += a*s
    print(f"Task 1: {result_fences} fences are needed, enclosing area {result_area}, with total price {result_price_task1}.")
    print(f"Task 2: {result_fences} fences are needed, enclosing area {result_area}, with total price {result_price_task2}.")