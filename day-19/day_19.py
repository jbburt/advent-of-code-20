"""
https://adventofcode.com/2020/day/19
"""

import re
from itertools import accumulate

# Read input: rules that valid messages should obey, and a list of received
# messages
with open('day-19/input.txt') as fp:
    lines = fp.read().split('\n')

# Parse problem input
rules = dict()
for i, line in enumerate(lines):
    if not line:  # empty line
        break
    rule_, string = line.split(": ")
    try:  # rule which depends on other rules
        value = list(map(
            lambda x: list(map(int, x.split(" "))), string.split(' | ')))
    except ValueError:  # rule which specifies a character
        value = re.search(r"\"([a-z])\"", string).group(1)
    rules[int(rule_)] = value
messages = lines[i+1:]
base_rules = {k for k, v in rules.items() if type(v) is str}


# use topological sort to determine order in which rules should be checked
# if current rule depends on some other rule, go to that rule first

def topological_visit(_rule):
    visited.add(_rule)
    if _rule in base_rules:  # no dependencies
        stack.append(_rule)
    else:
        subrules = set([item for sublist in rules[_rule] for item in sublist])
        for sr in subrules:
            if sr not in visited:
                topological_visit(sr)
        stack.append(_rule)


stack = list()
visited = set()
for rule_ in rules.keys():
    if rule_ not in visited:
        topological_visit(rule_)

# determine length of strings associated with each rule
n = {ir: 1 for ir in base_rules}
for rule_ in stack:
    if rule_ not in base_rules:
        n[rule_] = sum([n[r] for r in rules[rule_][0]])


def evaluate(m, rule):
    """

    Evaluate a message against a specific rule.

    Parameters
    ----------
    m : str
        message to evaluate
    rule : int
        index of rule to check

    Returns
    -------
    bool
        evaluates to True if rules are satisfied

    """
    if rule in base_rules:
        return m == rules[rule]
    for ids in rules[rule]:
        subrule_isvalid = list()
        idx = [0] + list(accumulate([n[ir] for ir in ids]))
        if idx[-1] != len(m):
            continue
        for (ii, jj), r in zip(zip(idx[:-1], idx[1:]), ids):
            subrule_isvalid.append(evaluate(m[ii:jj], r))
        if all(subrule_isvalid):
            return True
    return False


print(f'problem 1: {sum(evaluate(m, 0) for m in messages)}')

# problem 2:
# As you look over the list of messages, you realize your matching rules
# aren't quite right. To fix them, completely replace rules
# 8: 42 and 11: 42 31 with the following:
#   8: 42 | 42 8
#   11: 42 31 | 42 11 31

# we can use our result from problem 1 to build up a different kind of solution.
# after staring at the new rules you can convince yourself that rule 0, which
# is
#   0: 8 11
# consists of subsequences that match rules 42 and 31. thus we should be able
# to check this condition by looping over the message in chunks and evaluating
# these chunks against rules 42 and 31. the minimum message that would satisfy
# rule 0 is a message that can be decomposed into 42 42 31.


def problem2(m):
    """
    Evaluation a message for problem 2.

    Parameters
    ----------
    m : str
        message to evaluate

    Returns
    -------
    bool
        evaluates to True if rules are satisfied

    """
    j = 0
    N = len(m)
    rule = 42  # begin by evaluating substrings against rule 42
    n1 = n2 = 0
    while j < N:  # loop through message in chunks
        s = m[j:j + n[rule]]  # grab next substring
        if not evaluate(s, rule):  # doesn't satisfy rule 42
            break
        j += n[rule]  # increment to check next sequence
        n1 += 1  # another pattern matched
    if n1 < 2 or j == N:  # either all rule-42 patterns, or not at least two
        return False
    rule = 31  # update rule
    while j < N:
        s = m[j:j + n[rule]]
        if not evaluate(s, rule):
            return False
        j += n[rule]
        n2 += 1
    # there are two more conditions which must be satisfied:
    # 1. we must have reached the end of the message (ie no extraneous chars)
    # 2. we must have fewer rule-42 patterns than rule-31 patterns
    return True if j == N and n2 < n1 else False


print(f'problem 2: {sum(problem2(m) for m in messages)}')
