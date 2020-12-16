"""
https://adventofcode.com/2020/day/5
"""

# Read input
f = 'day-05/input.txt'
with open(f, 'r') as fp:
    boarding_passes = fp.read().split("\n")


def bp2id(bp):
    """
    Convert boarding pass to unique seat ID using binary space partitioning.

    Parameters
    ----------
    bp : string
        boarding pass

    Returns
    -------
    int
        seat ID

    """
    row = col = 0
    for i, c in enumerate(bp[:-3]):
        row += 2**(6-i) * (c == 'B')
    for i, c in enumerate(bp[-3:]):
        col += 2**(2-i) * (c == 'R')
    return row*8 + col


# Problem 1: What is the highest seat ID on a boarding pass?
seat_ids = [bp2id(bp) for bp in boarding_passes]
max_id = max(seat_ids)
print('problem 1:', max_id)

# Problem 2: What is the ID of your seat?
all_ids = set(range(min(seat_ids), max_id+1))
print('problem 2:', all_ids.difference(seat_ids))
