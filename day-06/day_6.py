"""
https://adventofcode.com/2020/day/6
"""

f = 'day-06/input.txt'

with open(f, 'r') as fp:
    data = fp.read().split("\n\n")

# Problem 1
print(sum(len(set(s.replace('\n', ''))) for s in data))

# Problem 2
forms = [x.split('\n') for x in data]
print(sum([len(set.intersection(*map(set, f))) for f in forms]))
