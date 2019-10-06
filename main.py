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
        return (1, 0, 0) if h1c > h2c else (0, 1, 0)

    h1f = is_flush(h1)
    h2f = is_flush(h2)
    if h1f != h2f:
        return (1, 0, 0) if h1f else (0, 1, 0)

    h1s = is_straight(h1)
    h2s = is_straight(h2)
    if h1s != h2s:
        return (1, 0, 0) if h1s else (0, 1, 0)

    h1v = sorted(list(set(map(lambda i: Card.value(i), cards_from_hand(h1)))), reverse=True)
    h2v = sorted(list(set(map(lambda i: Card.value(i), cards_from_hand(h2)))), reverse=True)

    for a, b in zip(h1v, h2v):
        if a != b:
            return (1, 0, 0) if a < b else (0, 1, 0)

    return (0, 0, 1)



cards = Deck.create(52)
cards, p1 = cards_from_deck(cards, [
    (Value.TWO, Suit.HEARTS),
    (Value.THREE, Suit.CLUBS),
    (Value.FOUR, Suit.HEARTS),
    (Value.FIVE, Suit.HEARTS)])

single_draw_top = [
    Value.EIGHT, Value.NINE, Value.TEN, Value.JACK, Value.QUEEN, Value.KING, Value.ACE
]

cards, p2 = cards_from_deck(cards, [
    (Value.TWO, Suit.CLUBS),
    (Value.THREE, Suit.SPADES),
    (Value.FOUR, Suit.HEARTS),
    (Value.SEVEN, Suit.SPADES)])

from operator import add

trials = 25
runs = 2000

wallclock = time.time()


all_cards_picked = []
for high_card in single_draw_top:
    t1 = Card.add(p1, Card.to_index((Suit.HEARTS.value, high_card.value)))

    scores = []
    cards_to_pull = 1
    for j in range(trials):
        score = (0, 0, 0)
        #if j and j % 5 == 0:
        #    print(f'trail {j}/{trials} @ {runs}: {round(np.mean(scores)/runs*100, 3)}% +/- {round(np.std(scores)/runs*100, 3)}, {round(time.time() - wallclock, 3)}')

        for k in range(runs):
            t2 = p2
            for i in range(cards_to_pull):
                c = Deck.cardPeek(cards, 52 - 9 - i)
                t2 = Card.add(t2, c)

            result = rank_hands(t1, t2)
            score = tuple(map(add, score, result))

        scores.append(score)

    cards_display(t1)
    print()
    wins, loses, ties = zip(*scores)
    print(f'{trials}x{runs}', f'{round(np.mean(wins)/runs*100, 2)}% +/- {round(np.std(wins)/runs*100, 2)}%', f'{round(time.time() - wallclock, 3)}s')

#print(f'Drawing to {len(set(all_cards_picked))} for {round(len(set(all_cards_picked))/47*100, 1)}%. Ran {round(len(all_cards_picked)/(trials*runs)*100, 1)}%')
