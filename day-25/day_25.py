"""
https://adventofcode.com/2020/day/25

The handshake used by the card and the door involves an operation that
transforms a subject number. To transform a subject number, start with
the value 1. Then, a number of times called the loop size, perform the
following steps:
- Set the value to itself multiplied by the subject number.
- Set the value to the remainder after dividing the value by 20201227.

The card always uses a specific, secret loop size when it transforms a
subject number. The door always uses a different, secret loop size.

The cryptographic handshake works like this:
- The card transforms the subject number of 7 according to the card's secret
loop size. The result is called the card's public key.
- The door transforms the subject number of 7 according to the door's secret
loop size. The result is called the door's public key.
- The card and door use the wireless RFID signal to transmit the two public
keys (your puzzle input) to the other device. Now, the card has the door's
public key, and the door has the card's public key. Because you can
eavesdrop on the signal, you have both public keys, but neither device's
loop size.
- The card transforms the subject number of the door's public key according
to the card's loop size. The result is the encryption key.
- The door transforms the subject number of the card's public key according
to the door's loop size. The result is the same encryption key as the card
calculated.

"""

# Read input
with open('day-25/input.txt') as fp:
    card_public_key, door_public_key = [int(x) for x in fp.read().split('\n')]


def compute_loop_size(public_key):
    """

    Parameters
    ----------
    public_key : int
        public key

    Returns
    -------
    int : private loop size

    """

    value = 1
    subject_number = 7

    nloops = 0
    while value != public_key:
        value *= subject_number
        value = value % 20201227
        nloops += 1
    return nloops


def compute_encryption_key(public_key, loop_size):
    """

    Parameters
    ----------
    public_key : int
        public key
    loop_size : int
        number of loops

    Returns
    -------
    int : encryption key

    """
    value = 1
    subject_number = public_key
    for _ in range(loop_size):
        value *= subject_number
        value = value % 20201227
    return value


card_nloops = compute_loop_size(card_public_key)
door_nloops = compute_loop_size(door_public_key)

encryption_key = compute_encryption_key(door_public_key, card_nloops)
print(f'problem 1: {encryption_key}')
