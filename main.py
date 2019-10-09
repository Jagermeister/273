''' Explore 2-7 Triple Draw Statistics '''

from operator import add
from time import time

import numpy as np

from src.deck import Deck
from src.card import Card, Suit, Value


def cards_from_deck(deck, cards):
    hand = 0
    for c, s in cards:
        card = Card.to_index((s.value, c.value))
        hand = Card.add(hand, card)
        deck = Card.remove(deck, card)

    return deck, hand

def cards_display(hand):
    index = 0
    while hand:
        if hand & 0b1:
            print(Value(Card.value(index)).name, Suit(Card.color(index)).name[0].lower(), end='; ')
        index += 1
        hand = hand >> 1

def cards_value_minimal(hand):
    index = 0
    while hand:
        if hand & 0b1:
            v = Card.value(index)
            if v < 8:
                yield str(v + 2)
            elif v == 8:
                yield 'T'
            elif v == 9:
                yield 'J'
            elif v == 10:
                yield 'Q'
            elif v == 11:
                yield 'K'
            elif v == 12:
                yield 'A'

        index += 1
        hand = hand >> 1

def cards_from_hand(hand):
    index = 0
    while hand:
        if hand & 0b1:
            yield index

        index += 1
        hand = hand >> 1


def is_flush(h):
    return len(set(map(lambda i: Card.color(i), cards_from_hand(h)))) == 1

def is_straight(h):
    values = sorted(list(map(lambda i: i%13, cards_from_hand(h))))
    return len(set(values)) == 5 and values[-1] - values[0] == 4

def is_values_straight(vs):
    values = sorted(vs)
    return len(set(values)) == 5 and values[-1] - values[0] == 4

def unique_value_count(h):
    return len(set(map(lambda i: i%13, cards_from_hand(h))))


def rank_hands(h2, h2_values_sorted, h1_unique_count, is_h1_flush, is_h1_straight, t1_values_sorted):
    h1c = h1_unique_count # unique_value_count(h1)
    h2c = len(set(h2_values_sorted)) # unique_value_count(h2)
    if h1c != h2c:
        return (1, 0, 0) if h1c > h2c else (0, 1, 0)

    h1f = is_h1_flush # is_flush(h1)
    h2f = is_flush(h2)
    if h1f != h2f:
        return (1, 0, 0) if h1f else (0, 1, 0)

    h1s = is_h1_straight # is_straight(h1)
    h2s = is_values_straight(h2_values_sorted) # is_straight(h2)
    if h1s != h2s:
        return (1, 0, 0) if h1s else (0, 1, 0)

    h1v = t1_values_sorted # sorted(list(set(map(lambda i: i%13, cards_from_hand(h1)))), reverse=True)
    h2v = h2_values_sorted # sorted(list(set(map(lambda i: i%13, cards_from_hand(h2)))), reverse=True)

    for a, b in zip(h1v, h2v):
        if a != b:
            return (1, 0, 0) if a < b else (0, 1, 0)

    return (0, 0, 1)


def simulate_deuce_to_seven(t1, p2, cards):
    trials = 15
    runs = 2000

    wallclock = time()
    scores = []
    cards_to_pull = 1

    is_t1_flush = is_flush(t1)
    is_t1_straight = is_straight(t1)
    t1_unique_count = unique_value_count(t1)
    t1_values_sorted = sorted(list(set(map(lambda i: i%13, cards_from_hand(t1)))), reverse=True)

    for _ in range(trials):
        score = (0, 0, 0)
        for _ in range(runs):
            t2 = p2
            for i in range(cards_to_pull):
                c = Deck.cardPeek(cards, 52 - 9 - i)
                t2 = Card.add(t2, c)

            t2_values_sorted = sorted(list(map(lambda i: i%13, cards_from_hand(t2))), reverse=True)
            result = rank_hands(t2, t2_values_sorted, t1_unique_count, is_t1_flush, is_t1_straight, t1_values_sorted)
            score = tuple(map(add, score, result))

        scores.append(score)

    wins, loses, ties = zip(*scores)
    print('-'.join(reversed(list(cards_value_minimal(t1)))), f'{round((runs-np.mean(loses))/runs*100, 2):.2f}% +/- {round((np.std(loses))/runs*100, 2):.2f}%', list(map(np.sum, (wins, loses, ties))), f'{round(time() - wallclock, 3)}s')

from itertools import combinations

def is_value_enum_straight(values):
    values = sorted([v.value for v in values])
    return len(set(values)) == 5 and values [-1] - values[0] == 4

all_combos = list(filter(lambda h: not is_value_enum_straight(h), list(combinations(list(Value), 5))))
all_combos = sorted(all_combos, key=lambda cs: sorted([c.value for c in cs], reverse=True))

cards = Deck.create(52)
cards, p2 = cards_from_deck(cards, [
    (Value.TWO, Suit.DIAMONDS),
    (Value.THREE, Suit.SPADES),
    (Value.FOUR, Suit.DIAMONDS),
    (Value.EIGHT, Suit.SPADES)])
p1_suits = [Suit.CLUBS, Suit.HEARTS, Suit.HEARTS, Suit.HEARTS, Suit.HEARTS]

#import cProfile, pstats, io
#pr = cProfile.Profile()
#pr.enable()

#for hand in all_combos[:246]:
for hand in [all_combos[30]]:
    p1 = 0
    sim_deck = cards
    for s, v in zip(p1_suits, hand):
        c = Card.to_index((s.value, v.value))
        p1 = Card.add(p1, c)
        sim_deck = Card.remove(sim_deck, c)

    simulate_deuce_to_seven(p1, p2, sim_deck)

#pr.disable()
#s = io.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print(s.getvalue())