"""
https://adventofcode.com/2020/day/2
"""

# Read input
f = 'day-02/input.txt'
with open(f, 'r') as fp:
    lines = fp.read().split('\n')

# Each line has the following form:
#   1-3 a: abcde
# corresponding to
#   min-max char: password
# in problem 1 and
#   pos1-pos2 char: password
# in problem 2

count_p1 = count_p2 = 0
for line in lines:
    rnge, char, password = line.split(" ")
    cmin, cmax = (int(x) for x in rnge.split("-"))
    if cmin <= password.count(char[0]) <= cmax:
        count_p1 += 1  # password contains allowed number of this character
    if (password[cmin-1] == char[0]) + (password[cmax-1] == char[0]) == 1:
        count_p2 += 1  # exactly one of the two positions contains the character

# Problem 1: how many passwords are valid?
print('problem 1:', count_p1)

# Problem 2: how many passwords are valid?
print('problem 2:', count_p2)
