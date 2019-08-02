import copy
import typing

import splendor_sim.interfaces.action.i_action as i_action
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.player.i_player as i_player


class ReserveCardAction(i_action.IAction):

    def __init__(
            self,
            valid_coin_type_set: typing.Set[i_coin_type.ICoinType],
            current_player: i_player.IPlayer,
            coins: typing.Dict[i_coin_type.ICoinType, int],
            card: i_card.ICard
    ):
        self._validate_input(valid_coin_type_set, coins)
        self._card = card
        self._coin_dictionary = copy.copy(coins)
        self._current_player = current_player

    def validate(self, game_state: i_game_state.IGameState) -> bool:
        number_of_reserved_cards = self._current_player.get_card_inventory().get_number_of_reserved_cards()
        max_number_of_reserved_cards = self._current_player.get_card_inventory().get_max_number_of_reserved_cards()
        if number_of_reserved_cards < max_number_of_reserved_cards:
            if self._card in game_state.get_card_reserve().get_cards_for_sale():
                if game_state.get_coin_reserve().has_minimum(self._coin_dictionary):
                    return True
        return False

    def execute(self, game_state: i_game_state.IGameState) -> None:
        if not self.validate(game_state):
            raise ValueError("invalid action")
        game_state.get_coin_reserve().remove_coins(self._coin_dictionary)
        game_state.get_card_reserve().remove_card(self._card)
        self._current_player.get_coin_inventory().add_coins(self._coin_dictionary)
        self._current_player.get_card_inventory().add_card_to_reserved(self._card)

    @staticmethod
    def _validate_input(
            valid_coin_type_set: typing.Set[i_coin_type.ICoinType],
            coins: typing.Dict[i_coin_type.ICoinType, int]
    ):
        if len(coins.keys()) != 1:
            raise ValueError("can only take 1 type of coin")
        for coin_type, number_of_coins in coins.items():
            if number_of_coins != 1:
                raise ValueError("can only take one coin")
            if coin_type not in valid_coin_type_set:
                raise ValueError("invalid coin type")
