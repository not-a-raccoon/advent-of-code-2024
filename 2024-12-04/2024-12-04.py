from itertools import product

input_file = "2024-12-04_task.txt"
directions = list(product([1, -1, 0], repeat=2))
directions_diagonal = list(product([1, -1], repeat=2))



def read_text_file_to_array(file):
    # Open the file in read mode
    with open(file, 'r') as file:
        array = []
        for line in file:
            array.append(list(line.strip()))
    return array

def xmas_at_pos(x, y):
    found = 0
    for dx,dy in directions:
        newx = x
        newy = y
        valid = True
        for letter in 'XMAS':
            if (newx < 0 or newx >= len(array[0])) or (newy < 0 or newy >= len(array)) or array[newy][newx] != letter:
                valid = False
                break
            newx += dx
            newy += dy

        if valid:
            # print(f"Found XMAS at {x},{y} in direction {dx},{dy}")
            found += 1
    return found


def mas_at_pos(x, y):
    found = 0
    for dx,dy in directions_diagonal:
        newx = x-dx
        newy = y-dy
        valid = True
        for letter in 'MAS':
            if (newx < 0 or newx >= len(array[0])) or (newy < 0 or newy >= len(array)) or array[newy][newx] != letter:
                valid = False
                break
            newx += dx
            newy += dy

        if valid:
            print(f"Found MAS at {x},{y} in direction {dx},{dy}")
            found += 1
    # There must be a "cross" of two diagonal occurences of MAS which share the same letter A:
    return found >= 2



if __name__ == "__main__":
    array = read_text_file_to_array(input_file)
    number_of_xmas = sum(xmas_at_pos(x,y) for x,y in product(range(len(array[0])), range(len(array))))
    print(f"Task 1: Number of XMASes: {number_of_xmas}")
    number_of_x_mas = sum(mas_at_pos(x, y) for x, y in product(range(len(array[0])), range(len(array))))
    print(f"Task 2: Number of X-MASes: {number_of_x_mas}")