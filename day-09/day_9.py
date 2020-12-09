"""
https://adventofcode.com/2020/day/9
"""

from time import time

t1 = time()

f = 'day-09/input.txt'

with open(f) as fp:
    data = [int(x) for x in fp.read().split("\n")]


def problem1(nums, preamble_length=25):
    window = set(nums[:preamble_length])
    condition_met = False
    for i, x in enumerate(nums[preamble_length:]):
        for y in nums[i:i+preamble_length]:
            d = x-y
            if d != x and d in window:
                window.remove(nums[i])
                window.add(nums[preamble_length+i])
                condition_met = True
                break
        if not condition_met:
            return x
        condition_met = False


def problem2(nums, target):
    n = len(data)
    cumsum = 0
    for start in range(n-1):
        for end in range(start, n):
            cumsum += nums[end]
            if cumsum == target:
                subarr = nums[start:end+1]
                return min(subarr) + max(subarr)
            elif cumsum > target:
                start += 1
        cumsum = 0


bad_num = problem1(data)
encrypt_key = problem2(data, bad_num)
t2 = time()

print('problem 1:', bad_num)
print('problem 2:', encrypt_key)
print('time:', t2-t1)
