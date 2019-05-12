import copy
import typing
import random
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_deck as i_deck


class Deck(i_deck.IDeck):
    def __init__(self, tier: int, card_set: typing.Set[i_card.ICard]):
        if tier < 1:
            raise ValueError("tier must be greater than one")
        self._validate_card_list(tier, card_set)
        self._tier = tier
        self._remaining_card_set = copy.copy(card_set)
        self._card_list = list(copy.copy(card_set))
        random.shuffle(self._card_list)

    def get_tier(self) -> int:
        return self._tier

    def has_next(self) -> bool:
        return len(self._card_list) > 0

    def next(self) -> i_card.ICard:
        return_value = self._card_list.pop()
        self._remaining_card_set.remove(return_value)
        return return_value

    def number_remaining_cards(self) -> int:
        return len(self._card_list)

    def get_remaining_cards(self) -> typing.Set[i_card.ICard]:
        return copy.copy(self._remaining_card_set)

    def to_json(self):
        return {
            'cards': [
                card.get_name for card in self._card_list
            ],
            'tier': self._tier
        }

    @staticmethod
    def _validate_card_list(tier: int, card_set: typing.Set[i_card.ICard]):
        for card in card_set:
            if card.get_tier() != tier:
                raise ValueError("cards must all be of the correct tier")
