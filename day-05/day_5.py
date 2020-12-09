"""
https://adventofcode.com/2020/day/5
"""

f = 'day-05/input.txt'

with open(f, 'r') as fp:
    passes = fp.read().split("\n")


def pass2id(bp):
    row = col = 0
    for i, c in enumerate(bp[:-3]):
        row += 2**(6-i) * (c == 'B')
    for i, c in enumerate(bp[-3:]):
        col += 2**(2-i) * (c == 'R')
    return row*8 + col


# Problem 1
seat_ids = [pass2id(bp) for bp in passes]
print(max(seat_ids))

# Problem 2
all_ids = set(range(min(seat_ids), max(seat_ids)+1))
print(all_ids.difference(seat_ids))
