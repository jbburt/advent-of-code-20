"""
https://adventofcode.com/2020/day/18
"""

from functools import reduce

# Read input -- mathematical expressions
f = 'day-18/input.txt'
with open(f) as fp:
    lines = fp.read().split('\n')


def evaluate_lr(elements):
    """
    Evaluate a single mathematical expression left-to-right.

    Parameters
    ----------
    elements : List[str]
        mathematical expression represented as a list of characters, e.g.
        ['3', '+', '2']

    Returns
    -------
    int

    """

    num1 = int(elements.pop(0))
    while elements:
        op = elements.pop(0)
        num2 = int(elements.pop(0))
        num1 = num1+num2 if op == '+' else num1*num2
    return num1


def evaluate_add_first(elements):
    """
    Evaluate a single mathematical expression, with addition taking precedence
    over multiplication.

    Parameters
    ----------
    elements : List[str]
        mathematical expression represented as a list of characters, e.g.
        ['3', '+', '2']

    Returns
    -------
    int

    """
    _stack = [int(elements.pop(0))]
    while elements:
        op = elements.pop(0)
        if op == '*':
            _stack.append(int(elements.pop(0)))
        else:
            next_num = int(elements.pop(0))
            _stack[-1] += next_num
    return reduce(lambda a, b: a*b, _stack)


# Problem 1: Evaluate the expression on each line of the input;
# what is the sum of the resulting values?
tot = 0
for line in lines:
    stack = [[]]
    for j, c in enumerate(line):
        if c == " ":
            continue
        elif c == '(':
            stack.append([])
        elif c == ')':  # evaluate
            expr = stack.pop(-1)
            stack[-1].append(str(evaluate_lr(expr)))
        else:
            stack[-1].append(c)
    line_result = evaluate_lr(stack.pop())
    tot += line_result
print(f'problem 1: {tot}')


# Problem 2: Now, addition and multiplication have different precedence
# levels, but they're not the ones you're familiar with. Instead, addition
# is evaluated before multiplication.
tot = 0
for line in lines:
    stack = [[]]
    for j, c in enumerate(line):
        if c == " ":
            continue
        elif c == '(':
            stack.append([])
        elif c == ')':  # evaluate
            expr = stack.pop(-1)
            stack[-1].append(str(evaluate_add_first(expr)))
        else:
            stack[-1].append(c)
    line_result = evaluate_add_first(stack.pop())
    tot += line_result
print(f'problem 2: {tot}')


# def parse_nested(string):
#     """
#     Parse parenthetically-nested mathematical expressions.
#
#     Parameters
#     ----------
#     string : str
#         mathematical expression string
#
#     Returns
#     -------
#     indices : list(tuple(int,int))
#         each tuple includes three elements, corresponding to the index of the
#         opening parenthesis and the index of the corresponding closing
#         parenthesis. elements are ordered according to precedence such that
#         the parentheses corresponding to indices[0] should be evaluated first.
#
#     """
#     indices = list()
#     stack = list()
#     for j, c in enumerate(string):
#         if c == '(':
#             stack.append(j)
#         elif c == ')':
#             i = stack.pop(-1)
#             indices.append((i, j))
#     return indices
