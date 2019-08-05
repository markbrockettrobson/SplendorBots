import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory


class PlayerCoinInventory(i_player_coin_inventory.IPlayerCoinInventory):
    def __init__(
        self,
        coin_type_manager: i_coin_type_manager.ICoinTypeManager,
        current_coins: typing.Dict[i_coin_type.ICoinType, int],
    ):
        self._coin_type_manager = coin_type_manager
        self._coin_set = self._coin_type_manager.get_coin_set()
        self._validate_input_dictionary(current_coins)
        self._current_coins = current_coins
        self._number_of_current_coins = 0

    def get_coins(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        return copy.copy(self._current_coins)

    def get_number_of_coins(self) -> int:
        return self._number_of_current_coins

    def has_minimum(self, minimum: typing.Dict[i_coin_type.ICoinType, int]) -> bool:
        self._validate_input_dictionary(minimum)
        for coin, value in minimum.items():
            if self._current_coins[coin] < value:
                return False
        return True

    def add_coins(self, coins: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        self._validate_input_dictionary(coins)
        for coin, value in coins.items():
            if coin not in self._current_coins:
                self._current_coins[coin] = 0
            self._current_coins[coin] += value
            self._number_of_current_coins += value

    def remove_coins(self, coins: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        self._validate_input_dictionary(coins)
        for coin, value in coins.items():
            if self._current_coins[coin] - value < 0:
                raise ValueError("removed would set " + str(coin) + " bellow zero")
            self._current_coins[coin] -= value
            self._number_of_current_coins -= value
            if self._current_coins[coin] == 0:
                self._current_coins.pop(coin)

    def _validate_input_dictionary(
        self, dictionary: typing.Dict[i_coin_type.ICoinType, int]
    ) -> None:
        for key in dictionary:
            if key not in self._coin_set:
                raise ValueError(str(key) + "is not a coin type in this Reserve")

    def to_json(self) -> typing.Dict:
        coin_json = []
        for coin, value in self._current_coins.items():
            if value > 0:
                coin_json.append({"coin_name": coin.get_name(), "count": value})

        return {"coin_stocks": coin_json}
