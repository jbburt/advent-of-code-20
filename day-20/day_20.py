"""
this code is embarrassing but I don't have it in me to refactor it today ...
https://adventofcode.com/2020/day/20
"""

import numpy as np
from functools import reduce
from scipy import ndimage

# Read input: square image tiles
with open('day-20/input.txt') as fp:
    lines = fp.read().split('\n')

n = len(lines)
ntiles = n // 12  # each tile 10x10, w/ 2 extra lines in file
tiles = dict()
ids = np.empty(ntiles, dtype=int)

for i in range(ntiles):
    offset = i*12
    # first line contains tile ID
    ids[i] = int(lines[offset].split(' ')[1].strip(':'))
    tiles[ids[i]] = np.array(
        [[x for x in line] for line in lines[offset+1:offset+11]])

left = lambda x: tuple(x[:, 0])
right = lambda x: tuple(x[:, -1])
top = lambda x: tuple(x[0, :])
bottom = lambda x: tuple(x[-1, :])


class Piece:

    def __init__(self, arr, tileid):
        self.x = arr
        self.id = tileid

    def fliplr(self):
        self.x = np.fliplr(self.x)

    def flipud(self):
        self.x = np.flipud(self.x)

    def rotate90(self, k=1):
        """
        Rotate piece by 90 degrees counter-clockwise, k times.
        """
        self.x = np.rot90(self.x, k=k, axes=(0, 1))

    def transpose(self):
        self.x = self.x.T

    def match_right(self, piece):
        """
        Rotate and/or flip the piece such that the RHS of this piece matches
        the LHS of `piece`.

        Parameters
        ----------
        piece : Piece
            test piece

        Returns
        -------
        transformed_piece : Piece
        or
        None

        """

        target = self.right

        if target == piece.left:
            return piece

        elif target == piece.top:
            piece.transpose()
            return piece

        elif target == piece.right:
            piece.fliplr()
            return piece

        elif target == piece.bottom:
            piece.rotate90(k=-1)
            return piece

        elif target == piece.left[::-1]:
            piece.flipud()
            return piece

        elif target == piece.top[::-1]:
            piece.rotate90(k=1)
            return piece

        elif target == piece.right[::-1]:
            piece.rotate90(k=2)
            return piece

        elif target == piece.bottom[::-1]:
            piece.rotate90(k=-1)
            piece.flipud()
            return piece

        else:
            return None

    def match_bottom(self, piece):
        """
        Rotate and/or flip the piece such that the bottom of this piece matches
        the top of `piece`.

        Parameters
        ----------
        piece : Piece

        Returns
        -------
        transformed_piece : Piece

        """

        target = self.bottom

        if target == piece.top:
            return piece

        elif target == piece.right:
            piece.rotate90()
            return piece

        elif target == piece.bottom:
            piece.flipud()
            return piece

        elif target == piece.left:
            piece.rotate90(k=-1)
            piece.fliplr()
            return piece

        elif target == piece.top[::-1]:
            piece.fliplr()
            return piece

        elif target == piece.right[::-1]:
            piece.rotate90(k=1)
            piece.fliplr()
            return piece

        elif target == piece.bottom[::-1]:
            piece.flipud()
            piece.fliplr()
            return piece

        elif target == piece.left[::-1]:
            piece.rotate90(k=-1)
            return piece

        else:
            return None

    def __eq__(self, other):
        return self.id == other.id and np.all(self.x == other.x)

    @property
    def top(self):
        return top(self.x)

    @property
    def bottom(self):
        return bottom(self.x)

    @property
    def left(self):
        return left(self.x)

    @property
    def right(self):
        return right(self.x)


def edges(x):
    xlr = np.fliplr(x)
    xud = np.flipud(x)
    return (top(x), right(x), bottom(x), left(x),
            top(xlr), right(xud), bottom(xlr), left(xud))


tile_edges = dict()
for i, tile_id in enumerate(ids):
    tile_edges[tile_id] = edges(tiles[tile_id])

overlap = np.zeros((ntiles, ntiles))
for i, tile1_id in enumerate(ids):
    for j in range(i+1, ntiles):
        tile2_id = ids[j]
        overlap[i, j] = len(
            set(tile_edges[tile1_id][:4]).intersection(
                set(tile_edges[tile2_id])))

names = ['top', 'right', 'bottom', 'left']
# Problem 1: What do you get if you multiply together the IDs of the four
# corner tiles?
nmatch = np.zeros(144)
edge_matches = []
for i, id1 in enumerate(ids):
    matches = 0
    matched_edges = []
    x = tiles[id1]
    for name, edge1 in zip(names, [top(x), right(x), bottom(x), left(x)]):
        for id2 in ids:
            if id1 != id2:
                for edge2 in tile_edges[id2]:
                    if edge1 == edge2:
                        matches += 1
                        matched_edges.append(name)
    nmatch[i] = matches
    edge_matches.append(matched_edges)

# use the fact that corner tiles have only two matching edges
corner_ids = ids[nmatch == 2]
edge_ids = ids[nmatch == 3]
print(f'problem 1: {reduce(lambda x, y: x*y, corner_ids)}')

# corner_pieces_shared_edges = [
#     x for i, x in enumerate(edge_matches) if len(x) == 2]
# note: the second of four corner pieces has shared right and bottom edges,
# hence it will be used for our initial upper-left corner piece

# ok, now actually reconstruct the image
pieces = {tile_id: Piece(tiles[tile_id], tile_id) for tile_id in ids}

# first, reconstruct the top row
unused_piece_ids = set(ids)
unused_piece_ids.remove(corner_ids[1])
puzzle = np.zeros((12, 12))
puzzle[0, 0] = corner_ids[1]

# fill in top row of puzzle
for j in range(1, 12):
    test_piece = pieces[puzzle[0, j-1]]
    matched_id = None
    for tile_id in unused_piece_ids:  # test all other pieces
        p = pieces[tile_id]
        transformed_piece = test_piece.match_right(p)
        if transformed_piece is not None:  # found a match
            if matched_id is not None:
                raise Exception('found multiple matches')
            matched_id = transformed_piece.id
            pieces[tile_id] = transformed_piece  # update piece
            puzzle[0, j] = transformed_piece.id
    unused_piece_ids.remove(matched_id)
    matched_id = None

# fill in left column of puzzle
for i in range(1, 12):
    test_piece = pieces[puzzle[i-1, 0]]
    matched_id = None
    for tile_id in unused_piece_ids:  # test all other pieces
        p = pieces[tile_id]
        transformed_piece = test_piece.match_bottom(p)
        if transformed_piece is not None:  # found a match
            if matched_id is not None:
                raise Exception('found multiple matches')
            matched_id = transformed_piece.id
            pieces[tile_id] = transformed_piece  # update piece
            puzzle[i, 0] = transformed_piece.id
    unused_piece_ids.remove(matched_id)
    matched_id = None

# fill in the rest of the puzzle
for i in range(1, 12):
    for j in range(1, 12):
        left_piece = pieces[puzzle[i, j-1]]
        top_piece = pieces[puzzle[i-1, j]]
        matched_id = None
        for tile_id in unused_piece_ids:  # test all other pieces
            p = pieces[tile_id]
            tp1 = left_piece.match_right(p)
            if tp1 is not None:  # found a match
                tp2 = top_piece.match_bottom(p)
                if tp2 is not None:
                    if matched_id is not None:
                        raise Exception('found multiple matches')
                    assert tp1 == tp2
                    matched_id = tp1.id
                    pieces[tile_id] = tp1  # update piece
                    puzzle[i, j] = tp1.id
        unused_piece_ids.remove(matched_id)
        matched_id = None

# # sanity check
# for i in range(1, 12):
#     for j in range(1, 12):
#         assert pieces[puzzle[i-1, j]].bottom == pieces[puzzle[i, j]].top
#         assert pieces[puzzle[i, j-1]].right == pieces[puzzle[i, j]].left

image = np.empty((8*12, 8*12), dtype=str)
for i in range(12):
    io = 8*i
    for j in range(12):
        jo = 8*j
        image[io:io+8, jo:jo+8] = pieces[puzzle[i, j]].x[1:-1, 1:-1]

# build monster kernel
monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
parse = lambda x: 1 if x == '#' else 0
k = np.array([list(map(parse, line)) for line in monster.split('\n')])
npix_monster = k.sum()

# compute all orientations of monster kernel
kf = np.fliplr(k)
kernels = [k, np.rot90(k, k=1), np.rot90(k, k=2), np.rot90(k, k=-1),
           kf, np.rot90(kf, k=1), np.rot90(kf, k=2), np.rot90(kf, k=-1)]

# convolve with kernel to find monsters
monster_mask = np.zeros(image.shape)
image_binary = (image == '#').astype(int)
for kernel in kernels:
    ik, jk = kernel.shape
    for i in range(96-ik):
        for j in range(96-jk):
            npixels = (image_binary[i:i+ik, j:j+jk] * kernel).sum()
            if npixels == npix_monster:
                monster_mask[i:i + ik, j:j + jk] += kernel

# mask out the hashtags where I identified a monster
monster_mask = (monster_mask > 0).astype(int)
image_binary[np.where(monster_mask)] = 0

# computing the number of remaining hashtags to find the answer to problem 2
print(f'problem 2: {image_binary.sum()}')
