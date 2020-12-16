"""
https://adventofcode.com/2020/day/13
"""

# Read and parse input
f = 'day-13/input.txt'
with open(f) as fp:
    lines = fp.read().split('\n')
earliest_time = int(lines[0])
schedule = lines[1].split(',')
shuttle_ids = [int(x) for x in schedule if x != 'x']

# Problem 1: What is the ID of the earliest bus you can take to the airport
# multiplied by the number of minutes you'll need to wait for that bus?
wait_times = [x-(earliest_time % x) for x in shuttle_ids]
idx = wait_times.index(min(wait_times))
print(f'problem 1: {wait_times[idx]*shuttle_ids[idx]}')

# Problem 2: What is the earliest timestamp such that all of the listed bus
# IDs depart at offsets matching their positions in the list?
offsets = [schedule.index(str(x)) for x in shuttle_ids]
time = delta = shuttle_ids[0]
for bus_id, offset in zip(shuttle_ids[1:], offsets[1:]):
    while (time + offset) % bus_id:
        time += delta
    delta *= bus_id
print(f'problem 2: {time}')
