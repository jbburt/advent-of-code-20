"""
https://adventofcode.com/2020/day/13
"""

f = 'day-13/input.txt'

with open(f) as fp:
    lines = fp.read().split('\n')
earliest_time = int(lines[0])
schedule = lines[1].split(',')
shuttle_ids = [int(x) for x in schedule if x != 'x']

# problem 1
wait_times = [x-(earliest_time % x) for x in shuttle_ids]
idx = wait_times.index(min(wait_times))
print(f'problem 1: {wait_times[idx]*shuttle_ids[idx]}')

# problem 2
offsets = [schedule.index(str(x)) for x in shuttle_ids]
time = delta = shuttle_ids[0]
for bus_id, offset in zip(shuttle_ids[1:], offsets[1:]):
    while (time + offset) % bus_id:
        time += delta
    delta *= bus_id
print(f'problem 2: {time}')
