""" Supporting data structures """

from functools import reduce
from itertools import combinations


def generate_hands_from_deck(deck_card_count, hand_card_count):
    # Choose `hand_card_count` from `deck_card_count`
    deck = [(0b1 << i, i) for i in range(deck_card_count)]
    return combinations(deck, hand_card_count)

def generate_cards_from_hands():
    cards_by_hand = {}
    bitwise_or = lambda x, y: x ^ y
    for card_list in generate_hands_from_deck(52, 5):
        # (card_value, card_index)
        cards, indexes = zip(*card_list)
        hand = reduce(bitwise_or, cards)
        cards_by_hand[hand] = indexes

    return cards_by_hand