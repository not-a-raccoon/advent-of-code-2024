import csv
import logging
import re


input_file = "2024-12-03_task.txt"
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)



def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == '__main__':
    # read input, strip newlines:
    inputs = read_text_file(input_file).replace('\n', '').replace('\r', '')
    pattern = r'mul\((\d+),(\d+)\)'
    matches = re.findall(pattern, inputs)

    # Task 1

    the_sum = sum([int(x)*int(y) for x,y in matches])
    #print([[int(x), int(y)] for x,y in matches])
    print(f"Task 1: {the_sum}")

    # Task 2

    # shortest matches of the non-processing substrings can be obtained with ".*?" instead of ".*":
    pattern_disabled = r"don't\(\).*?do\(\)"
    # We make sure that an input where the last do/don't is a "don't" gets handled correctly
    # by adding a "do()" at the end:
    matches_disabled = re.findall(pattern_disabled, inputs + "do()")
    the_sum -= sum([sum([int(x)*int(y) for x,y in re.findall(pattern, p)]) for p in matches_disabled])
    print(f"Task 2: {the_sum}")