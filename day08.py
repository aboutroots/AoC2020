from common import file_to_lines


def parse_line_to_instr(line):
    instr, arg = line.strip().split()
    return instr, int(arg)


class InfiniteLoopException(BaseException):
    pass


class Processor:
    def __init__(self):
        self._reset()
        self.instr_map = {
            "nop": self._nop,
            "jmp": self._jmp,
            "acc": self._acc,
        }

    def _reset(self):
        self.visited = {}
        self.acc = 0
        self.pointer = 0

    def _nop(self, pointer, acc, arg):
        return pointer + 1, acc

    def _jmp(self, pointer, acc, arg):
        return pointer + arg, acc

    def _acc(self, pointer, acc, arg):
        return pointer + 1, acc + arg

    def _update_visited(self):
        if self.pointer in self.visited:
            raise InfiniteLoopException()
        self.visited[self.pointer] = True

    def _run_instruction(self, instruction):
        self._update_visited()

        instr_name, instr_arg = instruction
        proc_method = self.instr_map[instr_name]
        new_pointer, new_acc = proc_method(self.pointer, self.acc, instr_arg)

        self.pointer = new_pointer
        self.acc = new_acc

    def run_program(self, instructions):
        self._reset()
        success = True
        while True:
            try:
                self._run_instruction(instructions[self.pointer])
            except InfiniteLoopException:
                success = False
                break
            except IndexError:
                break
        return self.acc, success


def possible_source_generator(instructions):
    """Generate all possible instruction sets by changing one nop or one jmp"""
    for index, ins in enumerate(instructions):
        if ins[0] == "nop":
            new_instructions = [*instructions]
            new_instructions[index] = ("jmp", ins[1])
            yield new_instructions
        if ins[0] == "jmp":
            new_instructions = [*instructions]
            new_instructions[index] = ("nop", ins[1])
            yield new_instructions


def first(rows):
    proc = Processor()
    result, _ = proc.run_program(rows)
    return result


def second(instructions):
    proc = Processor()
    source_generator = possible_source_generator(instructions)
    for source in source_generator:
        result, success = proc.run_program(source)
        if success:
            return result


def main():
    rows = [parse_line_to_instr(line) for line in file_to_lines("inputs/day08.txt")]
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()
