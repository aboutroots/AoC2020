import math
from collections import defaultdict

import numpy as np
import plotly.express as px
import re


class Tile:
    def __init__(self, id, rows):
        self.id = id
        self.rows = rows

    def rotate90(self):
        # this rotates COUNTER CLOCKWISE AHHHH SO MUCH PAIN
        self.rows = np.rot90(self.rows)

    def flip_x(self):
        new_rows = []
        for row in self.rows:
            new_rows.append(list(reversed(row)))
        self.rows = new_rows

    def flip_y(self):
        self.rows = list(reversed(self.rows))

    def get_sides(self):
        return {
            "n": self.rows[0],
            "e": [row[-1] for row in self.rows],
            "s": self.rows[-1],
            "w": [row[0] for row in self.rows],
        }

    def side_match(self, other_tile_side):
        other_side_str = "".join(other_tile_side)
        for side_name, side in self.get_sides().items():
            side_str = "".join(side)
            side_str_rev = "".join(reversed(side))
            if side_str == other_side_str or side_str_rev == other_side_str:
                return side_name
        return None

    def __repr__(self):
        return f"<TILE:{self.id}>"


def get_edges_count_map(tiles):
    edges = defaultdict(lambda: 0)
    for tile in tiles:
        for side in tile.get_sides().values():
            edges["".join(side)] += 1
            edges["".join(reversed(side))] += 1
    return edges


def get_corner_tiles(tiles, edges_map):
    corners = []
    for tile in tiles:
        tile_edges = ["".join(side) for side in tile.get_sides().values()]
        loose_side = len([edge for edge in tile_edges if edges_map[edge] == 1])
        if loose_side == 2:
            corners.append(tile)
    return corners


def first(tiles):
    edges = get_edges_count_map(tiles)
    corners = get_corner_tiles(tiles, edges)
    return math.prod([c.id for c in corners])


map_rotations_to_match = {
    "e": ["w", "n", "e", "s"],
    "s": ["n", "e", "s", "w"],
    "w": ["e", "s", "w", "n"],
    "n": ["s", "w", "n", "e"],
}
map_flip_type = {
    "e": "y",
    "s": "x",
    "w": "y",
    "n": "x",
}
map_desired_side = {
    "e": "w",
    "s": "n",
    "w": "e",
    "n": "s",
}

map_next_tile_coords = {
    "e": (1, 0),
    "s": (0, -1),
    "w": (-1, 0),
    "n": (0, 1),
}

monster_yx_list = [
    (0, 18),
    (1, 0),
    (1, 5),
    (1, 6),
    (1, 11),
    (1, 12),
    (1, 17),
    (1, 18),
    (1, 19),
    (2, 1),
    (2, 4),
    (2, 7),
    (2, 10),
    (2, 13),
    (2, 16),
]

colors = {"dragon": "aaff00", "clear": "52bfe3", "rough": "2697bd"}


def update_neighbour_tiles(tile, tiles, edges_map, tiles_map, x, y):
    sides = tile.get_sides()
    tiles_map[(x, y)] = tile
    for direction, side in sides.items():
        side_string = "".join(side)

        # skip "loose" sides
        if edges_map[side_string] == 1:
            continue

        # find neighbour tile for side
        next_tile = next(
            t for t in tiles if t.side_match(side) is not None and tile != t
        )
        if next_tile in tiles_map.values():
            continue

        # rotate neighbour so the sides can match
        direction_in_next = next_tile.side_match(side)
        rotation_count = map_rotations_to_match[direction].index(direction_in_next)
        for _ in range(rotation_count):
            next_tile.rotate90()

        # flip neighbour if needed
        desired_side_name = map_desired_side[direction]
        side_in_next = next_tile.get_sides()[desired_side_name]
        need_to_flip = side_string == "".join(reversed(side_in_next))
        if need_to_flip:
            if map_flip_type[direction] == "x":
                next_tile.flip_x()
            else:
                next_tile.flip_y()

        # ok we are done, the neighbour is placed correctly. Now onto HIS neighbours...
        next_x_add, next_y_add = map_next_tile_coords[direction]
        update_neighbour_tiles(
            next_tile, tiles, edges_map, tiles_map, x + next_x_add, y + next_y_add
        )
    return tiles_map


def check_if_sea_monster_tail(x, y, big_map):
    try:
        found = all([big_map[y + a][x + b] == "#" for a, b in monster_yx_list])
    except IndexError:
        return False
    return found


def plot(graphic_map):
    # convert hex colors to rgb
    as_rgb = []
    for row in graphic_map:
        simple_list = []
        for value in row:
            simple_list.append([int(value[i : i + 2], 16) for i in (0, 2, 4)])
        as_rgb.append(simple_list)

    img = np.array(as_rgb, dtype=np.uint8)
    fig = px.imshow(img)
    # plot
    fig.show()


def second(tiles):
    edges = get_edges_count_map(tiles)
    corners = get_corner_tiles(tiles, edges)
    tiles_map = {}
    # build tiles map recursively
    update_neighbour_tiles(corners[0], tiles, edges, tiles_map, 0, 0)

    # normalize tiles - the indexation can start from value below 0.
    # Make them start from 0
    min_tiles_x = min(tiles_map.keys(), key=lambda t: t[0])[0]
    min_tiles_y = min(tiles_map.keys(), key=lambda t: t[1])[1]
    max_tiles_x = max(tiles_map.keys(), key=lambda t: t[0])[0]
    max_tiles_y = max(tiles_map.keys(), key=lambda t: t[1])[1]

    if min_tiles_x < 0 or min_tiles_y < 0:
        updated_map = {}
        add_to_x = -min_tiles_x
        add_to_y = -min_tiles_y
        for x, y in tiles_map.keys():
            updated_map[(x + add_to_x, y + add_to_y)] = tiles_map[(x, y)]
        tiles_map = updated_map
        max_tiles_x = max(tiles_map.keys(), key=lambda t: t[0])[0]
        max_tiles_y = max(tiles_map.keys(), key=lambda t: t[1])[1]

    # build one big map
    len_tiles_x = max_tiles_x + 1
    len_tiles_y = max_tiles_y + 1
    len_tile_y = len(tiles[0].rows) - 2  # remember to strip "borders"
    len_tile_x = len(tiles[0].rows[0]) - 2
    big_map = np.full((len_tiles_y * len_tile_y, len_tiles_x * len_tile_x), "X")

    for tile_y in range(0, len_tiles_y):
        for tile_x in range(0, len_tiles_x):
            tile = tiles_map[(tile_x, tile_y)]
            for idx_y, row in enumerate(tile.rows[1:-1]):  # remember to strip "borders"
                for idx_x, value in enumerate(row[1:-1]):
                    final_y = idx_y + (len_tiles_y - 1 - tile_y) * len_tile_y
                    final_x = idx_x + tile_x * len_tile_x
                    big_map[final_y][final_x] = value

    # find correct map orientation (the one that has dragons visible)
    correct_map = None
    roughness = 0
    for flip_y in range(2):
        for rotation in range(4):
            monsters = 0

            # find and draw dragons
            placeholder = "xxxxxx"
            graphic_map = np.full(
                (len_tiles_y * len_tile_y, len_tiles_x * len_tile_x), placeholder
            )
            for y, row in enumerate(big_map):
                for x in range(len(row)):
                    if graphic_map[y][x] == placeholder:
                        has_monster_tail = check_if_sea_monster_tail(x, y, big_map)
                        if big_map[y][x] == "#":
                            graphic_map[y][x] = colors["rough"]
                        else:
                            graphic_map[y][x] = colors["clear"]
                        if has_monster_tail:
                            monsters += 1
                            for a, b in monster_yx_list:
                                graphic_map[y + a][x + b] = colors["dragon"]
            if monsters:
                # get rough water count
                roughness = sum(
                    1
                    for row in graphic_map
                    for value in row
                    if value == colors["rough"]
                )
                correct_map = graphic_map

            # try again by rotating big map
            big_map = np.rot90(big_map)
        # try again by flipping the big map
        big_map = list(reversed(big_map))

    print(roughness)
    plot(correct_map)


def main():
    with open("inputs/day20.txt") as file:
        tiles_data = file.read().split("\n\n")
    tiles = []
    for tile in tiles_data:
        header, *lines = tile.split("\n")
        num = int(re.search(r"\d+", header).group(0))
        tiles.append(Tile(id=num, rows=[list(line) for line in lines]))

    print(first(tiles))
    second(tiles)


if __name__ == "__main__":
    main()
