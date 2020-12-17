from common import file_to_lines
import itertools
from typing import Tuple, Set

Vector = Tuple[int, int, int, int]  # x y z w


def get_neighbours(vector: Vector, fourth_dim: bool) -> Set[Vector]:
    x, y, z, w = vector
    vectors = [
        [x - 1, x, x + 1],
        [y - 1, y, y + 1],
        [z - 1, z, z + 1],
        [0],
    ]
    if fourth_dim:
        vectors[-1] = [w - 1, w, w + 1]
    n = set(itertools.product(*vectors))
    n.remove(vector)
    return n


def run(active_cells_start: Set[Vector], use_fourth_dim=False) -> int:
    active_cells_before = active_cells_start
    for cycle in range(6):
        active_cells_after = set()
        affected_cells = itertools.chain.from_iterable(
            get_neighbours(c, use_fourth_dim) for c in active_cells_before
        )
        # use set to make neighbours unique
        unique_affected_cells = {*affected_cells, *active_cells_before}
        for coordinates in unique_affected_cells:
            is_active = coordinates in active_cells_before
            neighbours = get_neighbours(coordinates, use_fourth_dim)
            active_sum = len(neighbours.intersection(active_cells_before))

            cond1 = is_active and active_sum in [2, 3]
            cond2 = not is_active and active_sum == 3
            if cond1 or cond2:
                active_cells_after.add(coordinates)

        active_cells_before = active_cells_after
    return len(active_cells_before)


def main():
    rows = file_to_lines("inputs/day17.txt")
    active_cells: Set[Vector] = set()
    for y, row in enumerate(rows):
        for x, value in enumerate(row.strip()):
            if value == "#":
                active_cells.add((x, y, 0, 0))

    print(run(active_cells))
    print(run(active_cells, use_fourth_dim=True))


if __name__ == "__main__":
    main()
