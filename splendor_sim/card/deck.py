import copy
import typing
import random
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_deck as i_deck


class Deck(i_deck.IDeck):
    def __init__(self, card_list: typing.List[i_card.ICard]):
        self._card_list = copy.copy(card_list)
        random.shuffle(self._card_list)

    def has_next(self) -> bool:
        return len(self._card_list) > 0

    def next(self) -> i_card.ICard:
        return self._card_list.pop()

    def number_remaining_cards(self) -> int:
        return len(self._card_list)
