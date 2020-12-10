"""
https://adventofcode.com/2020/day/10
"""

f = 'day-10/input.txt'

with open(f) as fp:
    adapters = [0] + sorted([int(x) for x in fp.read().split("\n")])

deltas = [x - y for x, y in zip(adapters[1:], adapters[:-1])]
answer = deltas.count(1) * (deltas.count(3)+1)
print(f'problem 1: {answer}')

adapters.remove(0)
na = len(adapters)
paths = [0 if x > 3 else 1 for x in adapters]

for i in range(na):
    j = i+1
    while (j < (na-1)) and ((adapters[j]-adapters[i]) <= 3):
        paths[j] += paths[i]
        j += 1

print(f'problem 2: {paths[-2]}')
