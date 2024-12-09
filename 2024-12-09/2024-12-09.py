input_file = "2024-12-09_task.txt"

def read_input_file(file_name):
    with open(file_name) as f:
        return f.readlines()[0]

def flatten(list_of_lists):
    return [x for y in list_of_lists for x in y]

def convert_to_filesystem(s):
    return flatten([[None if i % 2 == 1 else i//2]*int(s[i]) for i in range(len(s))])

def file_lengths(s):
    return [int(s[i]) for i in range(len(s)) if i % 2 == 0]

def free_blocks(fs):
    return [i for i in range(len(fs)) if fs[i] is None]

def used_blocks(fs):
    return [i for i in range(len(fs)) if fs[i] is not None]

def get_checksum(fs):
    return sum([i*fs[i] if fs[i] is not None else 0 for i in range(len(fs))])

def find_free_space(size, fs, maxpos):
    free = [i for i in range(len(fs)) if fs[i] is None]
    # print(f"free={free}, looking for free block of size={size}, maxpos={maxpos}")
    j = 1
    possible = [i for i in range(len(free)-(size-1)) if i+size-1 < len(free) and free[i+size-1] == free[i]+size-1]
    if len(possible) == 0:
        return maxpos+1
    else:
        return free[possible[0]]


if __name__ == '__main__':
    the_input = read_input_file(input_file)
    fs = convert_to_filesystem(the_input)
    # print(fs)

    free = free_blocks(fs)
    used = used_blocks(fs)

    print(f"#free = {len(free)}")
    print(f"#used = {len(used)}")

    # task 1: moving individual file blocks
    i = 0
    while i < len(used) and i < len(free):
        defrag_at_pos = free[i]
        if defrag_at_pos >= len(used):
            break
        # print(f"defrag_at_pos = {defrag_at_pos}")
        fs[defrag_at_pos] = fs[used[-(i+1)]]
        fs[used[-(i+1)]] = None
        i += 1
        # print(f"Filled position: {undefrag_at_pos}")
        # print("".join(fs))

    # print(fs)
    task_1 = get_checksum(fs)
    print(f"Task 1: {task_1}")

    fs = convert_to_filesystem(the_input)

    # task 2: moving whole files at a time, starting with the right-most file.
    # we are really inefficient here. To improve, we could keep track of the position of the first consecutive
    # free N blocks, for 1<=N<=9.
    fl = file_lengths(the_input)
    print(f"Processing {len(fl)} files. Each '.' means 100 files processed.")
    for the_file in reversed(range(len(fl))):
        if the_file % 100 == 0:
            print(".",end="")
        # try to move each file to the front exactly once:
        file_position = sum(int(the_input[2*j])+int(the_input[2*j+1]) for j in range(the_file))
        # print(f"File #{the_file} should start at position {file_position}")
        new_position = find_free_space(fl[the_file], fs, file_position-1)
        if new_position < file_position:
            # print(f"Found new position for file #{the_file}: {new_position}")
            pass
        else:
            # This file can't be moved to consecutive free blocks to the left of it.
            # print(f"File #{the_file} can't be moved.")
            continue

        for k in range(fl[the_file]):
            fs[new_position + k] = fs[file_position + k]
            fs[file_position + k] = None

        # print(f"fs={fs}")

    task_2 = get_checksum(fs)
    print(f"Task 2: {task_2}")
