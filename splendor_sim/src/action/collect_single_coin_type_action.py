import copy
import typing

import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.action.i_action as i_action
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.player.i_player as i_player


class CollectSingleCoinTypeAction(i_action.IAction):

    def __init__(
            self,
            valid_coin_type_set: typing.Set[i_coin_type.ICoinType],
            current_player: i_player.IPlayer,
            coins: typing.Dict[i_coin_type.ICoinType, int],
    ):
        self._validate_input(valid_coin_type_set, coins)
        self._coin_dictionary = copy.copy(coins)
        coin_type, number_of_coins = copy.copy(coins).popitem()
        self._current_player = current_player
        self._coin_type = coin_type
        self._number_of_coins = number_of_coins

    def validate(self, game_state: i_game_state.IGameState) -> bool:
        return game_state.get_coin_reserve().has_minimum(self._coin_dictionary)

    def execute(self, game_state: i_game_state.IGameState) -> None:
        if not self.validate(game_state):
            raise ValueError("invalid action")
        test_dictionary = {}
        print()
        for coin, number in self._coin_dictionary.items():
            test_dictionary[coin] = number + 2
        game_state.get_coin_reserve().remove_coins(test_dictionary)
        self._current_player.get_coin_inventory().add_coins(self._coin_dictionary)

    @staticmethod
    def _validate_input(
            valid_coin_type_set: typing.Set[i_coin_type.ICoinType],
            coins: typing.Dict[i_coin_type.ICoinType, int]
    ):
        if not len(coins.keys()) == 1:
            raise ValueError("can only take one type of coin")
        coin_type = list(coins.keys())[0]
        number_of_coins = coins[coin_type]
        if number_of_coins not in (1, 2):
            raise ValueError("can only take one or two coins")
        if coin_type not in valid_coin_type_set:
            raise ValueError("invalid coin type")
