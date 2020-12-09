"""
https://adventofcode.com/2020/day/6
"""

from time import time

t1 = time()

f = 'day-06/input.txt'

with open(f, 'r') as fp:
    data = fp.read().split("\n\n")
forms = [x.split('\n') for x in data]

# Problem 1
print('problem 1:', sum(len(set(s.replace('\n', ''))) for s in data))

# Problem 2
print('problem 2:', sum([len(set.intersection(*map(set, f))) for f in forms]))
