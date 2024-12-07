input_file = "2024-12-07_task.txt"
equations = []

def read_input_file(file_name):
    result = []
    with open(file_name) as f:
        for l in f.readlines():
            left, right = l.split(":")
            assert len(left) > 0 and len(right) > 0
            result += [[int(left), [int(r) for r in right.split(" ") if len(r) > 0]]]
    return result

def concatenation_operation(x, y):
    return int(str(x) + str(y))

def backtracking(values, desired_result, chosen_operators, index, result_so_far, allow_concatenation_operator):
    if index == len(values):
        if result_so_far == desired_result:
            return True, chosen_operators
        else:
            return False, []

    if result_so_far * values[index] <= desired_result:
        a, b = backtracking(values, desired_result, chosen_operators + ['*'], index + 1, result_so_far * values[index], allow_concatenation_operator)
        if a:
            return True, b
    if result_so_far + values[index] <= desired_result:
        a, b = backtracking(values, desired_result, chosen_operators + ['+'], index + 1, result_so_far + values[index], allow_concatenation_operator)
        if a:
            return True, b
    if allow_concatenation_operator:
        if concatenation_operation(result_so_far, values[index]) <= desired_result:
            a, b = backtracking(values, desired_result, chosen_operators + ['||'], index + 1, concatenation_operation(result_so_far, values[index]), allow_concatenation_operator)
            if a:
                return True, b


    return False, []

def format_equation(sum, values, operators):
    assert len(values)-1 == len(operators)
    return f"{sum}=" + "".join(f"{n}{l}" for n, l in zip(values, operators+[""]))

if __name__ == "__main__":
    equations = read_input_file(input_file)
    task1 = 0
    task2 = 0
    for res, values in [e for e in equations]:
        a, b = backtracking(values, res, [], 1, values[0], False)
        if a:
            # print(format_equation(res, values, b))
            task1 += res
        # print(f"Task 1 failed to solve equation: {res} from {values}")
        a, b = backtracking(values, res, [], 1, values[0], True)
        if a:
            # print(format_equation(res, values, b))
            task2 += res

    print(f"Task 1: {task1}")
    print(f"Task 2: {task2}")

