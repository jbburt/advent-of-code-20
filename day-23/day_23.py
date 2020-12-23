"""
https://adventofcode.com/2020/day/23
"""

# Read input: cups arranged in a circle and labeled clockwise
with open('day-23/input.txt') as fp:
    cups = [int(x) for x in fp.read().replace("\n", '')]

# Each move, the crab does the following actions:
# The crab picks up the three cups that are immediately clockwise of the current
# cup. They are removed from the circle; cup spacing is adjusted as necessary
# to maintain the circle.
# The crab selects a destination cup: the cup with a label equal to the current
# cup's label minus one. If this would select one of the cups that was just
# picked up, the crab will keep subtracting one until it finds a cup that
# wasn't just picked up. If at any point in this process the value goes below
# the lowest value on any cup's label, it wraps around to the highest value on
# any cup's label instead.
# The crab places the cups it just picked up so that they are immediately
# clockwise of the destination cup. They keep the same order as when they were
# picked up.
# The crab selects a new current cup: the cup which is immediately clockwise of
# the current cup.

# Let's try to use a circular linked list data structure for this problem


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class CircularLinkedList:

    def __init__(self):
        self.head = None

    def push(self, value):
        node = Node(value)  # new node pushed to beginning of list
        if self.head is None:  # list is empty
            node.next = node
        else:  # insert into list
            node.next = self.head
            # the last element (the node pointing to self.head) must now point
            # to node
            ptr = self.head
            while ptr.next != self.head:
                ptr = ptr.next
            ptr.next = node
        self.head = node


# throw in a little object inheritance too
class Cups(CircularLinkedList):

    def __init__(self, cup_labels):
        super().__init__()
        for cup in reversed(cup_labels):
            self.push(cup)
        self.cups = set(cup_labels)
        self.n = max(cups)

    def move(self):
        # current cup is self.head

        # select next three cups
        c1 = self.head.next
        # next_three_cups = [node]
        next_three_values = {c1.value}
        node = c1
        for _ in range(2):
            node = node.next
            # next_three_cups.append(node)
            next_three_values.add(node.value)
        c3 = node

        # determine destination value
        dest_val = self.head.value - 1 if self.head.value > 1 else self.n
        while dest_val in next_three_values:
            dest_val -= 1
            if not dest_val:
                dest_val = self.n

        # place the picked-up cups immediately to the right of destination cup

        # head now points to the fourth-next cup
        self.head.next = c3.next

        # destination cup now points to the three picked-up cups
        dest_cup = self.head
        while dest_cup.value != dest_val:
            dest_cup = dest_cup.next
        temp = dest_cup.next
        dest_cup.next = c1

        # third picked-up cup now points to the cup destination cup pointed to
        c3.next = temp

        # select new current cup
        self.head = self.head.next
        # self.print()

    def print(self):
        vals = []
        temp = self.head
        if self.head is not None:
            while 1:
                vals.append(temp.value)
                temp = temp.next
                if temp == self.head:
                    break
        print(" ".join(str(v) for v in vals))

    def solution(self):
        ptr = self.head
        while ptr.value != 1:
            ptr = ptr.next
        vals = []
        root = ptr
        ptr = ptr.next
        while 1:
            vals.append(ptr.value)
            ptr = ptr.next
            if ptr == root:
                break
        return vals


# Problem 1: what are the labels after 100 moves?
c = Cups(cups)
for i in range(100):
    c.move()
print('problem 1: ' + "".join(str(v) for v in c.solution()))


# Problem 2 : numbers 1-1000000 and 10 million iterations
# store the nodes in a more convenient way to make this problem computationally
# tractable. nodes will be stored in order (node corresponding to number 1 is
# the first element, node corresponding to number 2 is the second element, etc)
# in a list, and on each iteration, the links between nodes will be changed.
# this way we never have to search the whole linked list for a specific element
nodes = [Node(x) for x in list(range(1, 1000001))]
n = 1000000
for i1, i2 in zip(cups[:-1], cups[1:]):
    nodes[i1-1].next = nodes[i2-1]
nodes[cups[-1]-1].next = nodes[9]
for i in range(10, 1000000):
    nodes[i-1].next = nodes[i]
head = nodes[cups[0]-1]
nodes[-1].next = head

for move in range(10000000):

    # select next three cups
    c1 = head.next

    next_three_values = {c1.value}
    node = c1
    for _ in range(2):
        node = node.next
        next_three_values.add(node.value)
    c3 = node

    # determine destination value
    dest_val = head.value-1 if head.value > 1 else n
    while dest_val in next_three_values:
        dest_val -= 1
        if not dest_val:
            dest_val = n

    # place the picked-up cups immediately to the right of destination cup

    # head now points to the fourth-next cup
    head.next = c3.next

    # destination cup now points to the three picked-up cups
    dest_cup = nodes[dest_val-1]
    temp = dest_cup.next
    dest_cup.next = c1

    # third picked-up cup now points to the cup destination cup pointed to
    c3.next = temp

    # select new current cup
    head = head.next

# print(nodes[0].next.value, nodes[0].next.next.value)
print(f'problem 2: {nodes[0].next.value * nodes[0].next.next.value}')
