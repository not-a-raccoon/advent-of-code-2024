from math import prod

input_file = "2024-12-14_task.txt"

def read_input_file(filename):
    robots = {}
    with open(filename) as f:
        id = 0
        for line in f.readlines():
            id -= 1 # robot id, to allow the dict to keep multiple robots at one position
            s = [int(x) for x in line.replace(" v=",",").replace("p=", "").split(",")]
            robots[(s[1], s[0], id)] = (s[3], s[2])
    return robots

def step(robots, steps, board_width, board_height):
    # Robots walk in straight lines and wrap around the map when they hit an edge.
    robots_after_steps = {}
    for k in robots.keys():
        newy = (k[0] + steps*robots[k][0]) % board_height
        newx = (k[1] + steps*robots[k][1]) % board_width
        robots_after_steps[(newy, newx, k[2])] = robots[k]
    return robots_after_steps

def evaulate_board(robots, board_width, board_height):
    assert board_width % 2 == 1
    assert board_height % 2 == 1

    mid_x = board_width//2
    mid_y = board_height // 2

    quadrant = [0, 0, 0, 0]
    for k in robots.keys():
        if k[0] < mid_y and k[1] < mid_x:
            quadrant[0] += 1
        elif k[0] < mid_y and k[1] > mid_x:
            quadrant[1] += 1
        elif k[0] > mid_y and k[1] < mid_x:
            quadrant[2] += 1
        elif k[0] > mid_y and k[1] > mid_x:
            quadrant[3] += 1
    return prod(quadrant)

def print_board(robots, board_width, board_height):
    for y in range(board_height):
        t = ""
        for x in range(board_width):
            c = [r for r in robots if (r[0], r[1]) == (y, x)]
            if 0 < len(c) <= 9:
                d = str(len(c))
            elif len(c) == 0:
                d = "."
            elif len(c) > 9:
                d = "X"

            t = t + d
        print(t)

if __name__ == "__main__":
    robots = read_input_file(input_file)
    board_width = 101
    board_height = 103
    print(f"Read {len(robots)} robots.")

    # Task 1:
    tmp = step(robots, 100, board_width, board_height)
    print(f"Task 1: {evaulate_board(tmp, board_width, board_height)}")

    # Task 2:
    robots = read_input_file(input_file)
    scores = {}
    for i in range(board_height * board_width):
        tmp = step(robots, i, board_width, board_height)
        scores[i] = evaulate_board(tmp, board_width, board_height)
        #print_board(robots, board_width, board_height)

    sorted_scores = sorted(scores.items(), key=lambda item: item[1])
    whatever = 10
    # Easter egg: if the robots are arranged to display a picture,
    # then they should be evenly distributed over the quadrants,
    # so we expect a low score.
    lowest_keys = [key for key, value in sorted_scores[:whatever]]

    for i in lowest_keys:
        print(f"Task 2, after {i} iterations:")
        print_board(step(robots, i, board_width, board_height), board_width, board_height)

    # Now have a look at the printouts visually. Increase "whatever" if necessary.