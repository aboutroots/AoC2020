from common import file_to_lines

# e, se, sw, w, nw, ne
# 0  1   2   3   4   5
moves_map = {
    "0": (1, -1, 0),
    "1": (0, -1, 1),
    "2": (-1, 0, 1),
    "3": (-1, 1, 0),
    "4": (0, 1, -1),
    "5": (1, 0, -1),
}

def row_to_moves(row):

    row = row.replace('se', '1').replace('sw', '2').replace('nw', '4').replace('ne', '5').replace('e', '0').replace('w', '3')
    moves = list(row.strip())
    return moves

def get_tiles_map(paths):
    # 0 - white, 1 - dark
    tiles = {
        (0, 0, 0): 0
    }
    for path in paths:
        moves = row_to_moves(path)
        tile = [0, 0, 0]
        for move in moves:

            xyz_add = moves_map[move]
            for coord in range(3):
                tile[coord] += xyz_add[coord]

        tile = tuple(tile)
        if tile in tiles:
            tiles[tile] = 1 - tiles[tile]
        else:
            tiles[tile] = 1
    return tiles



def first(paths):
    tiles = get_tiles_map(paths)
    return sum(tiles.values())


def get_neighbours(tile):
    n = []
    for neighbour_xyz in moves_map.values():
        neighbour_tile = list(tile)
        for coord in range(3):
            neighbour_tile[coord] += neighbour_xyz[coord]
        n.append(tuple(neighbour_tile))
    return n


def second(paths):
    tiles = get_tiles_map(paths)
    next_tiles = {}
    for tile in tiles:
        for n in get_neighbours(tile):
            if n not in tiles:
                next_tiles[n] = 0
    tiles.update(next_tiles)

    for _ in range(100):
        next_tiles = dict(tiles)
        for tile, tile_value in tiles.items():
            sum_black = 0
            for neighbour in get_neighbours(tile):
                if neighbour in tiles:
                    sum_black += tiles[neighbour]
                else:
                    next_tiles[neighbour] = 0

            if tile_value == 1 and (sum_black == 0 or sum_black > 2):
                next_tiles[tile] = 0
            elif tile_value == 0 and sum_black == 2:
                next_tiles[tile] = 1
            else:
                next_tiles[tile] = tile_value


        tiles = next_tiles
    return sum(tiles.values())


def main():
    paths = file_to_lines("inputs/day24.txt")
    print(first(paths))
    print(second(paths))


if __name__ == "__main__":
    main()
