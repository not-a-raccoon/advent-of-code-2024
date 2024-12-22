input_file = "2024-12-22_task.txt"


def read_input_file(file_path):
    seeds = []
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            s = line.strip()
            if s:
                seeds.append(int(s))
    return seeds


def mix(a: int, b: int):
    return a ^ b


def prune(a: int):
    return a & ((1 << 24) - 1)


def generate(a: int):
    b = prune(mix(a, a << 6))
    c = prune(mix(b, b >> 5))
    d = prune(mix(c, c << 11))
    return d


def use(a: int):
    return a % 10


def add_to_global_archive(g: dict, a: dict):
    for aa in a.keys():
        if aa in g:
            g[aa] += a[aa]
        else:
            g[aa] = a[aa]


def generate_many(a: int, n: int):
    archive = {}
    last_four = []
    for i in range(n):
        b = generate(a)
        last_four.append(use(b) - use(a))
        if i >= 4:
            last_four.pop(0)
        if i >= 3:
            if tuple(last_four) not in archive:
                archive[tuple(last_four)] = use(b)

        a = b
    return archive


if __name__ == '__main__':
    seeds = read_input_file(input_file)
    print(f"Seeds: {seeds}")

    enable_task1 = True
    enable_task2 = True

    if enable_task1:
        task1 = 0
        for s in seeds:
            t = s
            for i in range(2000):
                t = generate(t)
            task1 += t
        print(f"Task 1: {task1} is the sum of all seeds after 2000 iterations.")

    if enable_task2:
        g = {}
        for s in seeds:
            add_to_global_archive(g, generate_many(s, 2000))

        print(f"Task 2: {g[max(g, key=g.get)]} bananas are possible.")
