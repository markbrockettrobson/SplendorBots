import typing

from splendor_sim.interfaces.collection_rules.i_collection_rule import ICollectionRule
# todo document this


class SelectMultipleSameCoinsRule(ICollectionRule):

    _description_format = 'select up to {0} coins from one of {1}'

    def __init__(self,
                 max_number: int,
                 required_remaining_coins: int,
                 valid_color_ids: typing.List[int]):

        self._max_number = max_number
        self._required_remaining_coins = required_remaining_coins
        self._valid_color_ids = valid_color_ids
        self._description = self._description_format.format(self._max_number, self._valid_color_ids)

    def __str__(self) -> str:
        return self._description

    def is_valid(self,
                 requested_coins: typing.List[int],
                 current_reserves: typing.List[int]) -> bool:

        total_number_of_requested_coin_types = 0
        for coin, amount in enumerate(requested_coins):
            if amount > 0:
                total_number_of_requested_coin_types += 1
                if current_reserves[coin] - self._required_remaining_coins < amount or \
                   amount > self._max_number or \
                   coin not in self._valid_color_ids or \
                   total_number_of_requested_coin_types > 1:
                    return False
        return True

    def get_description(self) -> str:
        return self._description
