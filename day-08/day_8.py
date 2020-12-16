"""
https://adventofcode.com/2020/day/8
"""

# Read input
f = 'day-08/input.txt'
with open(f, 'r') as fp:
    lines = [line.split() for line in fp.read().split("\n")]
    data = list(map(lambda x: (x[0], int(x[1])), lines))
n = len(data)


def run(instructions):
    """
    Execute instructions in a boot sequence.

    Parameters
    ----------
    instructions : list
        elements are tuples of (string, int) where string is one of the
        three operations nop, acc, jmp

    Returns
    -------
    int
        accumulated value

    Raises
    ------
    IndexError: tried to access an element outside of the list

    """
    i = acc = 0
    visited = set()
    while True:
        if i in visited:
            return i, acc
        else:
            visited.add(i)
        try:
            op_, val_ = instructions[i]
        except IndexError:
            return i, acc
        i += 1 if op_ != 'jmp' else val_
        acc += val_ if op_ == 'acc' else 0


# Problem 1: The original boot sequence contains an error which introduces an
# infinite loop. Immediately before any instruction is executed a second time,
# what value is in the accumulator?
print('problem 1:', run(data)[1])

# Problem 2: Fix the program so that it terminates normally by changing
# exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator
# fter the program terminates?
ops_to_check = [j for j, (x, _) in enumerate(data) if x in ['nop', 'jmp']]
for op_idx in ops_to_check:
    op, val = data[op_idx]
    new_op = (['nop', 'jmp'][op == 'nop'], val)
    new_data = data.copy()
    new_data[op_idx] = new_op
    idx, ans = run(new_data)
    if idx == n:
        print('problem 2:', ans)
        break
