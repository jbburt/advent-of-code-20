from functools import reduce

f = 'day-03/input.txt'

nrows = 0
arr = list()
with open(f, 'r') as fp:
    lines = fp.readlines()
for line in lines:
    arr.append([x for x in line.strip("\n")])
    nrows += 1
width = len(arr[0])


def compute(slope):
    ntrees = 0
    di = slope[1]
    dj = slope[0]
    for i in range(0, nrows, di):
        j = (dj * int(i/di)) % width
        if arr[i][j] == "#":
            ntrees += 1
    return ntrees


# Problem 1
print(compute((3, 1)))

# Problem 2
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
tree_counts = [compute(s) for s in slopes]
print(reduce(lambda a, b: a*b, tree_counts))
