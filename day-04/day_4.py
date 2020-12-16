"""
https://adventofcode.com/2020/day/4
"""

# Read and parse input
f = 'day-04/input.txt'
with open(f, 'r') as fp:
    text = fp.read()
passports = list()
entries = text.split("\n\n")
for e in entries:
    entry_dict = dict()
    items_as_strings = e.replace("\n", " ").split(" ")
    for i in items_as_strings:
        k, v = i.split(":")
        entry_dict[k] = v
    passports.append(entry_dict)

fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
eyecolors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def pass_is_valid(pdict):
    """
    Check if a passport is valid.

    Parameters
    ----------
    pdict : dict
        dictionary containing passport elements

    Returns
    -------
    int
        1 if passport is valid, else 0

    """
    for key, value in pdict.items():
        if key == 'byr':
            if int(value) < 1920 or int(value) > 2002:
                return 0
        elif key == 'iyr':
            if int(value) < 2010 or int(value) > 2020:
                return 0
        elif key == 'eyr':
            if int(value) < 2020 or int(value) > 2030:
                return 0
        elif key == 'hgt':
            unit = value[-2:]
            hgt = int(value[:-2])
            if unit == 'cm':
                if hgt < 150 or hgt > 193:
                    return 0
            elif unit == 'in':
                if hgt < 59 or hgt > 76:
                    return 0
            else:
                return 0
        elif key == 'hcl':
            if len(value) != 7 or value[0] != '#' or (not value[1:].isalnum()):
                return 0
        elif key == 'ecl':
            if value not in eyecolors:
                return 0
        elif key == 'pid':
            if len(value) != 9:
                return 0
    return 1


# Problem 1
np = 0
valid_passports1 = list()
for p in passports:
    if set(p.keys()).issuperset(fields):  # passport incl. all required fields
        np += 1
        valid_passports1.append(p)
print('problem 1:', np)

# Problem 2
np = 0
valid_passports2 = list()
for p in valid_passports1:
    if pass_is_valid(p):
        np += 1
        valid_passports2.append(p)
print('problem 2:', np)
