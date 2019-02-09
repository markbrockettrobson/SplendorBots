import typing

from splendor_sim.interfaces.collection_rules.i_collection_rule import ICollectionRule
# todo document this


class SelectNDifferentRule(ICollectionRule):

    _description_format = 'select up to {0} different coins from {1}'

    def __init__(self,
                 max_number: int,
                 valid_color_ids: typing.List[int]):

        self._max_number = max_number
        self._valid_color_ids = valid_color_ids
        self._description = self._description_format.format(self._max_number, self._valid_color_ids)

    def __str__(self) -> str:
        return self._description

    def is_valid(self,
                 requested_coins: typing.List[int],
                 current_reserves: typing.List[int]) -> bool:

        total_number_of_requested_coins = 0
        for coin, amount in enumerate(requested_coins):
            total_number_of_requested_coins += amount
            if current_reserves[coin] < amount or \
               amount > 1 or \
               coin not in self._valid_color_ids or \
               total_number_of_requested_coins > self._max_number:
                return False
        return True

    def get_description(self) -> str:
        return self._description
