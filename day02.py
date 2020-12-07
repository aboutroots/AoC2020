from common import file_to_lines
from collections import Counter


def parse_line(line):
    return line.strip().replace("-", " ").replace(":", "").split(" ")


def first(rows):
    count = 0
    for line in rows:
        rule_min, rule_max, letter, password = parse_line(line)
        letter_counter = Counter(password)
        if int(rule_min) <= letter_counter[letter] <= int(rule_max):
            count = count + 1
    return count


def second(rows):
    count = 0
    for line in rows:
        rule_a, rule_b, letter, password = parse_line(line)
        length = len(password)
        index_a = int(rule_a) - 1
        index_b = int(rule_b) - 1

        is_first = index_a < length and password[index_a] == letter
        is_second = index_b < length and password[index_b] == letter

        if is_first ^ is_second:
            count = count + 1
    return count


def main():
    rows = file_to_lines("inputs/day02.txt")
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()
