"""
https://adventofcode.com/2020/day/7
"""

from collections import defaultdict

# Read input
f = 'day-07/input.txt'
with open(f, 'r') as fp:
    data = fp.read().replace(" bags", '').replace(" bag", '').replace('.', '')
data = data.split("\n")

# Parse input: map from a bag to other bags contained therein
mappings = dict()
for d in data:
    k, v = d.split(' contain ')
    if v == "no other":
        mappings[k] = None
    else:
        mappings[k] = [(x[2:], int(x[0])) for x in v.split(', ')]

# Problem 1:
# How many bag colors can contain at least one shiny gold bag?
untested = set(mappings.keys())  # colors which have not been tested
queue = {'shiny gold'}  # bags which may contain a shiny gold bag
n = -1
while queue:
    c = queue.pop()
    n += 1
    for k, v in mappings.items():
        if v is not None:  # if bag contains other bags
            colors = [x[0] for x in v]
            if c in colors and k in untested:
                queue.add(k)
                untested.remove(k)
print(f'problem 1: {n}')

# Problem 2:
# How many individual bags are required inside your single shiny gold bag?
n = -1
queue = defaultdict(lambda: 0)
queue['shiny gold'] = 1
while queue:
    bag_color, nbags = queue.popitem()
    n += nbags
    nested_items = mappings[bag_color]
    if nested_items is not None:
        for c, nb in nested_items:
            queue[c] += nb*nbags
print(f'problem 2: {n}')
