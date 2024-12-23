from collections import defaultdict

input_file = "2024-12-23_task.txt"


def read_input_file(file_path):
    result = set({})
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            s = line.strip()
            if s == "":
                continue
            a = s.split("-")
            result = result.union({(a[0], a[1])})
            result = result.union({(a[1], a[0])})
    return result


def get_graph(edges):
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    return graph


# Task 2:
def find_larger_cliques(graph, edges, cliques):
    # Find cliques that are 1 vertex larger than the cliques of size N passed as parameters.
    larger_cliques = []
    for c in cliques:
        adjacent_to_all = graph[c[0]]
        for iv in range(1, len(c)):
            v = c[iv]
            adjacent_to_all = adjacent_to_all & graph[v]
            if len(adjacent_to_all) == 0:
                break
        for a in adjacent_to_all:
            new_value = c + [a]
            new_value.sort()
            if new_value not in larger_cliques:
                larger_cliques.append(new_value)
    return larger_cliques


# Task 1:
def find_cliques_of_size_3(graph):
    cliques = []
    for u in graph:
        for v in graph[u]:
            for w in graph[u] & graph[v]:
                if u < v < w:  # Avoid duplicates
                    cliques.append([u, v, w])
    return cliques


def contains_vertex_starting_with(clique, vertex_starts_with):
    for t in clique:
        if t.startswith(vertex_starts_with):
            return True
    return False


if __name__ == '__main__':
    inp = read_input_file(input_file)

    graph = get_graph(inp)

    c = find_cliques_of_size_3(graph)

    # We continue to task 2 with just those cliques that contain a computer starting with "t".
    # The problem description was not clear about this, but it works for our input.
    c = [x for x in c if contains_vertex_starting_with(x, "t")]
    task1 = len(c)
    print(f"Task 1: {task1} is the number of possible cliques of length 3 containing a computer that starts with 't'.")

    task2 = 3
    keep_enlarging = True
    while True:
        print(f"Task 2: looking for cliques of size {task2 + 1}...")
        new_c = find_larger_cliques(graph, inp, c)
        if len(new_c) > 0:
            c = new_c
        else:
            break
        task2 += 1
        print(f"Found {len(c)} new clique(s), e.g.: {c[0]}")

    # In the end, the graph should contain one largest clique:
    assert len(c) == 1

    print(
        f"Task 1: {task2} is the size of the largest clique in the graph which contains a computer that starts with 't'.")
    print(f"{','.join(c[0])} should be the password.")
