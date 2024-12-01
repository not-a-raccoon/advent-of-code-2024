import csv
import logging

input_file = "2024-12-01_task1.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

def read_csv(file_path, delimiter=','):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            return list(reader)
    except FileNotFoundError:
        logging.error('File not found')


if __name__ == '__main__':
    input_raw = read_csv(input_file, delimiter=" ")
    # there are some additional spaces in the input. Our data should be
    # the 1st and 4th column of every line in the result:
    input_1 = [int(i[0]) for i in input_raw]
    input_2 = [int(i[3]) for i in input_raw]

    # input_1 = [3,4,2,1,3,3]
    # input_2 = [4,3,5,3,9,3]

    if len(input_1) != len(input_2):
        logging.error('The number of rows in the two columns of data do not match.')

    # Sorting: Python modifies lists in-place and returns None. Weird.
    input_1.sort()
    input_2.sort()

    distance = sum(abs(input_1[j] - input_2[j]) for j in range(len(input_1)))

    print(f"Task 1a: Calculated distance is: {distance}")

    counts = {i: i * input_1.count(i) * input_2.count(i) for i in set(input_1)}
    count = sum(counts[i] for i in counts)

    print(f"Task 1b: Calculated distance is: {count}")
