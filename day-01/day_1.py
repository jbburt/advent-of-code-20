from itertools import product

f = 'day-01/input.txt'

with open(f, 'r') as fp:
    data = fp.read().split('\n')

d = [int(x) for x in data]
s = set(d)

# Problem 1
for n in s:
    if (2020-n) in s:
        print(n * (2020-n))
        break

# Problem 2
combs = product(d, d, d)
for c in combs:
    if sum(c) == 2020:
        print(c[0]*c[1]*c[2])
        break
