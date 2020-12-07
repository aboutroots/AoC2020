from common import file_to_lines
import re


def get_seat_id(row):
    with_ones = re.sub(r"[BR]", "1", row)
    with_zeroes = re.sub(f"[LF]", "0", with_ones)
    return int(with_zeroes, 2)


def first(rows):
    return max([get_seat_id(row.strip()) for row in rows])


def second(rows):
    ids = sorted([get_seat_id(row.strip()) for row in rows])
    for index, seat_id in enumerate(ids):
        if ids[index + 1] == seat_id + 2:
            return seat_id + 1


def main():
    rows = file_to_lines("inputs/day05.txt")
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()
