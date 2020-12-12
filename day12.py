import math
from collections import namedtuple

from common import file_to_lines


def compute_move(direction_tuple, facing=0):
    key, value = direction_tuple
    facings = ["E", "S", "W", "N"]  # 0, 1, 2, 3
    Modifiers = namedtuple("Modifiers", "real imag face")
    movement_rules_map = {
        "N": Modifiers(0, 1, 0),
        "S": Modifiers(0, -1, 0),
        "E": Modifiers(1, 0, 0),
        "W": Modifiers(-1, 0, 0),
        "L": Modifiers(0, 0, -1),
        "R": Modifiers(0, 0, +1),
    }

    if key == "F":
        rule_key = facings[facing]
        rule = movement_rules_map[rule_key]
    else:
        rule = movement_rules_map[key]

    move = complex(rule.real * value, rule.imag * value)
    turn = rule.face * (value // 90)
    return move, turn


def first(directions):
    position = 0 + 0j
    facing = 0
    for direction_tuple in directions:
        move, turn = compute_move(direction_tuple, facing)
        position = position + move
        facing = (facing + turn) % 4

    dist = abs(position.real) + abs(position.imag)
    return dist


def rotate_around_origin(origin, point, degrees, sign):
    angle = sign * math.radians(degrees)
    ox, oy = origin.real, origin.imag
    px, py = point.real, point.imag

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return complex(math.floor(qx), math.floor(qy))


def second(directions):
    ship_position = 0 + 0j
    waypoint_position = 10 + 1j
    for direction_tuple in directions:
        key, value = direction_tuple
        if key == "F":
            # move to waypoint
            diff = waypoint_position - ship_position
            ship_move = value * diff
            ship_position = ship_position + ship_move

            # move waypoint itself
            waypoint_position = ship_position + diff

        elif key in ["L", "R"]:
            # rotate waypoint around the ship
            sign = 1 if direction_tuple[0] == "L" else -1
            waypoint_position = rotate_around_origin(
                ship_position, waypoint_position, value, sign
            )
        else:
            # move waypoint
            waypoint_move, _ = compute_move(direction_tuple)
            waypoint_position = waypoint_position + waypoint_move

    dist = abs(ship_position.real) + abs(ship_position.imag)
    return dist


def main():
    rows = [(row[0], int(row[1:].strip())) for row in file_to_lines("inputs/day12.txt")]
    print(first(rows))
    print(second(rows))


if __name__ == "__main__":
    main()
