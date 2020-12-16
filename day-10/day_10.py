"""
https://adventofcode.com/2020/day/10
"""

# Read input
f = 'day-10/input.txt'
with open(f) as fp:
    adapters = [0] + sorted([int(x) for x in fp.read().split("\n")])

# difference in joltage for paired adapters
deltas = [x-y for x, y in zip(adapters[1:], adapters[:-1])]

# Problem 1: What is the number of 1-jolt differences multiplied by the number
# of 3-jolt differences? Note that your device's built-in adapter has a joltage
# 3 jolts higher than the highest-rated adapter.
answer = deltas.count(1) * (deltas.count(3)+1)
print(f'problem 1: {answer}')

# Problem 2: What is the total number of distinct ways you can arrange the
# adapters to connect the charging outlet to your device?
adapters.remove(0)
na = len(adapters)
paths = [0 if x > 3 else 1 for x in adapters]

# Compute the numbers of `paths` or unique adapter configurations which can
# produce a given output joltage.
for i in range(na):
    j = i+1
    while (j < (na-1)) and ((adapters[j]-adapters[i]) <= 3):
        paths[j] += paths[i]
        j += 1

print(f'problem 2: {paths[-2]}')
