"""
https://adventofcode.com/2020/day/15
"""

from collections import defaultdict

f = 'day-15/input.txt'

with open(f) as fp:
    nums = [int(x) for x in fp.read().strip().split(",")]


def main(n):
    d = defaultdict(list)
    for j, x in enumerate(nums):
        d[x].append(j)
    first_spoken = True
    for i in range(j+1, n):
        if first_spoken:
            y = 0
        else:  # previous number is x
            y = d[x][-1] - d[x][-2]
        first_spoken = True if y not in d else False
        d[y].append(i)
        x = y
    return x


print(f'problem 1: {main(2020)}')
print(f'problem 2: {main(30000000)}')


# Solution 2, marginally faster but less concise

# class Data:
#
#     def __init__(self, i):
#         self.prev = i
#         self.penultimate = None
#
#     def update(self, i):
#         self.penultimate = self.prev
#         self.prev = i
#
#     def delta(self):
#         return self.prev - self.penultimate
#
#
# def main(n):
#     d = dict()
#     for j, x in enumerate(nums):
#         d[x] = Data(j)
#     first_spoken = True
#     for i in range(j+1, n):
#         y = 0 if first_spoken else d[x].delta()  # get next number
#         first_spoken = True if y not in d else False
#         if first_spoken:
#             d[y] = Data(i)
#         else:
#             d[y].update(i)
#         x = y
#     return x
#
#
# print(f'problem 1: {main(2020)}')
# print(f'problem 2: {main(30000000)}')


# Solution 3, same runtime as Solution 2

# init = lambda i: {'prev': i, 'penultimate': None}
#
#
# def main(n):
#     d = dict()
#     for j, x in enumerate(nums):
#         d[x] = init(j)
#     first_spoken = True
#     for i in range(j+1, n):
#         if first_spoken:
#             y = 0
#         else:
#             y = d[x]['prev']-d[x]['penultimate']
#         if y not in d:
#             first_spoken = True
#             d[y] = init(i)
#         else:
#             first_spoken = False
#             d[y]['penultimate'] = d[y]['prev']
#             d[y]['prev'] = i
#         x = y
#     return x
#
#
# print(f'problem 1: {main(2020)}')
# print(f'problem 2: {main(30000000)}')
