from itertools import product
from more_itertools import distinct_permutations

input_file = "2024-12-21_task.txt"


def read_input_file(filename):
    result = []
    with open(filename) as f:
        for s in f.readlines():
            if s.strip() == "":
                continue
            result.append([a for a in s.strip()])
    return result


def get_position_on_keypad(keypad_type, key):
    result = None
    if keypad_type == "numeric":
        if key == "A":
            return [3, 2]
        elif key == "#":
            # blocked path
            return [3, 0]
        elif key == "0":
            return [3, 1]
        k = int(key)
        col = (k - 1) % 3
        row = 3 - ((k + 2) // 3)
        return [row, col]
    elif keypad_type == "direction":
        if key == "A":
            return [0, 2]
        elif key == "^":
            return [0, 1]
        elif key == ">":
            return [1, 2]
        elif key == "v":
            return [1, 1]
        elif key == "<":
            return [1, 0]
        elif key == "#":
            return [0, 0]
    return result


def map_direction_to_output(direction):
    result = None
    if direction == [0, 1]:
        result = ">"
    elif direction == [0, -1]:
        result = "<"
    elif direction == [1, 0]:
        result = "v"
    elif direction == [-1, 0]:
        result = "^"
    assert result
    return result


def shortest_paths_on_keypad(keypad_type, from_key, to_key):
    result = []

    from_y, from_x = get_position_on_keypad(keypad_type, from_key)
    to_y, to_x = get_position_on_keypad(keypad_type, to_key)
    # if keypad_type == "direction" and from_key == "A":
    #    pass
    path_elements = []
    if from_y != to_y:
        path_elements += [[1 if to_y > from_y else -1, 0]] * abs(from_y - to_y)
    if from_x != to_x:
        path_elements += [[0, 1 if to_x > from_x else -1]] * abs(from_x - to_x)
    if from_key == to_key:
        return ["A"]
    invalid = [get_position_on_keypad(keypad_type, "#")]
    unique_perms = list(distinct_permutations(path_elements))
    for pp in unique_perms:
        # walk the path and break if an invalid place is in the path:
        p = list(pp)
        y, x = from_y, from_x
        step = 0
        valid = True
        while True:
            y += p[step][0]
            x += p[step][1]
            if (y == to_y) and (x == to_x):
                break
            if [y, x] in invalid:
                # We may never step on whatever places are marked with "#" on our keypad.
                valid = False
                break
            step += 1
        if valid:
            result.append([map_direction_to_output(x) for x in p] + ["A"])
    return result


def all_shortest_paths_on_keypads():
    result = {}
    for keypad_type in ["numeric", "direction"]:
        if keypad_type == "numeric":
            keyset = ["A"] + [str(i) for i in range(10)]
        else:
            keyset = ["A", "^", ">", "v", "<"]

        for key_1 in keyset:
            for key_2 in keyset:
                result[(keypad_type, key_1, key_2)] = shortest_paths_on_keypad(keypad_type, key_1, key_2)
                assert result[(keypad_type, key_1, key_2)]
    return result


def solve(keypad_list, desired_result, all_shortest_paths):
    keypad_list_range = range(len(keypad_list))

    level_todo = [desired_result]
    for k in range(len(keypad_list)):
        next_level_todo = []
        while level_todo:
            # Process next option for this level. We start with the level's starting key.
            current_output = []
            # Starting key for this level:
            from_key = keypad_list[k][1]
            # The next possibility for the output we wish to produce on this level:
            d = level_todo.pop(0)
            # Translate given input to a list of instructions like "move from key A to key B and then press B":
            for i in range(len(d)):
                to_key = d[i]
                options = all_shortest_paths[(keypad_list[k][0], from_key, to_key)]
                current_output.append(options)
                from_key = to_key
            # Now let's generate input for the next-level keypad:
            # for every character c to be generated on this level, we have genreated all
            # shortest lists of button-presses which produce c.
            # So the input for the next level is all combinations of these separate outputs:
            r = []
            for combo in product(*current_output):
                flattened = [item for sublist in combo for item in sublist]
                r.append(flattened)
            shortest_r = min([len(a) for a in r])
            print(f"DEBUG: {[len(a) for a in r]}")
            if len(next_level_todo) > 0:
                shortest_next_level_todo = min([len(a) for a in next_level_todo])
                found_something = shortest_r <= shortest_next_level_todo
            else:
                found_something = True
            if found_something:
                next_level_todo += [rr for rr in r if len(rr) == shortest_r]
        shortest_next_level_todo = min([len(a) for a in next_level_todo])
        level_todo = [a for a in next_level_todo if len(a) == shortest_next_level_todo]
        print(f"Input {"".join(desired_result)}: Level {k} done, shortest solution is {shortest_next_level_todo}. len(level_todo)={len(level_todo)} for next level.")
        print(f"Example solution: {"".join(level_todo[0])}")
    # Return the list of options of button-presses on the top level:
    return level_todo


def get_numeric_part(input):
    s = "".join([x for x in input if x in "1234567890"])
    assert s
    return int(s) if len(s) > 0 else 0


def solve_task2(best_paths_keypad, input, iterations):
    this_iteration = {}
    last_symbol = "A"
    for c in input:
        if (last_symbol, c) not in this_iteration:
            this_iteration[(last_symbol, c)] = 1
        else:
            this_iteration[(last_symbol, c)] += 1
        last_symbol = c

    while iterations > 0:
        next_iteration = {}
        for c in this_iteration.keys():
            v = this_iteration[c]

            b = best_paths_keypad[c]
            assert b
            assert b[-1] == "A"
            last_symbol = "A"
            for bb in b:
                if (last_symbol, bb) in next_iteration:
                    next_iteration[(last_symbol, bb)] +=  v
                else:
                    next_iteration[(last_symbol, bb)] = v
                last_symbol = bb

        iterations -= 1
        this_iteration = next_iteration
    return sum([this_iteration.get(c) for c in this_iteration.keys()])


if __name__ == "__main__":
    inp = read_input_file(input_file)
    solve_task1 = False

    assert get_position_on_keypad("numeric", "4") == [1, 0]
    assert get_position_on_keypad("numeric", "6") == [1, 2]
    assert get_position_on_keypad("numeric", "3") == [2, 2]

    assert shortest_paths_on_keypad("numeric", "A", "0") == [["<", "A"]]
    all_shortest_paths = all_shortest_paths_on_keypads()

    # keypads to translate between, and their respective starting positions
    keypads_all_the_way_down = [("numeric", "A"), ("direction", "A"), ("direction", "A")]

    if solve_task1:
        task1_checksum = 0
        for i in range(len(inp)):
            x = solve(keypads_all_the_way_down, inp[i], all_shortest_paths)
            print(f"Task 1: Example solution for input {"".join(inp[i])}: {x[0]}")
            task1_checksum += get_numeric_part(inp[i]) * len(x[0])

        print(f"Task 1: Checksum: {task1_checksum}")



    #
    # Let's talk about best paths on the keypad. If there are multiple paths for a combination
    # that are shortest on level +1, then we need to check on level +2 which of these is the best.
    # We did this manually, so the dict below is just stuff we computed by hand.
    #
    # An example calculation:
    # For moving from "A" to "v", the options are v< or <v.
    #
    # a) If you pick v<, then on the next level you will have to move
    # from A to v to < to A, which takes 6 moves, and the level +1 input looks like this:
    # [A]v<A<A>>^A
    # The [A] is not part of the level +1 code, but indicates that the cursor of level +1
    # will be at the A symbol when the robot starts producing our input. The cursor always
    # starts at the A symbol.
    #
    # b) If you pick <v, then you will have to move from A to < to v to A, which also takes 6 moves.
    # The corresponding level +1 input looks like this:
    # [A]v<<A>A>^A
    #
    # Now both of these inputs are the same length on level +1, and contain the same symbols in
    # different order. However the ordering makes a significant difference on level +2,
    # because ">>" means, that on level +2, the second ">" does not have to be produced
    # (just press A twice). Similarly for "<<" in the second variant.
    # So either a ">" or a "<" can be produced on level +2 by just pressing A.
    # But it is much more expensive to produce a "<" from level +1 on level +2 than
    # it is to produce a ">" sign from level +1 on level +2, since the path
    # from A to ">" is just "vA", but the path from A to "<" is "v<<A".

    best_paths_keypad = {}
    best_paths_keypad[("A", "A")] = ["A"]
    best_paths_keypad[("A", "^")] = ["<", "A"]
    best_paths_keypad[("A", "v")] = ["<", "v", "A"] # other variant eliminated manually
    best_paths_keypad[("A", "<")] = ["v", "<", "<", "A"] # other path is forbidden
    best_paths_keypad[("A", ">")] = ["v", "A"]
    best_paths_keypad[("^", "A")] = [">", "A"]
    best_paths_keypad[("^", "^")] = ["A"]
    best_paths_keypad[("^", "<")] = ["v", "<", "A"] # other path is forbidden
    best_paths_keypad[("^", ">")] = ["v", ">", "A"] # other variant eliminated manually
    best_paths_keypad[("v", "A")] = ["^", ">", "A"] # other variant eliminated manually
    best_paths_keypad[("v", "v")] = ["A"]
    best_paths_keypad[("v", "<")] = ["<", "A"]
    best_paths_keypad[("v", ">")] = [">", "A"]
    best_paths_keypad[("<", "A")] = [">", ">", "^", "A"] # other variants eliminated manually
    best_paths_keypad[("<", "^")] = [">", "^", "A"] # other variant eliminated manually
    best_paths_keypad[("<", "v")] = [">", "A"]
    best_paths_keypad[("<", "<")] = ["A"]
    best_paths_keypad[(">", "A")] = ["^", "A"]
    best_paths_keypad[(">", "^")] = ["<", "^", "A"] # other variant eliminated manually
    best_paths_keypad[(">", "v")] = ["<", "A"]
    best_paths_keypad[(">", ">")] = ["A"]
    # missing combinations are <>, ><, ^v, and v^. These are never needed.

    keypads_all_the_way_down = [("numeric", "A")]
    levels_of_direction_keypads = 25
    task2_checksum = 0
    for i in range(len(inp)):
        # Solve first step (numerical keypad): with task 1 solver
        x = solve(keypads_all_the_way_down, inp[i], all_shortest_paths)
        new_r = []
        for y in x:
            r = solve_task2(best_paths_keypad, y, levels_of_direction_keypads)
            new_r += [r*get_numeric_part(inp[i])]
            print(f"Task 2: Level 0 solution was {"".join(y)} of length {len(y)}; length of level {1+levels_of_direction_keypads} solution is {r}, checksum is {r*get_numeric_part(inp[i])}")
        print(f"Min checksum for input {"".join(inp[i])}: {min(new_r)}")
        task2_checksum += min(new_r)

    print(f"Task 2: Checksum: {task2_checksum}")
