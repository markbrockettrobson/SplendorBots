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
        coin_type, number_of_coins = coins.popitem()
        self._coin_dictionary = coins
        self._validate_input(valid_coin_type_set, coins)
        self._current_player = current_player
        self._coin_type = coin_type
        self._number_of_coins = number_of_coins

    def validate(self, game_state: i_game_state.IGameState) -> bool:
        return game_state.get_coin_reserve().has_minimum(self._coin_dictionary)

    def execute(self, game_state: i_game_state.IGameState) -> None:
        if not self.validate(game_state):
            raise ValueError("invalid action")
        game_state.get_coin_reserve().remove_coins(self._coin_dictionary)
        self._current_player.get_coin_inventory().add_coins(self._coin_dictionary)

    @staticmethod
    def _validate_input(
            valid_coin_type_set: typing.Set[i_coin_type.ICoinType],
            coins: typing.Dict[i_coin_type.ICoinType, int]
    ):
        if not len(coins.keys()) == 1:
            raise ValueError("can only take one type of coin")
        coin_type, number_of_coins = coins.popitem()
        if number_of_coins not in (1, 2):
            raise ValueError("can only take one or two coins")
        if coin_type not in valid_coin_type_set:
            raise ValueError("invalid coin type")
