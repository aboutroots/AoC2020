import re
from collections import namedtuple

from typing import Dict, List

Rule = namedtuple("Rule", "min1 max1 min2 max2")

RulesDict = Dict[str, Rule]
Ticket = List[int]
TicketList = List[Ticket]


def parse_input(filename: str) -> (RulesDict, Ticket, TicketList):
    with open(filename, "r") as file:
        content = file.read()
    rules_raw, mine_raw, other_raw = content.split("\n\n")
    rules = {}
    for r in rules_raw.split("\n"):
        s = re.search(r"(.*): (\d*)-(\d*) or (\d*)-(\d*)", r)
        key = s.group(1)
        value = Rule(*[int(val) for val in s.groups()[1:]])
        rules[key] = value

    _, mine = mine_raw.split("\n")
    mine = [int(val) for val in mine.split(",")]

    other = []
    for t in other_raw.split("\n")[1:]:
        other.append([int(val) for val in t.split(",")])

    return rules, mine, other


def check_rule(rule: Rule, val: int) -> bool:
    return rule.min1 <= val <= rule.max1 or rule.min2 <= val <= rule.max2


def get_invalid_values_for_ticket(rules: RulesDict, ticket: Ticket) -> List[int]:
    invalid_list = []
    for value in ticket:
        if any(check_rule(rule, value) for rule in rules.values()):
            continue
        invalid_list.append(value)
    return invalid_list


def resolve_columns(rules: RulesDict, tickets: TicketList) -> Dict[int, str]:
    """
    Alg:
    1. If column matches only one rule, this is THE rule for this column.
    2. Save result and remove this column and this rule from equation.
    3. Repeat until all columns have matching rules.
    """
    row_len = len(tickets[0])
    column_results = {}

    while len(column_results) < row_len:
        for column_idx in range(row_len):
            if column_idx in column_results:
                # this column is already resolved
                continue

            column = [t[column_idx] for t in tickets]
            matches = []
            for rule_name, rule_values in rules.items():
                if all(check_rule(rule_values, value) for value in column):
                    matches.append(rule_name)
            if len(matches) == 1:
                rule = matches[0]
                column_results[column_idx] = rule
                # we don't need this rule anymore
                del rules[rule]
    return column_results


def first(rules: RulesDict, other: TicketList) -> int:
    invalid_sum = 0
    for ticket in other:
        invalid_sum += sum(get_invalid_values_for_ticket(rules, ticket))
    return invalid_sum


def second(rules: RulesDict, mine: Ticket, other: TicketList) -> int:
    valid_other = []
    for ticket in other:
        if not get_invalid_values_for_ticket(rules, ticket):
            valid_other.append(ticket)

    columns_map = resolve_columns(rules, valid_other)
    result = 1
    for column_idx, value in enumerate(mine):
        if "departure" in columns_map[column_idx]:
            result *= value
    return result


def main():
    rules, mine, other = parse_input("inputs/day16.txt")
    print(first(rules, other))
    print(second(rules, mine, other))


if __name__ == "__main__":
    main()
