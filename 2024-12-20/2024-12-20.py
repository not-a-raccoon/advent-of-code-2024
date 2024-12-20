import sys

input_file = "2024-12-20_task.txt"
directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def read_input_file(file_path):
    matrix = []
    start_col = None
    start_row = None
    end_col = None
    end_row = None
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            s = line.strip()
            matrix.append([x for x in s])
            if "S" in s:
                start_row = row
                start_col = s.index("S")
            if "E" in s:
                end_row = row
                end_col = s.index("E")
    return matrix, start_col, start_row, end_col, end_row


def pretty_print(array):
    for line in array:
        print(" ".join(
            [x if x in ('S', 'E', '#', '.') else x if int(x) in range(10) else 'Z' if int(x) >= 36 else chr(
                65 + int(x) - 10) for x in line]))


def get_neighbours(matrix, x, y, cheating: bool):
    # Non-cheating neighbours of (y, x):
    n = [[a + d for a, d in zip([y, x], d)] for d in directions]
    n_inrange = [a for a in n if 0 < a[0] < len(matrix) - 1 and 0 < a[1] < len(matrix[0]) - 1]
    n_allowed = [a for a in n_inrange if matrix[a[0]][a[1]] in ('E', '.')]

    if cheating:
        # In task 1, cheating may last 2 moves.
        n = [[a + d for a, d in zip([y, x], d)] for d in directions for [y, x] in n_inrange]
        n_inrange = [a for a in n if 0 < a[0] < len(matrix) - 1 and 0 < a[1] < len(matrix[0]) - 1]
        # There is only a single path to the goal (not a single shortest path).
        # So any shortcut that a cheating move might make must end on one
        # of the tiles in the single path.
        n_allowed = [a for a in n_inrange if
                     a not in n_allowed and matrix[a[0]][a[1]] not in ('S', 'E', '.', '#') and int(
                         matrix[a[0]][a[1]]) > int(matrix[y][x])]

    return n_allowed


def walk_only_path_to_end(matrix, x, y, end_col, end_row, path):
    n_allowed = get_neighbours(matrix, x, y, False)

    if len(n_allowed) > 1:
        print("Ohoh!")
        print((y, x))
        print(n_allowed)
    end = [y, x] == [end_row, end_col]
    assert (len(n_allowed) == 1 and not end) or (end and n_allowed == [])

    matrix[y][x] = str(len(path))
    path = path + [[y, x]]
    if end:
        return True, path
    else:
        return walk_only_path_to_end(matrix, n_allowed[0][1], n_allowed[0][0], end_col, end_row, path)


def task1(matrix, path, threshold: int):
    result = 0
    max_saved = 0
    for p in path:
        c = get_neighbours(matrix, p[1], p[0], True)

        # Our function for task 2 is a lot slower here, because it always
        # reads the entire path.
        # c = get_cheating_targets_in_range(matrix, p[1], p[0], path=path, range=2, threshold=threshold)

        for n in c:
            steps_saved = int(matrix[n[0]][n[1]]) - int(matrix[p[0]][p[1]])
            if steps_saved >= threshold + 2:
                # print(f"Cheating move from {p} to {n} would save {steps_saved - 2} steps.")

                # Cheating moves take te regular amount of time (1 picosecond per step).
                # Since we are excluding valid moves in get_neighbours() when cheating=True,
                # all of the moves returned take 2 picoseconds and not 1.
                if max_saved == 0 or steps_saved - 2 > max_saved:
                    max_saved = steps_saved - 2
                result += 1
    return result, max_saved


# Note: you should really use a more efficent data structure for "path", but it works for the input data (path of length ~10000).
def get_cheating_targets_in_range(matrix, x, y, path, range: int, threshold: int):
    # the number of steps saved is matrix[ny][nx] - matrix[y][x] - abs(ny-y) - abs(nx-x),
    # because even though cheating takes a shortcut in the path, the moves
    # done while cheating still count as regular moves.
    t = [[ny, nx, int(matrix[ny][nx]) - int(matrix[y][x]) - abs(ny - y) - abs(nx - x)] for ny, nx in path if
         abs(ny - y) + abs(nx - x) <= range]
    return [tt for tt in t if tt[2] >= threshold]


def task2(matrix, path, range: int, threshold: int):
    result = 0
    max_saved = 0
    for p in path:
        c = get_cheating_targets_in_range(matrix, p[1], p[0], path=path, range=range, threshold=threshold)
        result += len(c)
        if len(c) > 0:
            ms = max([cc[2] for cc in c])
            if ms >= max_saved:
                max_saved = ms
    return result, max_saved


if __name__ == "__main__":
    sys.setrecursionlimit(1000000)

    matrix, start_col, start_row, end_col, end_row = read_input_file(input_file)
    assert start_col and end_col and start_row and end_row

    r, path = walk_only_path_to_end(matrix, start_col, start_row, end_col, end_row, [])
    assert r
    # pretty_print(matrix)
    print(f"There is one path of length {len(path)} from start to end.")

    # Task 1: one single "cheating" move allowed, and it can have length 2
    threshold = 100
    r, s = task1(matrix, path, threshold)
    print(f"Task 1: {r} different options for cheating moves of length 2 that "
          f"save at least {threshold} steps each. The best of these saves {s} steps.")

    # Task 2: still only one single "cheating" move is allowed, but it can have any length <= 20
    threshold = 100
    range = 20
    r, s = task2(matrix, path, range, threshold)
    print(f"Task 2: {r} different options for cheating moves of length <= {range} that "
          f"save at least {threshold} steps each. The best of these saves {s} steps.")
