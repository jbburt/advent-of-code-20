"""
https://adventofcode.com/2020/day/3
"""

from functools import reduce

# Read input
f = 'day-03/input.txt'
with open(f) as fp:
    arr = fp.read().split('\n')

# `arr` is a 2D grid where '#' indicates that a tree exists at that location

nrows = len(arr)
ncols = len(arr[0])


def count_trees(slope):
    """
    Compute number of trees encountered for a given slope down the hill.

    Parameters
    ----------
    slope : tuple
        (change in x-position, change in y-position)

    Returns
    -------
    int
        number of trees encountered

    """
    ntrees = 0
    di = slope[1]
    dj = slope[0]
    for i in range(0, nrows, di):
        j = (dj * int(i/di)) % ncols
        if arr[i][j] == "#":
            ntrees += 1
    return ntrees


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
tree_counts = [count_trees(s) for s in slopes]

# Problem 1: how many trees would you encounter for a slope of 3 right, 1 down?
print('problem 1:', tree_counts[1])

# Problem 2: What do you get if you multiply together the number
# of trees encountered on each of the listed slopes?
print('problem 2:', reduce(lambda a, b: a*b, tree_counts))
