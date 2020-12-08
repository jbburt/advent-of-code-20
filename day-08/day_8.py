f = 'day-08/input.txt'

data = list()
with open(f, 'r') as fp:
    for line in fp.read().split("\n"):
        x, y = line.split(" ")
        data.append((x, int(y)))
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
        if op_ == 'nop':
            i += 1
        elif op_ == 'jmp':
            i += val_
        elif op_ == 'acc':
            acc += val_
            i += 1


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
