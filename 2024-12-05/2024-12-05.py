input_file = "2024-12-05_task.txt"

def read_input_file(file):
    # Open the file in read mode
    with open(file, 'r') as file:
        ordering_rules = []
        page_numbers = []
        for line in file:
            if line.count("|") > 0:
                ordering_rules.append(tuple(int(x) for x in line.replace('\n','').split("|")))
            if line.count(",") > 0:
                page_numbers.append([int(x) for x in line.replace('\n','').split(",")])
    return ordering_rules, page_numbers

def are_ordering_rules_violated(chosen, ordering_rules):
    violations = [o for o in ordering_rules if o[0] in chosen and o[1] in chosen if chosen.index(o[0]) > chosen.index(o[1])]
    return violations

def backtracking(todo, chosen, ordering_rules):
    #print(f"chosen = {chosen}")
    if len(todo) == 0:
        return True, chosen

    for t in todo:
        # Is t still allowed to be placed at the end of our chosen list?
        if len([q for q in ordering_rules if q[0] == t and q[1] in chosen]) == 0:
            # Do any of the remaining todos forbid to place t before them?
            if len([q for q in ordering_rules if q[1] == t and q[0] in todo]) == 0:
                a, b = backtracking(todo - {t}, chosen + [t], [x for x in ordering_rules if x[0] in todo - {t} or x[1] in todo - {t}])
                if a:
                    return True, b
    return False, []

if __name__ == "__main__":
    ordering_rules, page_numbers = read_input_file(input_file)

    task_1 = 0
    task_2 = 0
    for p in page_numbers:
        if len(p) % 2 == 0:
            raise Exception(f"This input has even length: {p}")

        v = are_ordering_rules_violated(p, ordering_rules)
        if len(v) == 0:
            print(f"No rules are violated for input: {p}")
            middle = p[len(p) // 2]
            print(f"Middle element is: {middle}")
            task_1 += middle
        else:
            print(f"Rules are violated for input: {p}, namely: {v}")
            a, b = backtracking(set(p), [], [x for x in ordering_rules if x[0] in p and x[1] in p])
            if not a:
                raise Exception(f"This input can't be ordered correctly: {p}")
            print(f"Reordered input satisfies rules: {b}")
            middle = b[len(b) // 2]
            print(f"Middle element is: {middle}")
            task_2 += middle


    print(f"Task 1: {task_1}")
    print(f"Task 2: {task_2}")

