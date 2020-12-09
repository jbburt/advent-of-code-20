"""
https://adventofcode.com/2020/day/2
"""

f = 'day-02/input.txt'

with open(f, 'r') as fp:
    lines = fp.read().split('\n')

count_p1 = count_p2 = 0
for line in lines:
    rnge, char, password = line.split(" ")
    cmin, cmax = (int(x) for x in rnge.split("-"))
    if cmin <= password.count(char[0]) <= cmax:
        count_p1 += 1
    if (password[cmin-1] == char[0]) + (password[cmax-1] == char[0]) == 1:
        count_p2 += 1

print('problem 1:', count_p1)
print('problem 2:', count_p2)
