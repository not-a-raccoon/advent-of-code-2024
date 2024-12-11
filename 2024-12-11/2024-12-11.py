input_file = "2024-12-11_task.txt"

def read_input_file(file_name):
    with open(file_name) as f:
        return [int(i) for i in f.readlines()[0].split(" ")]


def blink(input):
    for i in reversed(range(len(input))):
        a = input[i]
        input.pop(i)
        if a == 0:
            input.insert(i, 1)
        elif len(str(a)) % 2 == 0:
            input.insert(i, int(str(a)[0:(len(str(a))//2)]))
            input.insert(i+1, int(str(a)[(len(str(a)) // 2):len(str(a))]))
        else:
            input.insert(i, a*2024)

cache = {}
def blink_smarter(a, iterations_todo):
    if (a, iterations_todo) in cache:
        return cache[(a, iterations_todo)]

    if iterations_todo == 0:
        return 1

    if a == 0:
        cache[(a, iterations_todo)] = blink_smarter(1, iterations_todo-1)
    elif len(str(a)) % 2 == 0:
        cache[(a, iterations_todo)] = blink_smarter(int(str(a)[0:(len(str(a)) // 2)]), iterations_todo-1)\
            + blink_smarter(int(str(a)[(len(str(a)) // 2):len(str(a))]), iterations_todo-1)
    else:
        cache[(a, iterations_todo)] = blink_smarter(2024*a, iterations_todo-1)

    return cache[(a, iterations_todo)]



if __name__ == "__main__":
    the_input = read_input_file(input_file)

    result = 0
    for i in the_input:
        result += blink_smarter(i, 25)

    print(f"Task 1: {result}")

    result = 0
    for i in the_input:
        result += blink_smarter(i, 75)

    print(f"Task 2: {result}")
    print(f"len(cache) = {len(cache)}")
