from itertools import product
import sys
import logging
import copy

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

input_file = "2024-12-06_task.txt"

directions = [[0, -1, 1, "N"], [1, 0, 2, "E"], [0, 1, 4, "S"], [-1, 0, 8, "W"]] # N, E, S, W in this order


def read_text_file_to_array(file):
    with open(file, 'r') as file:
        array = []
        for line in file:
            array.append(list(line.strip().replace("\n", "").replace("\r", "")))
    return array

def get_guard(array):
    x, y = [(x,y) for x in range(len(array)) for y in range(len(array[0])) if array[y][x]=="^"][0]
    return x, y

def step(array, visited, guard_x, guard_y, direction, num_steps, positions_visited):
    assert 0 <= direction < 4
    logging.debug(f"At position (x={guard_x}, y={guard_y}), in direction {directions[direction][3]}. We have visited {positions_visited} positions.")

    # Mark current tile as visited in the current direction:
    assert visited[guard_y][guard_x] & directions[direction][2] == 0 and array[guard_y][guard_x] != "#"
    visited[guard_y][guard_x] |= directions[direction][2]

    # This is where the guard would step next:
    new_x = guard_x + directions[direction][0]
    new_y = guard_y + directions[direction][1]

    # Now what happens there?:
    if (new_x < 0) or (new_y >= len(array)) or (new_y < 0) or (new_x >= len(array[0])):
        # guard exits maze
        logging.debug(f"Guard exits maze after {num_steps} steps, and with {positions_visited} positions visited.")
        return 1, num_steps, positions_visited
    if visited[new_y][new_x] & directions[direction][2] > 0:
        # tile has been visited before, in this direction
        logging.debug(f"This place looks familiar. Afters: {num_steps} steps, and with {positions_visited} positions visited.")
        return 2, num_steps, positions_visited
    if array[new_y][new_x] == "#":
        # tile is blocked, rotate clockwise
        logging.debug("Path is blocked, rotating clockwise.")
        if visited[guard_y][guard_x] & directions[(direction+1) % 4][2] > 0:
            # tile has been visited before, in this direction
            logging.debug(
                f"This place looks familiar. Afters: {num_steps} steps, and with {positions_visited} positions visited.")
            return 2, num_steps, positions_visited
        return step(array, visited, guard_x, guard_y, (direction+1) % 4, num_steps + 1, positions_visited)

    # Visit new tile (or known tile, but in new direction):
    is_new_tile = visited[new_y][new_x] == 0
    return step(array, visited, new_x, new_y, direction, num_steps + 1, positions_visited + 1 if is_new_tile else positions_visited)

def pretty_print(array, visited):
    for y in range(len(the_array)):
        for x in range(len(the_array)):
            if visited[y][x] > 0:
                the_array[y][x] = "X"
        print("".join([x for x in the_array[y]]))

if __name__ == "__main__":
    the_array = read_text_file_to_array(input_file)
    visited_init = [[0 for i in range(len(the_array[0]))] for j in range(len(the_array))]

    the_visit = copy.deepcopy(visited_init)

    sys.setrecursionlimit(123456789) # wtf, Python's default recursion limit is just 1000?


    guard_x, guard_y = get_guard(the_array)
    result, num_steps, positions_visited = step(the_array, the_visit, guard_x, guard_y, 0, 0, 1)
    logging.info(f"Task 1: result = {'EXIT' if result==1 else 'LOOP'}, num_steps = {num_steps}, positions_visited = {positions_visited}")

    assert result == 1 # Unabridged maze run should be an EXIT, not a LOOP

    num_loops = 0
    num_tries = 0
    for (x,y) in  [(x,y) for x in range(len(the_array)) for y in range(len(the_array[0])) if the_visit[y][x]>0]:
        if (x == guard_x) and (y == guard_y):
            # A rule forbids to place an obstacle at the guard's starting position.
            continue

        logging.debug(f"Placing test obstacle at position: x={x}, y={y}.")
        new_visit = copy.deepcopy(visited_init)
        assert the_array[y][x] != "#"
        the_array[y][x] = "#"
        result, _, _ = step(the_array, new_visit, guard_x, guard_y, 0, 0, 1)
        the_array[y][x] = "."
        logging.debug(f"result = {'EXIT' if result == 1 else 'LOOP'}, num_steps = {num_steps}, positions_visited = {positions_visited}")
        if result == 2:
            num_loops += 1
        num_tries += 1
        if num_tries % 100 == 0:
            print(f"num_tries = {num_tries}")
        

    logging.info(f"Task 2: Number of possible loops by placing an additional obstacle: {num_loops}.")
