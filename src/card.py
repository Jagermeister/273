from enum import Enum

cardsInDeckCount = 52
cardsInColorCount = 13

bitTemplate = (1 << cardsInDeckCount) - 1
# This should be a parameter (How many total
# cards? #60) but for clarity we keep it constant.
def bit_mask(index):
    return bitTemplate - (1 << index)

class Card:
    colorIndex = 0
    valueIndex = 1

    @staticmethod
    def add(container, cardIndex):
        return container | 1 << cardIndex

    @staticmethod
    def remove(container, cardIndex):
        return container & bit_mask(cardIndex)

    @staticmethod
    def color(index):
        return index // cardsInColorCount

    @staticmethod
    def value(index):
        return index % cardsInColorCount

    @staticmethod
    def to_index(card):
        color, value = card
        return cardsInColorCount * color + value

class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

class Value(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12
