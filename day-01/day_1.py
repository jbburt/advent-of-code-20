"""
https://adventofcode.com/2020/day/1
"""

# Read input
f = 'day-01/input.txt'
with open(f, 'r') as fp:
    data = [int(x) for x in fp.read().split('\n')]

# Problem 1:
# What is the product of the two elements that sum to 2020?
s1 = set(data)
for n in data:
    test = 2020-n
    if test in s1:
        result1 = n*test
        break

# Problem 2:
# What is the product of the three elements that sum to 2020?
s2 = sorted(data)
for i, n1 in enumerate(s2):
    for n2 in s2[i+1:]:
        if (n1+n2) > 2020:
            break
        if 2020-n1-n2 in s1:
            result2 = n1 * n2 * (2020-n1-n2)
            break

print('problem 1:', result1)
print('problem 2:', result2)
