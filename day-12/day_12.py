"""
https://adventofcode.com/2020/day/12
"""

from math import sin, cos, pi

f = 'day-12/input.txt'

with open(f) as fp:
    instructions = [(x[0], int(x[1:])) for x in fp.read().split('\n')]


heading = [1, 0]  # +x direction = east
pos = [0, 0]

for ins, val in instructions:
    if ins == 'N':
        pos[1] += val
    elif ins == 'S':
        pos[1] -= val
    elif ins == 'E':
        pos[0] += val
    elif ins == 'W':
        pos[0] -= val
    elif ins == 'F':
        pos[0] += val * heading[0]
        pos[1] += val * heading[1]
    else:  # use 2D rotation matrix
        if ins == 'R':
            val *= -1
        cosine = cos(val*pi/180)
        sine = sin(val*pi/180)
        x = heading[0] * cosine - heading[1] * sine
        y = heading[0] * sine + heading[1] * cosine
        heading = (x, y)

print(f'problem 1: {int(abs(pos[0])+abs(pos[1])+0.5)}')

# problem 2

waypoint = [10, 1]  # relative to the ship
pos = [0, 0]

for ins, val in instructions:
    if ins == 'N':
        waypoint[1] += val
    elif ins == 'S':
        waypoint[1] -= val
    elif ins == 'E':
        waypoint[0] += val
    elif ins == 'W':
        waypoint[0] -= val
    elif ins == 'F':
        pos[0] += val * waypoint[0]
        pos[0] += val * waypoint[1]
    else:  # use 2D rotation matrix
        if ins == 'R':
            val *= -1
        cosine = cos(val*pi/180)
        sine = sin(val*pi/180)
        x = waypoint[0] * cosine - waypoint[1] * sine
        y = waypoint[0] * sine + waypoint[1] * cosine
        waypoint = [x, y]

print(f'problem 2: {int(abs(pos[0])+abs(pos[1])+0.5)}')
