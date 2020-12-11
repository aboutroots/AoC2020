import itertools
import math

from common import file_to_lines
import time
import cProfile


class XMASParser:
    def __init__(self, preamble):
        self.current_values = []

        self._sums_for_current_values = []

        for num in preamble:
            self._add_new(num)

    def _get_current_options(self):
        unique = set()
        for the_list in self._sums_for_current_values:
            for value in the_list:
                unique.add(value)
        return unique

        # return
        # return set(itertools.chain(*self._sums_for_current_values))

    def _add_new(self, item):
        options_for_num = [item + prev for prev in self.current_values]
        self.current_values.append(item)
        self._sums_for_current_values.append(options_for_num)

    @staticmethod
    def remove(old):
        return old[1:] if old else [],

    def _remove_oldest(self):
        self.current_values = self.current_values[1:]
        self._sums_for_current_values = list(map(self.remove, self._sums_for_current_values))

    def _is_valid(self, num):
        return any(num in list for list in self._sums_for_current_values)

    def tick(self, num, allow_invalid=False):
        if not allow_invalid and not self._is_valid(num):
            return False

        self._remove_oldest()
        self._add_new(num)
        return True


def first(rows, preamble_len=25):
    preamble, data = rows[:preamble_len], rows[preamble_len:]
    parser = XMASParser(preamble)
    for num in data:
        success = parser.tick(num)
        if not success:
            return num


def second(rows):
    target = 1038347917

    for preamble_len in range(2, len(rows) - 1):
        preamble, data = rows[:preamble_len], rows[preamble_len:]
        parser = XMASParser(preamble)
        for num in data:
            parser.tick(num, allow_invalid=True)
            if sum(parser.current_values) == target:
                lower = min(parser.current_values)
                upper = max(parser.current_values)
                return lower + upper



def test():
    results = []
    n_runs = 1000
    rows = [int(row.strip()) for row in file_to_lines("inputs/day09.txt")]
    for _ in range(n_runs):
        start =  time.perf_counter()
        first(rows)
        stop =  time.perf_counter()
        results.append((stop - start))
    print(sum(results) / n_runs)

def main():
    rows = [int(row.strip()) for row in file_to_lines("inputs/day09.txt")]
    # print(first(rows))

    cProfile.run('test()')
    print(first(rows))
    test()




if __name__ == "__main__":
    main()
