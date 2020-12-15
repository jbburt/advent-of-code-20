"""
https://adventofcode.com/2020/day/14
"""

from collections import defaultdict
import re

f = 'day-14/input.txt'

with open(f) as fp:
    lines = fp.read().split('\n')


def parse_mem(string):
    m = re.search(r"\[([0-9]+)]", string)
    memaddress = m.group(1)
    memvalue = string.split(' = ')[1]
    return int(memaddress), int(memvalue)


def parse_mask(string):
    return string.split(' = ')[1]


def num2binrep(num, width=36):
    return ''.join(str((num >> i) & 1) for i in range(width-1, -1, -1))


def binrep2num(binrep):
    return sum([2**int(i) if bit == '1' else 0 for i, bit in enumerate(
        reversed(binrep))])


def apply_mask(binmask, num):
    binrep_masked = ''
    binrep = num2binrep(num)
    for bit, m in zip(binrep, binmask):
        if m == '1':
            binrep_masked += '1'
        elif m == '0':
            binrep_masked += '0'
        else:
            binrep_masked += bit
    return binrep2num(binrep_masked)


def apply_mask_v2(binmask, memaddress):
    binrep_masked = ''
    binrep = num2binrep(memaddress)
    for bit, m in zip(binrep, binmask):
        if m == '1':
            binrep_masked += '1'
        elif m == 'X':
            binrep_masked += 'X'
        elif m == '0':
            binrep_masked += bit
    return binrep_masked


def expand(memaddress):
    try:  # find index of next floating bit
        ix = memaddress.index('X')
    except ValueError:  # no more floating bits
        return [memaddress]
    root = memaddress[:ix]
    return [root+bit+s for bit in ['1', '0'] for s in expand(memaddress[ix+1:])]


d1 = defaultdict(lambda x: 0)
d2 = defaultdict(lambda x: 0)
mask = parse_mask(lines[0])

for l in lines[1:]:
    if l[:3] == 'mem':
        address, value = parse_mem(l)
        d1[address] = apply_mask(mask, value)  # problem 1
        masked_address = apply_mask_v2(mask, address)
        addresses = [binrep2num(x) for x in expand(masked_address)]
        for addy in addresses:
            d2[addy] = value  # problem 2
    else:
        mask = parse_mask(l)


print(f'problem 1: {sum(d1.values())}')
print(f'problem 2: {sum(d2.values())}')
