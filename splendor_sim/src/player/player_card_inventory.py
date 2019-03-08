import copy
import typing

import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory


class PlayerCardInventory(i_player_card_inventory.IPlayerCardInventory):

    def __init__(self, max_reserved_cards: int):
        if max_reserved_cards < 0:
            raise ValueError("max_reserved_cards must be zero or more")
        self._max_reserved_cards = max_reserved_cards
        self._number_of_reserved_cards = 0  # type: int
        self._reserved_cards = set()  # type: typing.Set[i_card.ICard]
        self._cards = set()  # type: typing.Set[i_card.ICard]
        self._total_discount = {}  # type: typing.Dict[i_coin_type.ICoinType, int]
        self._victory_points = 0  # type: int

    def get_max_number_of_reserved_cards(self) -> int:
        return self._max_reserved_cards

    def get_number_of_reserved_cards(self) -> int:
        return self._number_of_reserved_cards

    def add_card(self, card: i_card.ICard) -> None:
        if card in self._cards:
            raise ValueError("card already in card list")
        self._cards.add(card)
        self._add_to_total_discount(card.get_discount())
        self._victory_points += card.get_victory_points()

    def add_card_to_reserved(self, card: i_card.ICard) -> None:
        if card in self._reserved_cards:
            raise ValueError("card already in reserved cards")
        if self._number_of_reserved_cards >= self._max_reserved_cards:
            raise ValueError("can not reserve more cards")
        self._reserved_cards.add(card)
        self._number_of_reserved_cards += 1

    def get_total_discount(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        return copy.copy(self._total_discount)

    def get_victory_points(self) -> int:
        return self._victory_points

    def get_card_list(self) -> typing.List[i_card.ICard]:
        return list(self._cards)

    def get_reserved_card_list(self) -> typing.List[i_card.ICard]:
        return list(self._reserved_cards)

    def _add_to_total_discount(self, new_discount: i_coin_type.ICoinType) -> None:
        if new_discount not in self._total_discount:
            self._total_discount[new_discount] = 0
        self._total_discount[new_discount] += 1

    def remove_from_reserved_card_list(self, card: i_card.ICard) -> None:
        if card not in self._reserved_cards:
            raise ValueError("card is not in reserved cards")
        self._reserved_cards.remove(card)
        self._number_of_reserved_cards -= 1
