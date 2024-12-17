input_file = "2024-12-17_task.txt"


class Computer:
    registers: list[int]
    program: list[int]
    outputs: list[int]
    steps: int

    def __init__(self):
        self.registers = [0, 0, 0]
        self.program: list[int] = []
        self.outputs: list[int] = []
        self.instruction_pointer: int = 0
        self.halted: bool = False
        self.steps: int = 0

    def from_input_file(self, filename):
        self.outputs = []
        self.instruction_pointer = 0
        self.halted = False
        self.steps = 0
        with open(filename, 'r') as file:
            for row, line in enumerate(file):
                if row < 3:
                    self.registers[row] = int(line.strip()[12:])
                elif line.strip() == "":
                    pass
                else:
                    assert line.startswith("Program: ")
                    self.program = [int(x) for x in line.strip()[9:].split(",")]

    def combo_operand(self, a):
        if a in [4, 5, 6]:
            return self.registers[a - 4]
        elif a in [0, 1, 2, 3]:
            return a
        else:
            assert False

    def listing(self):
        print("")
        print(f"**** Listing of program: ****")
        i = 0
        while i < len(self.program):
            instruction = self.program[i]
            operand = self.program[i+1]
            is_literal_operand = True
            instruction_description = ""
            instruction_text = ""
            instruction_description_2 = ""

            if instruction in [0, 6, 7]:
                instruction_text = "adv" if instruction == 0 else "bdv" if instruction == 6 else "cdv"
                instruction_description = chr(65+[0,6,7].index(instruction)) + " = A shr "
                is_literal_operand = False
            elif instruction == 1:
                # Operand "bxl"
                instruction_text = "bxl"
                instruction_description = "B = B xor "
                instruction_description_2 = ""
                is_literal_operand = True
            elif instruction == 2:
                # Operand "bst"
                instruction_text = "bst"
                instruction_description = "B = "
                instruction_description_2 = " mod 8"
                is_literal_operand = False
            elif instruction == 4:
                instruction_text = "bxc"
                # Operand "bxc"; Input is ignored
                instruction_description = "B = B xor C"
                instruction_description_2 = ""
                operand_text = ""
            elif instruction == 5:
                instruction_text = "out"
                # Operand "out"
                instruction_description = "out "
                instruction_description_2 = " mod 8"
                is_literal_operand = False
            elif instruction == 3:
                instruction_text = "jnz"
                instruction_description = "jump to "
                instruction_description_2 = " if A != 0"

            operand_text = "" if instruction == 4 else chr(operand-4+65) if not is_literal_operand and operand in [4, 5, 6] else str(operand)

            print(f"{i:04d}: {instruction_text} {self.program[i+1]} |  {instruction_description}{operand_text}{instruction_description_2}")
            i += 2
        print("End of listing.")
        print("")


    def instruction_exec(self, instruction, literal_or_combo_operand):
        jumped = False
        if instruction in [0, 6, 7]:
            # Operand "adv" (0), "bdv" (6), "cdv" (7)
            result = self.registers[0] >> self.combo_operand(literal_or_combo_operand)
            self.registers[0 if instruction == 0 else 1 if instruction == 6 else 2] = result
        elif instruction == 1:
            # Operand "bxl"
            result = self.registers[1] ^ literal_or_combo_operand
            self.registers[1] = result
        elif instruction == 2:
            # Operand "bst"
            self.registers[1] = self.combo_operand(literal_or_combo_operand) % 8
        elif instruction == 4:
            # Operand "bxc"; Input is ignored
            self.registers[1] = self.registers[1] ^ self.registers[2]
        elif instruction == 5:
            # Operand "out"
            self.outputs += [self.combo_operand(literal_or_combo_operand) % 8]
        elif instruction == 3:
            # Operand "jnz"
            if self.registers[0] != 0:
                self.instruction_pointer = literal_or_combo_operand
                jumped = True

        if not jumped:
            self.instruction_pointer += 2  # +2 because inputs alternative between command / operand.
        self.steps += 1

    def run(self, optional_register_state=None, task2: bool = False, verbose: bool = False):
        if optional_register_state is not None:
            self.registers = optional_register_state.copy()
        self.halted = False
        self.instruction_pointer = 0
        self.outputs = []
        self.steps = 0
        if verbose:
            print(f"Running program {self.program}. Initial state: {self.registers}")
        while self.instruction_pointer < len(self.program):
            self.instruction_exec(self.program[self.instruction_pointer], self.program[self.instruction_pointer + 1])
            if verbose:
                print(f"After step {self.steps}, state is: {self.registers}")
            if task2 and self.outputs[:len(self.program)] != self.program:
                break
        self.halted = True
        print(f"Program terminated after {self.steps} steps. Outputs: {",".join([str(x) for x in self.outputs])}")


def octal_to_binary(octal_digit: int):
    # e.g., 4 -> "100"
    decimal_value = int(str(octal_digit), 8)
    binary_representation = bin(decimal_value)[2:]
    padded_binary = binary_representation.zfill(3)
    return padded_binary

def task2_set_bits_at_position(binary_string, offset_position, low_3_bits_value_octal, higher_3_bits_value_octal, higher_3_bits_position):
    # Try to set the lowest 3 bits, and also 3 higher bits, of a string representing a binary number.
    # The binary number may be bitwise unspecified (indicated by character "?"), or specified by "1" or "0".
    # The function fails if the values to be set collide with the values that have already been specified.

    assert len(binary_string) >= offset_position + higher_3_bits_position
    new_string = [x for x in binary_string]

    low_3_bits_value = octal_to_binary(low_3_bits_value_octal)
    higher_3_bits_value = octal_to_binary(higher_3_bits_value_octal)

    # Set lowest 3 bits, if possible:
    for ii in [1,2,3]:
        i = offset_position + ii
        if binary_string[-i] in ["0","1"] and binary_string[-i] != low_3_bits_value[-ii]:
            return False, None
        new_string[-i] = low_3_bits_value[-ii]
    # Set higher 3 bits at specified position, if still possible afters setting lowest 3 bits:
    for ii in [1,2,3]:
        i = offset_position + higher_3_bits_position + ii
        if new_string[-i] in ["0","1"] and new_string[-i] != higher_3_bits_value[-ii]:
            return False, None
        new_string[-i] = higher_3_bits_value[-ii]
    return True, "".join(new_string)


def task2_enforce_next_output(binary_string, step, next_output, low_3_bits_value):
    assert 0 <= low_3_bits_value <= 7


    # In each iteration N (N=0,1,2,...), we can set the Nth lowest 3 bits of A.
    # This will possibly imply setting some higher bits, too.
    # offset_position will be set to 3*N in iteration to indicate that the lowest 3*N bits have
    # already been set and must be left alone.
    offset_position = 3*step

    higher_3_bits_value = None
    higher_3_bits_position = None

    if low_3_bits_value == 0:
        higher_3_bits_position = 5
        higher_3_bits_value = next_output ^ 3
    elif low_3_bits_value == 1:
        higher_3_bits_position = 4
        higher_3_bits_value = next_output ^ 2
    elif low_3_bits_value == 2:
        higher_3_bits_position = 7
        higher_3_bits_value = next_output ^ 1
    elif low_3_bits_value == 3:
        higher_3_bits_position = 6
        higher_3_bits_value = next_output ^ 0
    elif low_3_bits_value == 4:
        higher_3_bits_position = 1
        higher_3_bits_value = next_output ^ 7
    elif low_3_bits_value == 5:
        higher_3_bits_position = 0
        higher_3_bits_value = next_output ^ 6
    elif low_3_bits_value == 6:
        higher_3_bits_position = 3
        higher_3_bits_value = next_output ^ 5
    elif low_3_bits_value == 7:
        higher_3_bits_position = 2
        higher_3_bits_value = next_output ^ 4

    assert higher_3_bits_position is not None
    assert higher_3_bits_value is not None

    # Call helper function to actually do the bit manipulation:
    return task2_set_bits_at_position(binary_string, offset_position, low_3_bits_value, higher_3_bits_value, higher_3_bits_position)

matches = []
def task2_recursion(desired_output, binary_string, step, previous_choices):
    if step >= len(desired_output):
        # print(f"Success!! {binary_string.replace("?", "0")}. Choices were: {previous_choices}.")
        matches.append(int(binary_string.replace("?", "0")))
        return

    # print(f"Enforcing output of {desired_output[step]} as output no. {step}, previous choices were {previous_choices}, binary string representing register A on program launch is currently {binary_string}.")
    for i in range(8):
        success, new_binary_string = task2_enforce_next_output(binary_string, step, desired_output[step], i)
        if success:
            task2_recursion(desired_output, new_binary_string, step+1, previous_choices + [i])

def task2(desired_output):
    # We generate a value for register A by backtracking.
    # Each iteration of the main loop of our program outputs a number that depends on the lowest 10 bits of A,
    # then shifts A to the right by 3 bits.
    # Any values set to B or C on program launch will be ignored.
    # So if an admissible value for register A can be found, then its length is <= 3*len(desired_output) + (10-3) in binary.
    binary_string = "0000000" + "?"*(3*len(desired_output))

    # print(task2_enforce_next_output(binary_string, 0, 5, 1))
    task2_recursion(desired_output, binary_string, 0, [])
    if len(matches) > 0:
        print(f"Success! Minimal match: {eval('0b' + str(min(matches)))}")
    else:
        print("No solution found.")


if __name__ == '__main__':
    c = Computer()
    c.from_input_file(input_file)

    c.listing()

    print(f"Task 1: Running program.")
    c.run(verbose=False)

    print("")

    print(f"Task 2: Finding the minimal input value for register A that makes the program output its source code.")
    task2(c.program)
