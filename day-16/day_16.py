"""
https://adventofcode.com/2020/day/16
"""

f = 'day-16/input.txt'

with open(f) as fp:
    lines = fp.read().split('\n')


def ranges2set(string):
    strings = string.lstrip(' ').split(' or ')
    rngs = [(int(x[0]), int(x[1])) for x in [y.split('-') for y in strings]]
    return set(range(rngs[0][0], rngs[0][1]+1)).union(
        set(range(rngs[1][0], rngs[1][1]+1)))


rules = dict()
for line in lines[:20]:  # rules
    field_str, range_str = line.split(':')
    key = '_'.join([x for x in field_str.split(' ')])
    rules[key] = ranges2set(range_str)

my_ticket = [int(x) for x in lines[22].split(",")]
tickets = [list(map(int, y.split(','))) for y in lines[25:]]

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

valid_tickets = [t for i, t in enumerate(tickets) if i not in invalid_tickets]
valid_tickets.append(my_ticket)
all_fields = set([x for x in rules.keys()])

ticket_fields = [all_fields.copy() for _ in range(20)]
for ticket in valid_tickets:
    for i, (options, value) in enumerate(zip(ticket_fields, ticket)):
        invalid_options = set()
        for option in options:
            if value not in rules[option]:
                invalid_options.add(option)
        ticket_fields[i].difference_update(invalid_options)

# find self-consistent field identities
selected_fields = set()
field_assignments = [''] * 20
noptions = [len(f) for f in ticket_fields]
argsort = [noptions.index(i) for i in range(1, 21)]
for index in argsort:
    field = ticket_fields[index].difference(selected_fields).pop()
    selected_fields.add(field)
    field_assignments[index] = field

result2 = 1
for value, field in zip(my_ticket, field_assignments):
    if 'departure' in field:
        result2 *= value
print(f'problem 2: {result2}')
