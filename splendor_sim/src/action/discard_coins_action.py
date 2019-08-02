import copy
import typing

import splendor_sim.interfaces.action.i_action as i_action
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.player.i_player as i_player


class DiscardCoinsAction(i_action.IAction):

    def __init__(
            self,
            valid_coin_type_set: typing.Set[i_coin_type.ICoinType],
            current_player: i_player.IPlayer,
            coins: typing.Dict[i_coin_type.ICoinType, int],
    ):
        self._total_coins = self._validate_input(valid_coin_type_set, coins)
        self._coin_dictionary = copy.copy(coins)
        self._current_player = current_player

    def validate(self, game_state: i_game_state.IGameState) -> bool:
        if self._current_player.get_coin_inventory().has_minimum(self._coin_dictionary):
            if self._current_player.get_coin_inventory().get_number_of_coins() - self._total_coins == 10:
                return True
        return False

    def execute(self, game_state: i_game_state.IGameState) -> None:
        if not self.validate(game_state):
            raise ValueError("invalid action")
        game_state.get_coin_reserve().add_coins(self._coin_dictionary)
        self._current_player.get_coin_inventory().remove_coins(self._coin_dictionary)

    @staticmethod
    def _validate_input(
            valid_coin_type_set: typing.Set[i_coin_type.ICoinType],
            coins: typing.Dict[i_coin_type.ICoinType, int]
    ):
        if not coins.keys():
            raise ValueError("must discard at least one types of coins")
        total_coins = 0
        for coin_type, number_of_coins in coins.items():
            if coin_type not in valid_coin_type_set:
                raise ValueError("invalid coin type")
            total_coins += number_of_coins
        if total_coins < 1:
            raise ValueError("must discard at least one coin")
        return total_coins
