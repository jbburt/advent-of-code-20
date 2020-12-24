"""
https://adventofcode.com/2020/day/24
"""

from collections import defaultdict
from re import findall

# Read input: instructions for flipping tiles
with open('day-24/input.txt') as fp:
    lines = [findall('e|w|se|sw|ne|nw', line) for line in fp.read().split('\n')]

# southeast, southwest, west, northwest, and northeast. These directions are
# given in your list, respectively, as e, se, sw, w, nw, and ne. A tile is
# identified by a series of these directions with no delimiters; for example,
# esenee identifies the tile you land on if you start at the reference tile
# and then move one tile east, one tile southeast, one tile northeast, and one
# tile east.

# direction : (dx, dy, dz) (using cube coordinates)
mapping = {'e': (1, -1, 0),
           'se': (0, -1, 1),
           'sw': (-1, 0, 1),
           'w': (-1, 1, 0),
           'nw': (0, 1, -1),
           'ne': (1, 0, -1)}

# Problem 1: Go through the renovation crew's list and determine which tiles
# they need to flip. After all of the instructions have been followed, how
# many tiles are left with the black side up?
tile_is_flipped = defaultdict(int)
for steps in lines:
    tile = (sum(deltas) for deltas in zip(*[mapping[step] for step in steps]))
    tile_is_flipped[tile] = int(not tile_is_flipped[tile])
print(f'problem 1: {sum(tile_is_flipped.values())}')


# Problem 2: The tile floor in the lobby is meant to be a living art exhibit.
# Every day, the tiles are all flipped according to the following rules:
# Any black tile with zero or more than 2 black tiles immediately
# adjacent to it is flipped to white.
# Any white tile with exactly 2 black tiles immediately adjacent to it is
# flipped to black.


for day in range(1, 101):
    tiles_to_flip = list()
    tiles = set((x+dx, y+dy, z+dz) for (x, y, z) in tile_is_flipped.keys()
                for (dx, dy, dz) in mapping.values())
    for tile in tiles:
        if tile not in tile_is_flipped:
            tile_is_flipped[tile] = 0
    items = list(tile_is_flipped.items())
    for tile, color in items:
        x, y, z = tile
        n_black_neighbors = sum(
            tile_is_flipped[
                (x+dx, y+dy, z+dz)] for (dx, dy, dz) in mapping.values())
        if color:  # this tile is black
            if not n_black_neighbors or n_black_neighbors > 2:
                tiles_to_flip.append(tile)
        else:  # white tile
            if n_black_neighbors == 2:
                tiles_to_flip.append(tile)
    for tile in tiles_to_flip:
        tile_is_flipped[tile] = int(not tile_is_flipped[tile])
    # print(day, sum(tile_is_flipped.values()))
print(f'problem 2: {sum(tile_is_flipped.values())}')
