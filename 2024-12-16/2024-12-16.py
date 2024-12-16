import heapq
import math


input_file = "2024-12-16_task.txt"
directions_map = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}


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


# for an A*-like approach, we could have used this:
def estimate_minimum_distance_to_goal(matrix, x, y, end_col, end_row, orientation):
    # each turn costs 1000, each move costs 1.
    result = abs(x - end_col) + abs(y - end_row)
    d = directions_map[orientation]
    dy, dx = d

    if dy == 0:
        if x < end_col and dx < 0:
            result += 2000
        elif x > end_col and dx > 0:
            result += 2000
        elif y != end_row:
            result += 1000
    elif dx == 0:
        if y < end_row and dy < 0:
            result += 2000
        elif y > end_row and dy > 0:
            result += 2000
        elif x != end_col:
            result += 1000
    return result


def rotate(orientation, n):
    x = [">", "v", "<", "^"]
    return x[(x.index(orientation) + n) % 4]


def neighbours(matrix, x, y, orientation):
    result = []
    dy, dx = directions_map[orientation]
    for i in [-1, 0, 1, 2]:  # to be read as: turn x*90°
        new_x = x if i != 0 else x + dx
        new_y = y if i != 0 else y + dy
        new_orientation = rotate(orientation, i)
        new_cost = 1 if i == 0 else 1000*abs(i)
        if 0 <= new_x < len(matrix[0]) and 0 <= new_y < len(matrix):
            if matrix[new_y][new_x] != "#":
                result.append((new_x, new_y, new_orientation, new_cost))
    return result


def dijkstra(matrix, start_col, start_row, start_orientation, end_col, end_row):
    queue = []
    predecessors = {}
    distance = {}

    predecessors[(start_col, start_row, ">")] = []
    distance[(start_col, start_row, ">")] = 0
    # priority queue:  heap elements are: (current cost estimate, (x, y, orientation))
    heapq.heappush(queue, (0, (start_col, start_row, ">")))


    while queue:
        a = heapq.heappop(queue)
        cost, (x, y, orientation) = a
        for n in neighbours(matrix, x, y, orientation):
            nx, ny, no, nc = n
            alternative = distance[(x, y, orientation)] + nc
            if alternative == distance.get((nx, ny, no), math.inf):
                # For task 2, we keep track of all the best predecessors, not just one arbitrary best predecessor.
                predecessors[(nx, ny, no)] += [(x, y, orientation)]
            if alternative < distance.get((nx, ny, no), math.inf):
                distance[(nx, ny, no)] = alternative
                predecessors[(nx, ny, no)] = [(x, y, orientation)]
                heapq.heappush(queue, (alternative, (nx, ny, no)))

    return distance, predecessors



if __name__ == "__main__":
    matrix, start_col, start_row, end_col, end_row = read_input_file(input_file)
    assert start_col and end_col and start_row and end_row

    d, p = something_like_dijkstra(matrix, start_col, start_row, ">", end_col, end_row)

    goals = [(end_col, end_row, orientation) for orientation in directions_map.keys()]
    r = [d.get(g, math.inf) for g in goals]
    assert r != math.inf

    print(f"Task 1: Shortest path has cost {min(r)}")

    # Task 2: Count the distinct (x,y) coordinates of all the vertices in one of the best paths:
    todo = []
    counted = {}
    processed = {}
    # start with any orientation of the goal tile that has the lowest cost, there may be ties:
    for g in goals:
        if d.get(g, math.inf) == min(r):
            todo.append(g)
    while todo:
        x, y, orientation = todo.pop()
        counted[(x,y)] = True
        processed[(x,y,orientation)] = True
        for pp in p[(x, y, orientation)]:
            if pp not in processed:
                todo.append(pp)

    print(f"Task 2: There are {len(counted)} distinct (x,y) coordinates in the shortest path.")