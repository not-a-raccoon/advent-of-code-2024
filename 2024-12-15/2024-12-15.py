input_file = "2024-12-15_task.txt"


def read_input_file(file_path, task2=False):
    matrix = []
    moves = []
    reading_moves = False
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            if not reading_moves:
                s = line.strip()
                if task2:
                    s = s.replace("O", "[]")
                    s = s.replace("#", "##")
                    s = s.replace(".", "..")
                    s = s.replace("@", "@.")
                matrix.append([x for x in s])
                if line.strip() == "":
                    reading_moves = True
            else:
                moves = moves + [x for x in line.strip()]
    return matrix, moves


directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
directions_map = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}


def get_robot(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "@":
                return (j, i)
    assert False


# Obsolete code for task 1:
def find_next_empty_field(matrix, x, y, dx, dy):
    while 0 <= x + dx < len(matrix[0]) and 0 <= y + dy < len(matrix):
        if matrix[y + dy][x + dx] == ".":
            # free space
            return x + dx, y + dy
        elif matrix[y + dy][x + dx] == "#":
            # boundary marker
            break
        x += dx
        y += dy
    return None, None


# Obsolete code for task 1:
def do_push(matrix, x, y, direction):
    assert 0 <= x < len(matrix[0]) and 0 <= y < len(matrix)
    d = directions_map[direction]
    dy, dx = d
    # Check if there is an empty field in the given direction:
    ex, ey = find_next_empty_field(matrix, x, y, dx, dy)
    cx, cy = ex, ey
    if ex is not None:
        while True:
            assert matrix[cy][cx] != "#"

            matrix[cy][cx] = matrix[cy - dy][cx - dx]

            cy -= dy
            cx -= dx
            if (cy, cx) == (y, x):
                matrix[cy][cx] = "."
                break

        # x, y keeps track of the robot's ("@" symbol) coordinates:
        x += dx
        y += dy
    return x, y


def can_move_task2(matrix, x, y, direction):
    # Can object at coordinate (y,x) be moved 1 step in "direction"?
    d = directions_map[direction]
    dy, dx = d

    if not (0 <= x + dx < len(matrix[0]) and 0 <= y + dy < len(matrix)):
        return False
    elif matrix[y + dy][x + dx] == ".":
        return True
    elif matrix[y + dy][x + dx] == "#":
        return False
    elif matrix[y + dy][x + dx] == "[" and direction in ("v", "^"):
        return can_move_task2(matrix, x, y + dy, direction) and can_move_task2(matrix, x + 1, y + dy, direction)
    elif matrix[y + dy][x + dx] == "]" and direction in ("v", "^"):
        return can_move_task2(matrix, x, y + dy, direction) and can_move_task2(matrix, x - 1, y + dy, direction)
    else:
        return can_move_task2(matrix, x + dx, y + dy, direction)


def do_move_task2(matrix, x, y, direction):
    if not can_move_task2(matrix, x, y, direction):
        # print("Move not possible.")
        return x, y

    # Move object at coordinate (y,x) 1 step in "direction":
    d = directions_map[direction]
    dy, dx = d
    if matrix[y + dy][x + dx] == "#":
        assert False
    # Move stuff out of the way:
    elif matrix[y + dy][x + dx] == "[" and direction in ("v", "^"):
        do_move_task2(matrix, x + dx, y + dy, direction)
        do_move_task2(matrix, x + dx + 1, y + dy, direction)
    elif matrix[y + dy][x + dx] == "]" and direction in ("v", "^"):
        do_move_task2(matrix, x + dx, y + dy, direction)
        do_move_task2(matrix, x + dx - 1, y + dy, direction)
    elif matrix[y + dy][x + dx] != ".":
        do_move_task2(matrix, x + dx, y + dy, direction)

    assert matrix[y + dy][x + dx] == "."
    matrix[y + dy][x + dx] = matrix[y][x]
    matrix[y][x] = "."
    return x + dx, y + dy


def pretty_print(matrix):
    for i in range(len(matrix)):
        print("".join([x for x in matrix[i]]))


def get_checksum(matrix):
    result = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] in ("[", "O"):
                result += i * 100 + j
    return result


if __name__ == '__main__':
    # Task 1:
    matrix, moves = read_input_file(input_file, task2=False)
    # pretty_print(matrix)
    x, y = get_robot(matrix)

    for m in moves:
        # print(f"Robot is at x={x}, y={y}. Moving {m}")
        x, y = do_move_task2(matrix, x, y, m)
        # pretty_print(matrix)
        pass

    # pretty_print(matrix)
    print(f"Task 1: {get_checksum(matrix)}")

    # Task 2:
    matrix, moves = read_input_file(input_file, task2=True)
    # pretty_print(matrix)
    x, y = get_robot(matrix)
    for m in moves:
        # print(f"Robot is at x={x}, y={y}. Moving {m}")
        x, y = do_move_task2(matrix, x, y, m)
        # pretty_print(matrix)

    # pretty_print(matrix)
    print(f"Task 2: {get_checksum(matrix)}")
