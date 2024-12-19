from functools import cache

input_file = "2024-12-19_task.txt"


def read_input_file(file_path):
    patterns = []
    targets = []
    reading_targets = False
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            s = line.strip()
            if s == "":
                reading_targets = True
                continue
            if not reading_targets:
                patterns = [x.strip() for x in s.split(",")]
            else:
                targets = targets + [s]
    return patterns, targets


# This is what I used for task 1. It is not good enough to solve task 2 in a short time.
def puzzle(desired_result, chosen, current_pattern, patterns_tried):
    if current_pattern in patterns_tried:
        return False, []
    if len(current_pattern) == len(desired_result):
        return True, {tuple(chosen)}

    solved = False
    result = set({})

    for i in range(len(patterns)):
        p = patterns[i]
        if len(current_pattern) + len(p) > len(desired_result):
            continue
        if desired_result[len(current_pattern):len(current_pattern) + len(p)] != p:
            continue
        r, c = puzzle(desired_result, chosen + [i], current_pattern + p, patterns_tried)
        if r:
            solved = True
            result = result.union(c)

    patterns_tried[current_pattern] = True
    return solved, result


def puzzle2(desired_result, patterns_processed):
    if desired_result in patterns_processed:
        return patterns_processed[desired_result]

    assert desired_result != ""

    result = 0

    for i in range(len(patterns)):
        p = patterns[i]
        if p == desired_result:
            result += 1
            continue
        if len(p) > len(desired_result) or not desired_result.startswith(p):
            continue
        r = puzzle2(desired_result[len(p):], patterns_processed)
        result += r

    patterns_processed[desired_result] = result
    return result


# The same as puzzle2(), but we let functools.cache do the caching for us:
@cache
def puzzle2_v2(desired_result):
    assert desired_result != ""

    result = 0
    for i in range(len(patterns)):
        p = patterns[i]
        if p == desired_result:
            result += 1
            continue
        if len(p) > len(desired_result) or not desired_result.startswith(p):
            continue
        r = puzzle2_v2(desired_result[len(p):])
        result += r

    return result


if __name__ == '__main__':
    patterns, targets = read_input_file(input_file)
    print(f"Task 1: {len(patterns)} patterns and {len(targets)} targets.")

    task1 = 0
    task2 = 0
    for i in range(len(targets)):
        good = puzzle2_v2(targets[i])
        if good > 0:
            print(f"Found {good} correct pattern(s) for target #{i}: {targets[i]}")
            task1 += 1
            task2 += good
        else:
            print(f"No pattern found for target #{i}: {targets[i]}")
            continue

    print(f"Task 1: {task1} targets were solved.")
    print(f"Task 2: {task2} is the total number of solutions.")
