"""
https://adventofcode.com/2020/day/17
"""

import numpy as np
from scipy import ndimage


# Read input -- initial conditions of Conway Cubes in the pocket dimension
f = 'day-17/input.txt'
with open(f) as fp:
    data = np.asarray([[1 if x == '#' else 0 for x in line]
                       for line in fp.read().split('\n')])


# During a cycle, all cubes simultaneously change their state according to
# the following rules:
# - If a cube is active and exactly 2 or 3 of its neighbors are also active,
# the cube remains active. Otherwise, the cube becomes inactive.
# - If a cube is inactive but exactly 3 of its neighbors are active, the cube
# becomes active. Otherwise, the cube remains inactive.


def simulate(plane_init, ndim, niter):
    """
    Simulate Conway cubes on an N-dimensional lattice.

    Parameters
    ----------
    plane_init : (N,M) np.ndarray
        initial state of two-dimensional plane
    ndim : int
        number of dimensions
    niter : int
        number of cycles

    Returns
    -------
    int : number of active cubes after `niter` cycles

    """

    # expand to ndim dimensions
    X = plane_init.reshape(plane_init.shape + (1,)*int(ndim-2))

    # Define "neighbors" kernel
    kernel = np.ones(int(3 ** ndim)).reshape([3] * ndim)
    kernel[tuple([1] * ndim)] = 0  # you aren't your own neighbor lol

    for _ in range(niter):

        # expand cube to include (initially inactive) neighboring cells
        X = np.pad(X, pad_width=1, mode='constant', constant_values=0)

        # convolve with kernel to get number of active neighbors per cell
        active_neighbors = ndimage.convolve(X, kernel, mode='constant', cval=0)

        # apply rules to update state
        mask2 = active_neighbors == 2
        mask3 = active_neighbors == 3
        isactive = X.astype(bool)
        condition1 = np.logical_and(isactive, ~np.logical_or(mask2, mask3))
        condition2 = np.logical_and(~isactive, mask3)
        X[np.where(condition1)] = 0
        X[np.where(condition2)] = 1

    return X.sum()


# Problem 1: How many cubes are left in the active state after the sixth cycle?
print(f'problem 1: {simulate(data, 3, 6)}')

# Problem 2: same but in four dimensions
print(f'problem 2: {simulate(data, 4, 6)}')
