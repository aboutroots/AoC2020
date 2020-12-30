import itertools
import math
from collections import defaultdict

from common import file_to_lines
import numpy as np
import re


class Tile:
    def __init__(self, id, rows):
        self.id = id
        self.rows = rows
        self.neighbours = {
            "n": None,
            "e": None,
            "s": None,
            "w": None,
        }

    @property
    def has_all_neighbours(self):
        return all(n is not None for n in self.neighbours.values())

    @property
    def has_any_neighbours(self):
        return any(n is not None for n in self.neighbours.values())

    @property
    def neighbours_count(self):
        return sum(1 if v is not None else 0 for v in self.neighbours.values())

    def reset_neighbours(self):
        for direction, n in self.neighbours.items():
            if n is not None:
                side = self.get_sides()[direction]
                other_dir = n.side_match(side)
                n.neighbours[other_dir] = None
        self.neighbours = {
            "n": None,
            "e": None,
            "s": None,
            "w": None,
        }

    def flip_x(self):
        self.reset_neighbours()
        new_rows = []
        for row in self.rows:
            new_rows.append(list(reversed(row)))
        self.rows = new_rows

    def rotate90(self):
        self.reset_neighbours()
        self.rows = np.rot90(self.rows)

    def flip_y(self):
        self.reset_neighbours()
        self.rows = list(reversed(self.rows))

    def get_sides(self):  # n e s w
        return {
            "n": self.rows[0],
            "e": [row[-1] for row in self.rows],
            "s": self.rows[-1],
            "w": [row[0] for row in self.rows],
        }

    def side_match(self, other_tile_side):
        for side_name, side in self.get_sides().items():
            # print(''.join(side), ''.join(other_tile_side))
            if ''.join(side) == ''.join(other_tile_side):
                return side_name, False
            if ''.join(list(reversed(side))) == ''.join(other_tile_side):
                return side_name, True
        return None

    def __repr__(self):
        return f"TILE<{self.id}>"


def compute_neighbours(tile, tiles):
    if not tile.has_all_neighbours:
        for direction, neighbour in tile.neighbours.items():
            if neighbour is not None:
                continue
            side = tile.get_sides()[direction]
            for other_tile in tiles:
                if other_tile == tile or other_tile.has_all_neighbours:
                    continue
                side_match = other_tile.side_match(side)
                if side_match:
                    tile.neighbours[direction] = other_tile
                    other_tile.neighbours[side_match] = tile
                    break


def get_edges_count_map(tiles):
    edges = defaultdict(lambda: 0)
    for tile in tiles:
        for side in tile.get_sides().values():
            edge = "".join(side)
            edges[edge] += 1

            rev = "".join(reversed(side))
            edges[rev] += 1
    return edges


def get_corner_tiles(tiles, edges_map):
    corners = []
    for tile in tiles:
        tile_edges = ["".join(side) for side in tile.get_sides().values()]
        loose = len([edge for edge in tile_edges if edges_map[edge] == 1])
        if loose == 2:
            corners.append(tile)
    return corners


def first(tiles):
    edges = get_edges_count_map(tiles)
    corners = get_corner_tiles(tiles, edges)
    return math.prod([c.id for c in corners])


def get_tile_right_of(last_tile, tiles):
    common_edge = last_tile.get_sides()["e"]
    next_tile = [
        tile for tile in tiles if tile.side_match(common_edge) and tile != last_tile
    ][0]
    direction_in_other, rev = next_tile.side_match(common_edge)
    # if direction_in_other == 'w' and not rev:
    #     continue
    if direction_in_other == "w" and rev:
        next_tile.flip_y()
    elif direction_in_other == "e" and not rev:
        next_tile.flip_x()
    elif direction_in_other == "e" and rev:
        next_tile.rotate90()
        next_tile.rotate90()
    elif direction_in_other == "n" and not rev:
        next_tile.flip_x()
        next_tile.rotate90()
        next_tile.rotate90()
        next_tile.rotate90()
    elif direction_in_other == "n" and rev:
        next_tile.rotate90()
        next_tile.rotate90()
        next_tile.rotate90()
    elif direction_in_other == "s" and not rev:
        next_tile.rotate90()
    elif direction_in_other == "s" and rev:
        next_tile.flip_x()
        next_tile.rotate90()
    return next_tile


def get_tile_down_of(last_tile, tiles):
    common_edge = last_tile.get_sides()["s"]
    next_tile = [
        tile for tile in tiles if tile.side_match(common_edge) and tile != last_tile
    ][0]
    direction_in_other, rev = next_tile.side_match(common_edge)
    # if direction_in_other == 'w' and not rev:
    #     continue
    if direction_in_other == "n" and rev:
        next_tile.flip_x()
    elif direction_in_other == "e" and not rev:
        next_tile.rotate90()
        next_tile.rotate90()
        next_tile.rotate90()
    elif direction_in_other == "e" and rev:
        next_tile.flip_y()
        next_tile.rotate90()
        next_tile.rotate90()
        next_tile.rotate90()
    elif direction_in_other == "w" and not rev:
        next_tile.rotate90()
    elif direction_in_other == "w" and rev:
        next_tile.flip_y()
        next_tile.rotate90()
    elif direction_in_other == "s" and not rev:
        next_tile.flip_y()
    elif direction_in_other == "s" and rev:
        next_tile.rotate90()
        next_tile.rotate90()
    return next_tile


dir_map_rotation = {
    'e': ['w', 's', 'e', 'n'],
    's': ['n', 'w', 's', 'e'],
    'w': ['e', 'n', 'w', 's'],
    'n': ['s', 'e', 'n', 'w'],
}
dir_map_flip = {
    'e': 'y',
    's': 'x',
    'w': 'y',
    'n': 'x',
}

def update_next_tiles(tile, tiles, edges_map, tiles_map, x, y):
    sides = tile.get_sides()
    tiles_map[(x, y)] = tile
    for direction, side in sides.items():
        if edges_map[''.join(side)] == 1:
            continue
        next_tile = [t for t in tiles if t.side_match(side) is not None and tile != t][0]
        if next_tile in tiles_map.values():
            continue
        direction_in_next, rev = next_tile.side_match(side)
        rotation_count = dir_map_rotation[direction].index(direction_in_next)
        for _ in range(rotation_count):
            next_tile.rotate90()
        if rev:
            if dir_map_flip[direction] == 'x':
                next_tile.flip_x()
            else:
                next_tile.flip_y()
        if direction == 'e':
            update_next_tiles(next_tile, tiles, edges_map, tiles_map, x + 1, y)
        if direction == 's':
            update_next_tiles(next_tile, tiles, edges_map, tiles_map, x, y - 1)
        if direction == 'w':
            update_next_tiles(next_tile, tiles, edges_map, tiles_map, x - 1, y)
        if direction == 'n':
            update_next_tiles(next_tile, tiles, edges_map, tiles_map, x, y + 1)
    return tiles_map







def build_tiles_map(tiles, edges_map):
    tiles_map = {}
    update_next_tiles(tiles[0], tiles, edges_map, tiles_map, 0, 0)
    return tiles_map

    # map_len = int(math.sqrt(len(tiles)))
    #
    # tiles_map = []
    # for y in range(map_len):
    #     print(y)
    #     if y == 0:
    #         first_tile = corners[3]
    #         north_side = first_tile.get_sides()['n']
    #         if edges_map[''.join(north_side)] != 1:
    #             first_tile.flip_y()
    #         west_side = first_tile.get_sides()['w']
    #         if edges_map[''.join(west_side)] != 1:
    #             first_tile.flip_x()
    #         row = [first_tile]
    #     else:
    #         last_tile = tiles_map[y - 1][0]
    #         row = [get_tile_down_of(last_tile, tiles)]
    #
    #     tiles_map.append(row)
    #     for x in range(map_len - 1):
    #         print('x', x)
    #         last_tile = tiles_map[-1][-1]
    #         next_tile = get_tile_right_of(last_tile, tiles)
    #         tiles_map[y].append(next_tile)
    # return tiles_map


def second(tiles):
    edges = get_edges_count_map(tiles)
    corners = get_corner_tiles(tiles, edges)
    tiles_map = build_tiles_map(tiles, edges)
    # print(sorted(tiles_map.items()))
    min_x = min(tiles_map.keys(), key=lambda t: t[0])[0]
    max_x = max(tiles_map.keys(), key=lambda t: t[0])[0]
    min_y = min(tiles_map.keys(), key=lambda t: t[1])[1]
    max_y = max(tiles_map.keys(), key=lambda t: t[1])[1]

    print(len(tiles), len(tiles_map))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(tiles_map[(x, y)], end='')
        print()


def main():
    with open("inputs/day20.txt") as file:
        tiles_data = file.read().split("\n\n")
    tiles = []
    for tile in tiles_data:
        header, *lines = tile.split("\n")
        num = int(re.search(r"\d+", header).group(0))
        tiles.append(Tile(id=num, rows=[list(line) for line in lines]))

    # print(first(tiles))
    print(second(tiles))


if __name__ == "__main__":
    main()
