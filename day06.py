from collections import Counter


def get_count(group):
    return len(set(group.replace('\n', '')))


def get_count2(group):
    c = Counter(group)
    n_people = c['\n'] + 1
    return sum([count == n_people for (answer, count) in c.items()])


def first(groups):
    return sum([get_count(group) for group in groups])


def second(groups):
    return sum([get_count2(group) for group in groups])


def main():
    with open("inputs/day06.txt") as file:
        body = file.read()
    groups = body.split('\n\n')  # hehe thanks Filip
    print(first(groups))
    print(second(groups))


if __name__ == "__main__":
    main()
