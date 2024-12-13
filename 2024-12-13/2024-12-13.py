import numpy as np

input_file = "2024-12-13_task.txt"

def solve(A, b):
    solution = np.linalg.solve(A, b)
    # print(f"Exact solution: a = {solution[0]}, b = {solution[1]}")
    if np.allclose(solution, np.round(solution)):
        x1 = int(round(solution[0]))
        x2 = int(round(solution[1]))
        if np.array_equal(A.dot([x1, x2]), b):
            print(f"Integral solution found: x1 = {x1}, x2 = {x2}")
            return True, x1, x2
        else:
            print(f"There is a solution, but it is not integral.")
            return False, None, None
    else:
        print(f"There is no solution.")
        return False, None, None

def process_input_file(filename, offset=0):
    with open(filename) as f:
        lines = f.readlines()
        eq = 0
        coordinate_sum = 0
        for i in range(len(lines)):
            s = lines[i]
            if i % 4 == 0:
                assert s.startswith("Button A")
                a_coords = [int(x) for x in lines[i].split(':')[1].replace('X+', '').replace('Y+', '').split(',')]
            elif i % 4 == 1:
                assert s.startswith("Button B")
                b_coords = [int(x) for x in lines[i].split(':')[1].replace('X+', '').replace('Y+', '').split(',')]
            elif i % 4 == 2:
                assert s.startswith("Prize:")
                eq += 1
                print(f"Equation #{eq}:")
                prize_coords = [offset + int(x) for x in lines[i].split(':')[1].replace('X=', '').replace('Y=', '').split(',')]
                A = np.transpose(np.array([a_coords, b_coords]))
                b = np.array(prize_coords)
                sol, x1, x2 = solve(A, b)
                if sol:
                    coordinate_sum += 3*x1 + 1*x2 # pressing button A costs 3 tokens, pressing button B costs 1 token
        print(f"Sum of solution coordinates of the subset of equations that have integral solutions: {coordinate_sum}")

if __name__ == "__main__":
    print("Task 1:")
    process_input_file(input_file, 0)
    print("Task 2:")
    process_input_file(input_file, 10000000000000)

