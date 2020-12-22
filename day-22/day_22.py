"""
https://adventofcode.com/2020/day/22
"""

from collections import deque

# Read input: decks for two players of the game "Combat"
with open('day-22/input.txt') as fp:
    data = fp.read()
p1, p2 = data.split('\n\nPlayer 2:\n')
p1 = deque(map(int, p1.lstrip('Player 1: \n').split('\n')))
p2 = deque([int(x) for x in p2.split('\n')])
init = [list(p1.copy()), list(p2.copy())]

# Problem 1: what is the winning player's score?
while p1 and p2:
    card1 = p1.popleft()
    card2 = p2.popleft()
    if card1 > card2:
        p1.append(card1)
        p1.append(card2)
    else:
        p2.append(card2)
        p2.append(card1)
winning_deck = p1 if p1 else p2
score = sum((i+1)*c for i, c in enumerate(reversed(winning_deck)))
print(f'problem 1: {score}')

p1, p2 = init
games_played = dict()


def game(deck1, deck2, game_id):
    """
    Play a game of recursive combat.

    Parameters
    ----------
    deck1 : List[int]
        player 1's deck of cards
    deck2 : List[int]
        player 2's deck of cards
    game_id : int
        unique game identifier, where 0 corresponds to the root-level game

    Returns
    -------
    if `game_id` == 0:
        List[int] : winning player's deck
    else:
        str: 'p1' if `deck1` wins, else 'p2'

    """

    games_played[game_id] = set()
    games_played[game_id].add((tuple(deck1), tuple(deck2)))

    while deck1 and deck2:

        c1 = deck1[0]
        c2 = deck2[0]
        n1 = len(deck1) - 1
        n2 = len(deck2) - 1

        if n1 >= c1 and n2 >= c2:  # condition for playing sub-game
            subdeck1 = deck1[1:1+c1].copy()
            subdeck2 = deck2[1:1+c2].copy()
            winner = game(subdeck1, subdeck2, game_id+1)

        else:  # Update decks
            winner = 'p1' if c1 > c2 else 'p2'

        _ = deck1.pop(0)
        _ = deck2.pop(0)

        if winner == 'p1':
            deck1.append(c1)
            deck1.append(c2)
        else:
            deck2.append(c2)
            deck2.append(c1)

        if (tuple(deck1), tuple(deck2)) in games_played[game_id]:
            # player 1 automatically wins
            if not game_id:  # root game -- return winning deck
                return deck1
            return 'p1'
        else:
            games_played[game_id].add((tuple(deck1), tuple(deck2)))

    if not deck2:  # winner is p1
        return deck1 if not game_id else 'p1'
    else:
        return deck2 if not game_id else 'p2'


winning_deck = game(p1, p2, 0)
score = sum((i+1)*c for i, c in enumerate(reversed(winning_deck)))
print(f'problem 2: {score}')
