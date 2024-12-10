input_file = "2024-12-10_task.txt"


def read_input_file(file_path):
    matrix = []
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            matrix.append([int(x) for x in line.strip()])
    return matrix


def valid_moves(matrix, x, y):
    lenx = len(matrix[0])
    leny = len(matrix)
    result = []
    for v in ([-1, 0], [0, 1], [0, -1], [1, 0]):
        dy = v[0]
        dx = v[1]
        if 0 <= x + dx < lenx and 0 <= y + dy < lenx:
            if matrix[y + dy][x + dx] == matrix[y][x] + 1:
                result.append(v)
    return result


def bfs(matrix, x, y, visited, current_hike, partial_hikes, complete_hikes):
    partial_hikes += [tuple(current_hike)]

    if matrix[y][x] == 9:
        print(f"Summit reached at (x,y)={(x, y)}. Hike was: {current_hike}")
        complete_hikes += [current_hike]
        if (y,x) not in visited:
            visited.add((y, x))
            return 1
        else:
            return 0

    visited.add((y, x))

    summits = 0
    for v in valid_moves(matrix, x, y):
        dy, dx = v
        if tuple(current_hike + [(y + dy, x + dx)]) not in partial_hikes:
            new_summits = bfs(matrix, x + dx, y + dy, visited, current_hike + [(y + dy, x + dx)], partial_hikes, hikes)
            summits += new_summits

    return summits


if __name__ == '__main__':
    the_input = read_input_file(input_file)

    summits = 0
    ratings = 0
    for y in range(len(the_input)):
        for x in range(len(the_input[y])):
            if the_input[y][x] == 0:
                hikes = []
                new_summits = bfs(the_input, x, y, set(), [], [], hikes)
                print(f"Mountaineering at x={x}, y={y}: reached {summits} sumits.")
                for h in hikes:
                    print(f"Hike: {h}")
                ratings += len(hikes)
                summits += new_summits

    print(f"Task 1: {summits} summits reached.")
    print(f"Task 2: {ratings} is the total sum of ratings of all hikes.")
