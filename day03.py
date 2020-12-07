from common import file_to_lines
import math


def check_tree_encounter_on_index(row, index):
    real_index = index % len(row.strip())
    return row[real_index] == "#"


def compute_slide(rows, right, down):
    encounters = 0

    for row_index in range(down, len(rows), down):
        row = rows[row_index]
        position = (row_index // down) * right
        encounters = encounters + check_tree_encounter_on_index(row, position)
    return encounters


def first(rows):
    return compute_slide(rows, right=3, down=1)


def second(rows):
    return math.prod(
        [
            compute_slide(rows, right=1, down=1),
            compute_slide(rows, right=3, down=1),
            compute_slide(rows, right=5, down=1),
            compute_slide(rows, right=7, down=1),
            compute_slide(rows, right=1, down=2),
        ]
    )




def main():
    rows = file_to_lines("inputs/day03.txt")
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()
