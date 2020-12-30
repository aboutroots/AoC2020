import re


def memoize(f):
    memory = {}

    def wrapper(rule, rules):
        if rule not in memory:
            memory[rule] = f(rule, rules)
        return memory[rule]

    return wrapper


@memoize
def resolve_rule(rule, rules_dict):
    value = rules_dict[rule]
    if value in ["a", "b"]:
        return value

    new_groups = []
    for group in value:
        new_group = []
        for child in group:
            new_group.append(resolve_rule(child, rules_dict))

        if all(elem in ["a", "b"] for elem in new_group):
            new_group = "".join(new_group)
        else:
            new_group = f"({''.join(new_group)})"
            # new_group = '|'.join(new_group)
        new_groups.append(new_group)

    return f"({'|'.join(new_groups)})"


def first(rules_dict, messages):
    resolved = resolve_rule("0", rules_dict)
    counter = 0
    for idx, message in enumerate(messages):
        fullmatch = re.fullmatch(resolved, message)
        match = fullmatch.group(0) if fullmatch else None
        if match == message:
            counter += 1
    return counter


def second(rules_dict, messages):
    # prepare a couple recursive iterations.
    rules_dict["8"] = [["42"], ["42", "1000"]]
    rules_dict["11"] = [["42", "31"], ["42", "1001", "31"]]
    i = 1000
    for _ in range(max(len(msg) for msg in messages)):
        rules_dict[f"{i}"] = [["42"], ["42", f"{i+2}"]]
        rules_dict[f"{i + 1}"] = [["42", "31"], ["42", f"{i+3}", "31"]]
        i += 2
    rules_dict[f"{i}"] = [["42"], ["42"]]
    rules_dict[f"{i + 1}"] = [["42", "31"], ["42", "31"]]

    resolved = resolve_rule("0", rules_dict)
    counter = 0
    for idx, message in enumerate(messages):
        print(idx, len(messages))
        fullmatch = re.fullmatch(resolved, message)
        match = fullmatch.group(0) if fullmatch else None
        if match == message:
            counter += 1
    return counter


def main():
    with open("inputs/day19.txt") as file:
        rules, messages = file.read().split("\n\n")
    messages = messages.split("\n")
    rules_dict = {}
    for rule in rules.split("\n"):
        key, other = rule.split(": ")
        if "a" in other or "b" in other:
            groups = other.strip('"')
        else:
            groups = [re.findall(r"\d+", g) for g in other.split(" | ")]
        rules_dict[key] = groups

    print(first(rules_dict, messages))
    print(second(rules_dict, messages))


if __name__ == "__main__":
    main()
