"""
https://adventofcode.com/2020/day/3
"""

from functools import reduce

f = 'day-03/input.txt'

with open(f) as fp:
    arr = fp.read().split('\n')

nrows = len(arr)
ncols = len(arr[0])


def compute(slope):
    ntrees = 0
    di = slope[1]
    dj = slope[0]
    for i in range(0, nrows, di):
        j = (dj * int(i/di)) % ncols
        if arr[i][j] == "#":
            ntrees += 1
    return ntrees


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
tree_counts = [compute(s) for s in slopes]

# Problem 1
print('problem 1:', tree_counts[1])

# Problem 2
print('problem 2:', reduce(lambda a, b: a*b, tree_counts))
