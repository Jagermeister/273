""" Common utilities interacting with base classes """

from src.card import Card
from src.build import generate_cards_from_hands

def cards_from_deck(deck, cards):
    hand = 0
    for c, s in cards:
        card = Card.to_index((s.value, c.value))
        hand = Card.add(hand, card)
        deck = Card.remove(deck, card)

    return deck, hand

def card_index_from_hand(hand):
    index = 0
    while hand:
        if hand & 0b1:
            yield index

        index += 1
        hand = hand >> 1


def is_flush(h):
    return len(set(map(lambda i: Card.color(i), card_index_from_hand(h)))) == 1

def is_straight(h):
    values = sorted(list(map(lambda i: i%13, card_index_from_hand(h))))
    return len(set(values)) == 5 and values[-1] - values[0] == 4

def is_values_straight(vs):
    values = sorted(vs)
    return len(set(values)) == 5 and values[-1] - values[0] == 4

def unique_value_count(h):
    return len(set(map(lambda i: i%13, card_index_from_hand(h))))
