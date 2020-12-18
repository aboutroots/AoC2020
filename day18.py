import math

from common import file_to_lines
import re


def compute_enclosed_group_left_to_right(group):
    group = group.strip("()")
    result = 0
    operator = "+"
    for item in group.split(" "):
        if item in ["*", "+"]:
            operator = item
        else:
            result = result + int(item) if operator == "+" else result * int(item)
    return result


def compute_multiplication(problem):
    if "*" in problem:
        numbers = re.findall(r"\d+", problem)
        result = math.prod(int(n) for n in numbers)
        return result
    return problem


def compute_addition(problem):
    problem = problem.strip("()")
    while "+" in problem:
        enclosed_groups = re.findall(r"\d+ \+ \d+", problem)
        for group in enclosed_groups:
            numbers = re.findall(r"\d+", group)
            group_result = sum(int(n) for n in numbers)
            problem = f"{group_result}".join(problem.split(group))
    return compute_multiplication(problem)


def compute_parens(problem, left_to_right=False):
    while "(" in problem:
        enclosed_groups = re.findall(r"\([\d\+\*\s]+\)", problem)
        for group in enclosed_groups:
            if left_to_right:
                group_result = compute_enclosed_group_left_to_right(group)
            else:
                group_result = compute_addition(group)
            problem = f"{group_result}".join(problem.split(group))

    if left_to_right:
        return compute_enclosed_group_left_to_right(problem)
    return compute_addition(problem)


rows = file_to_lines("inputs/day18.txt")
print(sum(int(compute_parens(row, left_to_right=True)) for row in rows))
print(sum(int(compute_parens(row)) for row in rows))
