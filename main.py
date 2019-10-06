''' Explore 2-7 Triple Draw Statistics '''

import time

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
            print(Value(Card.value(index)), Suit(Card.color(index)).name[0], end=' ')
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
    values = sorted(list(map(lambda i: Card.value(i), cards_from_hand(h))))
    return len(set(values)) == 5 and values [-1] - values[0] == 4

def unique_value_count(h):
    return len(set(map(lambda i: Card.value(i), cards_from_hand(h))))


def rank_hands(h1, h2):
    h1c = unique_value_count(h1)
    h2c = unique_value_count(h2)
    if h1c != h2c:
        return 1 if h1c > h2c else -1

    h1f = is_flush(h1)
    h2f = is_flush(h2)
    if h1f != h2f:
        return 1 if h1f else -1

    h1s = is_straight(h1)
    h2s = is_straight(h2)
    if h1s != h2s:
        return 1 if h1s else -1

    h1v = sorted(list(set(map(lambda i: Card.value(i), cards_from_hand(h1)))), reverse=True)
    h2v = sorted(list(set(map(lambda i: Card.value(i), cards_from_hand(h2)))), reverse=True)

    for a, b in zip(h1v, h2v):
        if a != b:
            return 1 if a < b else -1

    return 0



cards = Deck.create(52)
cards, p1 = cards_from_deck(cards, [
    (Value.TWO, Suit.HEARTS),
    (Value.THREE, Suit.CLUBS),
    (Value.FOUR, Suit.HEARTS),
    (Value.SIX, Suit.HEARTS),
    (Value.JACK, Suit.HEARTS)])

cards, p2 = cards_from_deck(cards, [
    (Value.TWO, Suit.CLUBS),
    (Value.THREE, Suit.SPADES),
    (Value.FOUR, Suit.HEARTS),
    (Value.JACK, Suit.HEARTS)])


scores = []
trials = 25
runs = 10000

wallclock = time.time()

cards_to_pull = 1
for j in range(trials):
    score = 0
    if j and j % 5 == 0:
        print(f'trail {j}/{trials} @ {runs}: {round(np.mean(scores)/runs*100, 3)}% +/- {round(np.std(scores)/runs*100, 3)}, {round(time.time() - wallclock, 3)}')

    for k in range(runs):
        t2 = p2
        for i in range(cards_to_pull):
            c = Deck.cardPeek(cards, 52 - 9 - i)
            t2 = Card.add(t2, c)

        winner = rank_hands(p1, t2)
        score += winner
        #print(score, winner, Value(Card.value(c)).name, Suit(Card.color(c)).name[0].lower())
        #cards_display(t2)

    scores.append(score)

print(f'{trials}x{runs}', round(np.mean(scores)/runs*100, 3), round(np.std(scores)/runs*100, 3), round(time.time() - wallclock, 3))
