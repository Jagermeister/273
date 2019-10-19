""" Common utilities interacting with base classes """

import logging
import os
import json

from functools import reduce
from itertools import combinations

from src.card import Card, Value


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


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



def generate_hands_from_deck(deck_card_count, hand_card_count):
    # Choose `hand_card_count` from `deck_card_count`
    deck = [(0b1 << i, i) for i in range(deck_card_count)]
    return combinations(deck, hand_card_count)

# Provide hand ranking information:
# Hand Id, Card Values
# Jacks or better; Two Pair; 3 of a kind; Straight; Flush; Full House;
# 4 5s throu Kinds; 4 2s, 3s, 4s; 4 Aces; 4 2s, 3s, 4s w/Ace,2,3,4;
# 4 Aces with any 2,3,4; Straight Flush; Royal Flush;
def generate_cards_from_hands():
    cards_by_hand = {}
    bitwise_or = lambda x, y: x ^ y
    card_value_from_index = lambda i: i % 13
    for i, card_list in enumerate(generate_hands_from_deck(52, 5)):
        # (card_value, card_index)
        if i and i % 250000 == 0:
            LOGGER.info(f'..cached {i} hands..')
        cards, indexes = zip(*card_list)
        hand = reduce(bitwise_or, cards)
        cards_by_hand[hand] = (
            indexes,
            is_flush(hand),
            is_straight(hand),
            sorted(list(set(map(card_value_from_index, indexes))), reverse=True)
        )

    return cards_by_hand


def fetch_hand_rankings():
    """ 2-7 hand rankings """
    def is_value_enum_straight(values):
        values = sorted([v.value for v in values])
        return len(set(values)) == 5 and values [-1] - values[0] == 4

    all_combos = list(filter(lambda h: not is_value_enum_straight(h), list(combinations(list(Value), 5))))
    return sorted(all_combos, key=lambda cs: sorted([c.value for c in cs], reverse=True))

def fetch_card_cache():
    if os.path.exists('data/lookup.json'):
        with open('data/lookup.json') as f:
            return dict(json.load(f))

    card_cache = generate_cards_from_hands()
    with open('data/lookup.json', 'w') as f:
        json.dump(list(card_cache.items()), f)

    return card_cache


def cards_value_minimal(hand):
    index = 0
    values = { 8: 'T', 9: 'J', 10: 'Q',  11: 'K', 12: 'A' }
    while hand:
        if hand & 0b1:
            v = Card.value(index)
            yield str(v + 2) if v < 8 else values[v]

        index += 1
        hand = hand >> 1
