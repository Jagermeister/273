""" Common utilities interacting with base classes """


from functools import reduce
from itertools import combinations

from src.card import Card


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

def generate_cards_from_hands():
    cards_by_hand = {}
    bitwise_or = lambda x, y: x ^ y
    for i, card_list in enumerate(generate_hands_from_deck(52, 5)):
        # (card_value, card_index)
        if i and i % 250000 == 0:
            print(f'..cached {i} hands..')
        cards, indexes = zip(*card_list)
        hand = reduce(bitwise_or, cards)
        cards_by_hand[hand] = (indexes, is_flush(hand), is_straight(hand))

    return cards_by_hand