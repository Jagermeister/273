''' Explore 2-7 Triple Draw Statistics '''

import logging
from operator import add
from random import choice
from timeit import default_timer

import numpy as np
import pandas as pd

from src.card import Card, Suit, Value
from src.deck import Deck
from src.utility import (
    card_index_from_hand,
    cards_from_deck,
    cards_value_minimal,
    fetch_card_cache,
    generate_cards_from_hands,
    fetch_hand_rankings,
    is_flush,
    is_straight,
    is_values_straight,
    unique_value_count
)


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)



def rank_hands(h2, h2_values_sorted, is_t2_flush, is_t2_straight, h1_unique_count, is_h1_flush, is_h1_straight, t1_values_sorted):
    h1c = h1_unique_count # unique_value_count(h1)
    h2c = len(set(h2_values_sorted)) # unique_value_count(h2)
    if h1c != h2c:
        return (1, 0, 0) if h1c > h2c else (0, 1, 0)

    h1f = is_h1_flush # is_flush(h1)
    h2f = is_t2_flush # is_flush(h2)
    if h1f != h2f:
        return (1, 0, 0) if h1f else (0, 1, 0)

    h1s = is_h1_straight # is_straight(h1)
    h2s = is_t2_straight # is_values_straight(h2_values_sorted) # is_straight(h2)
    if h1s != h2s:
        return (1, 0, 0) if h1s else (0, 1, 0)

    h1v = t1_values_sorted
    h2v = h2_values_sorted

    for a, b in zip(h1v, h2v):
        if a != b:
            return (1, 0, 0) if a < b else (0, 1, 0)

    return (0, 0, 1)


def simulate_deuce_to_seven(t1, p2, cards, trials, runs):
    scores = []
    cards_to_pull = 1

    t1_unique_count = unique_value_count(t1)
    _, is_t1_flush, is_t1_straight, t1_values_sorted = CARDS_FROM_HAND[t1]

    deck = list(card_index_from_hand(cards))
    for _ in range(trials):
        score = (0, 0, 0)
        for _ in range(runs):
            t2 = p2
            cards_added = set()
            cards_added_count = 0
            #for i in range(cards_to_pull):
            while cards_added_count < cards_to_pull:
                c = choice(deck)
                #c = Deck.cardPeek(cards, 52 - 9 - cards_added_count)
                if c not in cards_added:
                    t2 = Card.add(t2, c)
                    cards_added.add(c)
                    cards_added_count += 1

            _, is_t2_flush, is_t2_straight, t2_values_sorted = CARDS_FROM_HAND[t2]
            result = rank_hands(t2, t2_values_sorted, is_t2_flush, is_t2_straight, t1_unique_count, is_t1_flush, is_t1_straight, t1_values_sorted)
            score = tuple(map(add, score, result))

        scores.append(score)

    return zip(*scores)



WALLCLOCK = default_timer()
p1_suits = [Suit.CLUBS] + [Suit.HEARTS] * 4

LOGGER.info('Fetch Card Cache')
CARDS_FROM_HAND = fetch_card_cache()
LOGGER.info(f'Card Cache Ready, {round(default_timer() - WALLCLOCK, 2)}')
WALLCLOCK = default_timer()

#import cProfile, pstats, io
#pr = cProfile.Profile()
#pr.enable()

TRIALS = 5
RUNS = 500
TOP_HANDS_COUNT = 246
HAND_RANKINGS = fetch_hand_rankings()[:TOP_HANDS_COUNT]

card_char = lambda c: str(c + 2) if c < 8 else { 8: 'T', 9: 'J', 10: 'Q',  11: 'K', 12: 'A' }[c]
results = pd.DataFrame({'hands': ['-'.join(reversed([card_char(c.value) for c in v])) for v in HAND_RANKINGS]})

DRAWING_HANDS = [
    [(Value.TWO, Suit.DIAMONDS), (Value.THREE, Suit.SPADES), (Value.FOUR, Suit.SPADES), (Value.SEVEN, Suit.SPADES)],
    [(Value.TWO, Suit.DIAMONDS), (Value.THREE, Suit.SPADES), (Value.FOUR, Suit.SPADES), (Value.EIGHT, Suit.SPADES)],
    [(Value.TWO, Suit.DIAMONDS), (Value.THREE, Suit.SPADES), (Value.FOUR, Suit.SPADES), (Value.NINE, Suit.SPADES)],
    [(Value.TWO, Suit.DIAMONDS), (Value.THREE, Suit.SPADES), (Value.FOUR, Suit.SPADES), (Value.TEN, Suit.SPADES)],
    [(Value.TWO, Suit.DIAMONDS), (Value.THREE, Suit.SPADES), (Value.FOUR, Suit.SPADES), (Value.JACK, Suit.SPADES)]]

LOGGER.info(f'Simulating {len(DRAWING_HANDS)} hands drawing against the top {TOP_HANDS_COUNT} hands.')
for drawing_cards in DRAWING_HANDS:

    HAND_WALLCLOCK = default_timer()
    cards = Deck.create(52)
    cards, p2 = cards_from_deck(cards, drawing_cards)
    hand_name = '-'.join(reversed(list(cards_value_minimal(p2))))

    hand_results = []
    for hand in HAND_RANKINGS:
        p1 = 0
        sim_deck = cards
        for s, v in zip(p1_suits, hand):
            c = Card.to_index((s.value, v.value))
            p1 = Card.add(p1, c)
            sim_deck = Card.remove(sim_deck, c)

        wins, loses, ties = simulate_deuce_to_seven(p1, p2, sim_deck, TRIALS, RUNS)
        hand_results.append(round((RUNS-np.mean(loses))/RUNS*100, 2))
        #print(
        #    '-'.join(reversed(list(cards_value_minimal(p1)))),
        #    f'{round((RUNS-np.mean(loses))/RUNS*100, 2):.2f}% +/- {round((np.std(loses))/RUNS*100, 2):.2f}%',
        #    list(map(np.sum, (wins, loses, ties))),
        #    f'{round(time() - wallclock, 3)}s')

    results[hand_name] = hand_results
    LOGGER.info(f'{hand_name}, {round(default_timer() - HAND_WALLCLOCK, 2)}')

LOGGER.info(f'Simulation completed, {round(default_timer() - WALLCLOCK, 2)}')
results.to_csv('docs/results/frame.csv')

#pr.disable()
#s = io.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print(s.getvalue())
