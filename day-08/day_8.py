f = 'day-08/input.txt'

with open(f, 'r') as fp:
    lines = [line.split() for line in fp.read().split("\n")]
    data = list(map(lambda x: (x[0], int(x[1])), lines))
n = len(data)


def run(instructions):
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


# Problem 1
print(run(data)[1])

# Problem 2
ops_to_check = [j for j, (x, _) in enumerate(data) if x in ['nop', 'jmp']]
for op_idx in ops_to_check:
    op, val = data[op_idx]
    new_op = (['nop', 'jmp'][op == 'nop'], val)
    new_data = data.copy()
    new_data[op_idx] = new_op
    idx, ans = run(new_data)
    if idx == n:
        print(ans)
        break
