"""
https://adventofcode.com/2020/day/9
"""

# Read input
f = 'day-09/input.txt'
with open(f) as fp:
    data = [int(x) for x in fp.read().split("\n")]


def problem1(nums, preamble_length=25):
    """
    Problem 1 solution.

    Parameters
    ----------
    nums : list
        Integers which have been encrypted with the eXchange-Masking Addition
        System (XMAS) protocol.
    preamble_length : int
        Number of elements in `nums` corresponding to the preamble

    Returns
    -------
    int
        the first number in `nums` which is not the sum of two of the preceding
        `preamble_length` numbers

    """
    window = set(nums[:preamble_length])
    condition_met = False
    for i, x in enumerate(nums[preamble_length:]):
        for y in nums[i:i+preamble_length]:
            d = x-y
            if d != x and d in window:
                window.remove(nums[i])
                window.add(nums[preamble_length+i])
                condition_met = True
                break
        if not condition_met:
            return x
        condition_met = False


def problem2(nums, target):
    """
    Problem 2 solution.

    Parameters
    ----------
    nums : list
        Integers which have been encrypted with the eXchange-Masking Addition
        System (XMAS) protocol.
    target : int
        target number

    Returns
    -------
    int
        the min and max of a range of contiguous elements in `nums` which sum to
        `target`

    """
    n = len(data)
    cumsum = 0
    for start in range(n-1):
        for end in range(start, n):
            cumsum += nums[end]
            if cumsum == target:
                subarr = nums[start:end+1]
                return min(subarr) + max(subarr)
            elif cumsum > target:
                start += 1
        cumsum = 0


bad_num = problem1(data)
encrypt_key = problem2(data, bad_num)

# Problem 1: The first step of attacking the weakness in the XMAS data is to
# find the first number in the list (after the preamble) which is not the sum
# of two of the 25 numbers before it. What is the first number that does not
# have this property?
print('problem 1:', bad_num)

# Problem 2: The final step in breaking the XMAS encryption relies on the
# invalid number you just found: find a contiguous set of at least
# two numbers in your list which sum to the invalid number from problem 1.
print('problem 2:', encrypt_key)
