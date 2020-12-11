from collections import defaultdict
from common import file_to_lines


def first(adapters):
    occurrences = defaultdict(int)
    for index, adapter in enumerate(adapters):
        diff = adapter - adapters[index - 1] if index > 0 else adapter
        occurrences[diff] += 1
    # add built in adapter
    occurrences[3] += 1
    return occurrences[3] * occurrences[1]


def memoize(f):
    # you know this trick already, dont ya
    memory = {}

    def wrapper(rule, rules):
        if rule not in memory:
            memory[rule] = f(rule, rules)
        return memory[rule]

    return wrapper


@memoize
def get_combinations(adapter, possibilities):
    if len(possibilities[adapter]) == 0:
        return 1

    poss_sum = 0
    for child_rule in possibilities[adapter]:
        poss_sum = poss_sum + get_combinations(child_rule, possibilities)
    return poss_sum


def second(adapters):
    adapters.insert(0, 0)
    possibilities_map = defaultdict(list)
    for index, adapter in enumerate(adapters):
        possible_next_adapters = [
            next_adapter
            for next_adapter in adapters[index + 1: index + 4]
            if next_adapter - adapter < 4
        ]
        possibilities_map[adapter] = possible_next_adapters

    return get_combinations(adapters[0], possibilities_map)


def main():
    # sorting is really useful in this one
    rows = sorted([int(x) for x in file_to_lines("inputs/day10.txt")])
    print(first(rows))
    import time;

    start = time.perf_counter()
    print(second(rows))
    end = time.perf_counter()
    print(end - start)


if __name__ == "__main__":
    main()
