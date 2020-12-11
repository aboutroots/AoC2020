from common import file_to_lines


def get_seat(x, y, initial_layout):
    if x < 0 or y < 0:
        return "X"
    try:
        return initial_layout[y][x]
    except IndexError:
        return "X"


def get_first_seat_in_view(
    start_x, start_y, x_direction, y_direction, initial_layout, scope
):
    x = start_x
    y = start_y
    scope_counter = 0

    while True:
        scope_counter += 1
        x = x + (1 * x_direction)
        y = y + (1 * y_direction)
        next_seat = get_seat(x, y, initial_layout)
        if next_seat != ".":
            return next_seat

        if scope and scope_counter >= scope:
            return next_seat


def get_adjacent_occupancy_in_view(x, y, initial_layout, scope=None):
    directions = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ]
    adjacent_occupancy = [
        get_first_seat_in_view(x, y, dir_x, dir_y, initial_layout, scope)
        for dir_x, dir_y in directions
    ]
    return adjacent_occupancy


def compute_round(initial_layout, scope=1, max_occupancy=4):
    new_layout = []
    for y, row in enumerate(initial_layout):
        new_layout.append([])
        for x, col in enumerate(initial_layout):
            adjacent_occupancy = get_adjacent_occupancy_in_view(
                x, y, initial_layout, scope
            )

            seat = get_seat(x, y, initial_layout)
            # rules for new seat
            if seat == "L" and all(n in [".", "L", "X"] for n in adjacent_occupancy):
                new_layout[y].append("#")
            elif (
                seat == "#"
                and sum(n == "#" for n in adjacent_occupancy) >= max_occupancy
            ):
                new_layout[y].append("L")
            else:
                new_layout[y].append(seat)
    return new_layout


def get_occuped_sum(layout, scope, max_neighbours_occupancy):
    while True:
        new_layout = compute_round(layout, scope, max_neighbours_occupancy)
        if str(new_layout) == str(layout):
            occupied = sum([row.count("#") for row in new_layout])
            return occupied
        layout = new_layout


def first(layout):
    return get_occuped_sum(layout, scope=1, max_neighbours_occupancy=4)


def second(layout):
    return get_occuped_sum(layout, scope=None, max_neighbours_occupancy=5)


def main():
    rows = [list(line.strip()) for line in file_to_lines("inputs/day11.txt")]
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()
