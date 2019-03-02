import copy
import typing
import random
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_deck as i_deck


class Deck(i_deck.IDeck):
    def __init__(self, tier: int, card_list: typing.List[i_card.ICard]):
        if tier < 1:
            raise ValueError("tier must be greater than one")
        self._validate_card_list(tier, card_list)
        self._tier = tier
        self._un_shuffled_card_list = set(copy.copy(card_list))
        self._card_list = copy.copy(card_list)
        random.shuffle(self._card_list)

    def get_tier(self) -> int:
        return self._tier

    def has_next(self) -> bool:
        return len(self._card_list) > 0

    def next(self) -> i_card.ICard:
        return_value = self._card_list.pop()
        self._un_shuffled_card_list.remove(return_value)
        return return_value

    def number_remaining_cards(self) -> int:
        return len(self._card_list)

    def get_remaining_cards(self) -> typing.Set[i_card.ICard]:
        return copy.copy(self._un_shuffled_card_list)

    @staticmethod
    def _validate_card_list(tier: int, card_list: typing.List[i_card.ICard]):
        for card in card_list:
            if card.get_tier() != tier:
                raise ValueError("cards but all be of the correct tier")
