import copy
import typing

import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type


class CoinReserve(i_coin_reserve.ICoinReserve):

    def __init__(self, coin_type_manager: i_coin_type_manager.ICoinTypeManager):
        self._coin_type_manager = coin_type_manager
        self._coin_list = self._coin_type_manager.get_coin_list()
        self._max_coin_size = {coin: coin.get_total_number() for coin in self._coin_list} \
            # type: typing.Dict[i_coin_type.ICoinType, int]
        self._current_coins = {coin: coin.get_total_number() for coin in self._coin_list} \
            # type: typing.Dict[i_coin_type.ICoinType, int]

    def get_coins_remaining(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        return copy.copy(self._current_coins)

    def get_coins_maximum(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        return copy.copy(self._max_coin_size)

    def has_minimum(self, minimum: typing.Dict[i_coin_type.ICoinType, int]) -> bool:
        self._validate_input_dictionary(minimum)
        for coin, value in minimum.items():
            if self._current_coins[coin] < value:
                return False
        return True

    def add_coins(self, added_coins: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        self._validate_input_dictionary(added_coins)
        for coin, value in added_coins.items():
            if self._current_coins[coin] + value > self._max_coin_size[coin]:
                raise ValueError("add would set " + str(coin) + " above its max")
            self._current_coins[coin] += value

    def remove_coins(self, removed_coins: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        self._validate_input_dictionary(removed_coins)
        for coin, value in removed_coins.items():
            if self._current_coins[coin] - value < 0:
                raise ValueError("removed would set " + str(coin) + " bellow zero")
            self._current_coins[coin] -= value

    def _validate_input_dictionary(self, dictionary: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        for key in dictionary:
            if key not in self._coin_list:
                raise ValueError(str(key) + "is not a coin type in this Reserve")
