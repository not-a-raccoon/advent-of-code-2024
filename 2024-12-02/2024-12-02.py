import csv
import logging

input_file = "2024-12-02_task.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def read_csv(file_path, delimiter=','):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            return list(reader)
    except FileNotFoundError:
        logging.error('File not found')


if __name__ == '__main__':
    inputs_raw = read_csv(input_file, delimiter=" ")
    # inputs_raw = [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1], [1, 3, 2, 4, 5], [8, 6, 4, 4, 1], [1, 3, 6, 7, 9]]
    inputs = [[int(a) for a in b] for b in inputs_raw]

    level_difference = [[a[i] - a[i + 1] for i in range(len(a) - 1)] for a in inputs]

    # Task 1
    safe_measurements = [1 if min(b) * max(b) > 0 \
                              and abs(min(b)) in [1, 2, 3] \
                              and abs(max(b)) in [1, 2, 3] \
                             else 0 for b in
                         level_difference]
    print(f"Number of safe measurements for Task 1: {sum(safe_measurements)} of {len(inputs)}")

    # Task 2

    # Level difference signs must be all positive, or all negative:
    level_difference_sign = [[1 if d > 0 else -1 for d in x] for x in level_difference]
    level_difference_sign_majority = [1 if sum(x) >= 0 else -1 for x in level_difference_sign]
    level_difference_sign_dissent = [[j for j, sign in enumerate(item) if sign != majority] for item, majority in
                                     zip(level_difference_sign, level_difference_sign_majority)]

    # Level differences must be between -3 and 3 (but not 0):
    level_difference_bad = [[j for j, value in enumerate(item) if value not in [-3, -2, -1, 1, 2, 3]] for item in
                            level_difference]

    # We may act on any measurement by removing any level at position i, for some 0<=i<=len(measurement)-1.

    # Acting on a measurement at position j implies introducing a new level difference, unless i==0 or i==len(measurement)-1:
    possible_actions = [[
                            # The result of not acting at all on the measurement is the same as
                            # the measurement being called "safe" in Task 1:
                            (None, 1, 1, 1, 1) if safe_measurements[i] == 1 else (None, 0, 0, 0, 0)]
                        + [
                            # Now let's calculate the result of acting at position j on the measurement,
                            # by which we mean removing the item at position j from the measurement:
                            (j,
                             # Newly introduced level difference must be between -3 and 3 (but not 0):
                             1 if j in [0, len(inputs[i]) - 1] else 1 if inputs[i][j - 1] - inputs[i][j + 1] in [-3, -2,
                                                                                                                 -1, 1,
                                                                                                                 2,
                                                                                                                 3] else 0,
                             # Newly introduced level difference sign must equal the measurement's majority sign:
                             1 if j in [0, len(inputs[i]) - 1] else 1 if (1 if inputs[i][j - 1] - inputs[i][
                                 j + 1] > 0 else -1) == level_difference_sign_majority[i] else 0,
                             # Sign dissents can only occur in places that would be removed by acting at position i:
                             1 if len(set(level_difference_sign_dissent[i]) - (
                                 {0} if j == 0 else {len(inputs[i]) - 2} if j in [0, len(inputs[i]) - 1] else {j - 1,
                                                                                                               j})) == 0 else 0,
                             # Bad level differences can only occur in places that would be removed by acting at position i:
                             1 if len(set(level_difference_bad[i]) - (
                                 {0} if j == 0 else {len(inputs[i]) - 2} if j in [0, len(inputs[i]) - 1] else {j - 1,
                                                                                                               j})) == 0 else 0
                             ) \
                            for j, value in enumerate(inputs[i])] for i in range(len(inputs))]

    good_actions = [[x[0] for x in p if x[1] == 1 and x[2] == 1 and x[3] == 1 and x[4] == 1] for p in possible_actions]
    redeemable_inputs = [j for j in range(len(inputs)) if len(good_actions[j]) > 0]

    print(f"Number of redeemable measurements for Task 2: {len(redeemable_inputs)} of {len(inputs)}")

