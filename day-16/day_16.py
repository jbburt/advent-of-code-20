"""
https://adventofcode.com/2020/day/16
"""

# Read input
f = 'day-16/input.txt'
with open(f) as fp:
    lines = fp.read().split('\n')

# Construct mapping from field name to set of allowed values
rules = dict()
for line in lines[:20]:  # rules
    field_str, range_str = line.split(':')
    key = '_'.join([x for x in field_str.split(' ')])
    strings = range_str.lstrip(' ').split(' or ')
    rngs = [(int(x[0]), int(x[1])) for x in [y.split('-') for y in strings]]
    rules[key] = set(range(rngs[0][0], rngs[0][1]+1)).union(
        set(range(rngs[1][0], rngs[1][1]+1)))

# Numbers on each ticket
my_ticket = [int(x) for x in lines[22].split(",")]
tickets = [list(map(int, y.split(','))) for y in lines[25:]]

# Problem 1: Consider the validity of the nearby tickets you scanned.
# What is your ticket scanning error rate?
allowed_values = set()
for _, allowed in rules.items():
    allowed_values = allowed_values.union(allowed)
result1 = 0
invalid_tickets = set()
for i, ticket in enumerate(tickets):
    for num in ticket:
        if num not in allowed_values:
            result1 += num
            invalid_tickets.add(i)
print(f'problem 1: {result1}')

# Determine which tickets in problem 1 were valid
valid_tickets = [t for i, t in enumerate(tickets) if i not in invalid_tickets]
valid_tickets.append(my_ticket)

# Determine which fields could correspond to each ticket element per the rules
all_fields = set([x for x in rules.keys()])
ticket_fields = [all_fields.copy() for _ in range(20)]
for ticket in valid_tickets:
    for i, (options, value) in enumerate(zip(ticket_fields, ticket)):
        invalid_options = set()
        for option in options:
            if value not in rules[option]:
                invalid_options.add(option)
        ticket_fields[i].difference_update(invalid_options)

# Find self-consistent field identities
selected_fields = set()
field_assignments = [''] * 20
noptions = [len(f) for f in ticket_fields]
argsort = [noptions.index(i) for i in range(1, 21)]
for index in argsort:
    field = ticket_fields[index].difference(selected_fields).pop()
    selected_fields.add(field)
    field_assignments[index] = field

# Problem 2: Once you work out which field is which, look for the six fields
# on your ticket that start with the word departure. What do you get if you
# multiply those six values together?
result2 = 1
for value, field in zip(my_ticket, field_assignments):
    if 'departure' in field:
        result2 *= value
print(f'problem 2: {result2}')
