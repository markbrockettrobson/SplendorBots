import typing

import splendor_sim.interfaces.action.i_action as i_action
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor


class PurchaseCardAction(i_action.IAction):
    def __init__(self, current_player: i_player.IPlayer, sponsor: i_sponsor.ISponsor):
        self._current_player = current_player
        self._sponsor = sponsor

    def validate(self, game_state: i_game_state.IGameState) -> bool:
        if (
            self._sponsor
            in game_state.get_sponsor_reserve().get_remaining_sponsor_set()
        ):
            return self.validate_payment(
                self._current_player.get_card_inventory().get_total_discount(),
                self._sponsor.get_cost(),
            )
        return False

    def execute(self, game_state: i_game_state.IGameState) -> None:
        if not self.validate(game_state):
            raise ValueError("invalid action")
        self._current_player.get_sponsor_inventory().add_sponsor(self._sponsor)
        game_state.get_sponsor_reserve().remove_sponsor(self._sponsor)

    @staticmethod
    def validate_payment(
        total_discount: typing.Dict[i_coin_type.ICoinType, int],
        sponsor_cost: typing.Dict[i_coin_type.ICoinType, int],
    ) -> bool:
        for key, value in sponsor_cost.items():
            if key not in total_discount:
                return False
            if value > total_discount[key]:
                return False
        return True
