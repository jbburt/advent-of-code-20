"""
https://adventofcode.com/2020/day/6
"""

# Read input
f = 'day-06/input.txt'
with open(f, 'r') as fp:
    data = fp.read().split("\n\n")
forms = [x.split('\n') for x in data]

# Each form corresponds to a group of people
# Each element of a form corresponds to a person
# Each element contains the questions which that person responded 'yes' to

# Problem 1
# For each group, count the number of questions to which anyone answered 'yes';
# find the sum of those counts.
print('problem 1:', sum(len(set(s.replace('\n', ''))) for s in data))

# Problem 2
# For each group, count the number of questions to which everyone answered yes;
# find the sum of those counts.
print('problem 2:', sum([len(set.intersection(*map(set, f))) for f in forms]))
