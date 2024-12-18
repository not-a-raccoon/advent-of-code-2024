import heapq
import math

input_file = "2024-12-18_task.txt"
array_dim = 71  # 7 for demo data


def read_input_file(filename, array_dim):
    array = [[0] * array_dim for i in range(array_dim)]
    blocks = []
    with open(filename, "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            a = [int(aa) for aa in line.strip().split(",")]
            blocks.append(a)
            if not(0 <= a[0] < array_dim and 0 <= a[1] < array_dim):
                raise ValueError(
                    f"Invalid coordinates ({a[0]},{a[1]}) in line {i+1} of input file {filename}. Coordinates must be between 0 and {array_dim-1}."
                )
            array[a[1]][a[0]] = i+1
    return array, blocks, i+1


def pretty_print(array, at_time: int = None):
    for line in array:
        print("".join(
            ["#" if (x > 0 and at_time is None) or (at_time is not None and 0 < x <= at_time) else " " for x in line]))

directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
def neighbours(matrix, x, y, at_time: int|None = None):
    result = []
    for dx, dy in directions:
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < len(matrix[0]) and 0 <= new_y < len(matrix):
            if (at_time is None and matrix[new_y][new_x] == 0) or (at_time is not None and matrix[new_y][new_x] > at_time) or (at_time is not None and matrix[new_y][new_x] == 0):
                result.append((new_x, new_y, 1))
    return result


# adapted from day 16
def dijkstra(matrix, start_col, start_row, at_time: int|None = None):
    queue = []
    predecessors = {}
    distance = {}

    predecessors[(start_col, start_row)] = []
    distance[(start_col, start_row)] = 0
    # priority queue:  heap elements are: (current cost estimate, (x, y))
    heapq.heappush(queue, (0, (start_col, start_row)))

    while queue:
        a = heapq.heappop(queue)
        cost, (x, y) = a
        for n in neighbours(matrix, x, y, at_time):
            nx, ny, nc = n
            alternative = distance[(x, y)] + nc
            if alternative < distance.get((nx, ny), math.inf):
                distance[(nx, ny)] = alternative
                predecessors[(nx, ny)] = (x, y)
                heapq.heappush(queue, (alternative, (nx, ny)))

    return distance, predecessors


if __name__ == "__main__":

    exit_x = array_dim - 1
    exit_y = array_dim - 1

    start_x = 0
    start_y = 0

    array, blocks, number_of_iterations = read_input_file(input_file, array_dim)

    test_iteration = 1024
    d, p = dijkstra(array, start_x, start_y, test_iteration )
    if (exit_x, exit_y) in d:
        print(f"Task 1: in iteration {test_iteration}, the distance to the exit is {d[(exit_x, exit_y)]}.")
    else:
        print(f"Task 1: in iteration {test_iteration}, the exit is not reachable.")

    # print(f"Task 2: Number of iterations is: {number_of_iterations}")

    left = 0
    right = number_of_iterations
    while left <= right:
        middle = left + (right - left) // 2
        # print(f"Testing iteration {middle}...")
        d, p = dijkstra(array, start_x, start_y, middle)
        d2, p2 = dijkstra(array, start_x, start_y, middle-1)

        if (exit_x, exit_y) not in d and (exit_x, exit_y) in d2:
            print(f"Task 2: {middle} is the first point in time where the path is blocked by obstacles. "
            f"The block that was new at this point in time was (x,y)=({blocks[middle-1][0]}, {blocks[middle-1][1]}).")
            break
        elif (exit_x, exit_y) in d:
            left = middle + 1
        else:
            right = middle - 1


