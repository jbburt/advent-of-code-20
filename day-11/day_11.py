"""
https://adventofcode.com/2020/day/11
"""

import numpy as np
from scipy.signal import convolve2d

# Read data
f = 'day-11/input.txt'
with open(f) as fp:
    data = [[x for x in line] for line in fp.read().split('\n')]


class Grid(object):

    def __init__(self, grid):

        self.grid = grid
        self.nr = len(grid)
        self.nc = len(grid[0])
        self.adjacent = dict()
        self.temp = None

    def compute_adjacent(self):
        """
        Compute indices of grid cells adjacent to each cell. This method
        updates `self.adjacent`.

        """
        for i in range(self.nr):
            for j in range(self.nc):
                inds = list()
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if not (di == dj == 0):
                            if (0 <= i+di < self.nr) and (0 <= j+dj < self.nc):
                                inds.append((i+di, j+dj))
                self.adjacent[(i, j)] = inds

    def _update(self, i, j, max_n_adj):
        """
        State-updating method for problems 1 and 2.

        Parameters
        ----------
        i : int
            row index
        j : int
            col index
        max_n_adj : int
            max number of adjacent seats allowed

        Returns
        -------
        int : row index
        int : col index
        char : updated seat

        """
        empty = self.temp[i][j] == 'L'
        is_occupied = self.temp[i][j] == '#'
        adjacent = [self.temp[ii][jj] for (ii, jj) in self.adjacent[(i, j)]]
        n_adjacent_filled = sum([x == '#' for x in adjacent])
        if empty and not n_adjacent_filled:
            return i, j, '#'
        elif is_occupied and n_adjacent_filled >= max_n_adj:
            return i, j, 'L'
        return None

    def solve_steady_state(self, problem=1):
        """
        Find steady-state solution to one of the problems.

        Parameters
        ----------
        problem : int
            1 or 2

        """
        self.temp = [[i for i in l] for l in self.grid]
        if problem == 1:
            self.compute_adjacent()
            max_adj = 4
        else:
            self.compute_lineofsight()
            max_adj = 5
        while True:
            updates = list()
            for r in range(self.nr):
                for c in range(self.nc):
                    u = self._update(r, c, max_adj)
                    if u is not None:
                        updates.append(u)
            if not updates:
                break
            for r, c, v in updates:
                self.temp[r][c] = v
        answer = sum(map(lambda x: sum([s == '#' for s in x]), self.temp))
        print(f'problem {problem}: {answer}')

    def compute_lineofsight(self):
        """
        Compute index of nearest seat along line-of-sight in each of eight
        directions (four cardinal plus four diagonal). This method updates
        `self.adjacent`.

        """
        for i in range(self.nr):
            for j in range(self.nc):
                seats = list()
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if not (di == dj == 0):
                            k = 1
                            while (0 <= i+k*di < self.nr) and \
                                    (0 <= j+k*dj < self.nc):
                                if self.grid[i+k*di][j+k*dj] == 'L':
                                    seats.append((i+k*di, j+k*dj))
                                    break
                                else:
                                    k += 1
                self.adjacent[(i, j)] = seats


g = Grid(data)
g.solve_steady_state(1)
g.solve_steady_state(2)

# ----------------------------------------------------- #
# Problem 1 w/ image convolution (significantly faster) #
# ----------------------------------------------------- #

arr = np.array(data)
is_floor = (arr == '.')
nrows, ncols = arr.shape
im = np.zeros(arr.shape, dtype=int)

# neighbor kernel
kernel = np.ones((3, 3))
kernel[1, 1] = 0

while True:
    delta = np.zeros(im.shape, dtype=int)
    occupied = (im == 1)
    n_adj = convolve2d(im, kernel, mode='same')
    delta[np.logical_and(~is_floor, np.logical_and(~occupied, n_adj == 0))] = 1
    delta[np.logical_and(occupied, n_adj >= 4)] = -1
    if not np.any(delta):
        break
    im += delta

print(f'problem 1 (convolution): {im.sum()}')
