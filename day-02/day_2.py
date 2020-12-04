f = 'day-02/input.txt'

with open(f, 'r') as fp:
    lines = fp.readlines()

count_p1 = 0
count_p2 = 0
for line in lines:
    rnge, char, password = line.strip("\n").split(" ")
    char = char[0]
    cmin, cmax = rnge.split("-")
    cmin = int(cmin)
    cmax = int(cmax)
    if cmin <= password.count(char) <= cmax:
        count_p1 += 1
    if int(password[cmin-1] == char) + int(password[cmax-1] == char) == 1:
        count_p2 += 1

print(count_p1)
print(count_p2)
