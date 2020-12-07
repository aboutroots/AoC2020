from common import file_to_lines
import re
from collections import defaultdict


def extract_row_rules(row):
    """
    Formatting as below:
    :param row
        "light red bags contain 1 bright white bag, 2 muted yellow bags."
    :returns:
        ('light red', {'bright white': 1, 'muted yellow': 2}
    """
    main_type, children = row.split("contain")
    main_type = " ".join(main_type.split()[:2])
    pattern = r"((\d)\s(\w*\s\w*))"
    matches = re.findall(pattern, children)
    return main_type, {name: int(count) for (_, count, name) in matches}


def memoize(f):
    """cache recursion results."""

    # this dict will store our results. If a result has already been computed,
    # we return value from cache, without the need of re-computing. This dict
    # is preserved among target function calls! (read about closures :) )
    memory = {}

    def wrapper(rule, rules):
        if rule not in memory:
            memory[rule] = f(rule, rules)
        return memory[rule]

    return wrapper

# Functions below are "decorated" with the "memoize" wrapper. This means that the
# "memoize" function can perform action BEFORE and AFTER function returns.

@memoize
def resolve_gold(rule, rules):
    # while recurring, it's important to return as soon as possible
    if "shiny gold" in rules[rule].keys():
        return True

    for child_rule in rules[rule]:
        result_child = resolve_gold(child_rule, rules)
        if result_child:
            return True
    return False


@memoize
def resolve_count(rule, rules):
    counter = 1
    for child_rule, n_bags in rules[rule].items():
        counter = counter + n_bags * resolve_count(child_rule, rules)
    return counter


def first(rules):
    return sum((resolve_gold(rule, rules) for rule in rules))


def second(rules):
    return resolve_count("shiny gold", rules) - 1


def main():
    rows = file_to_lines("inputs/day07.txt")
    # parse rules into nice format
    rules = defaultdict(dict)
    for row in rows:
        key, value = extract_row_rules(row)
        rules[key].update(value)

    print(first(rules))
    print(second(rules))


if __name__ == "__main__":
    main()
