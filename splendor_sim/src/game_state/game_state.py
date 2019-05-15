import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve
import splendor_sim.interfaces.coin.i_payment_manager as i_payment_manager
import splendor_sim.interfaces.game_state.i_game_state as i_game_state


class GameState(i_game_state.IGameState):
    def __init__(
            self,
            player_manager: i_player_manager.IPlayerManager,
            coin_reserve: i_coin_reserve.ICoinReserve,
            card_reserve: i_card_reserve.ICardReserve,
            sponsor_reserve: i_sponsor_reserve.ISponsorReserve,
            payment_manager: i_payment_manager.IPaymentManager
    ):
        self._player_manager = player_manager
        self._coin_reserve = coin_reserve
        self._card_reserve = card_reserve
        self._sponsor_reserve = sponsor_reserve
        self._payment_manager = payment_manager

    def get_player_manager(self) -> i_player_manager.IPlayerManager:
        return self._player_manager

    def get_coin_reserve(self) -> i_coin_reserve.ICoinReserve:
        return self._coin_reserve

    def get_card_reserve(self) -> i_card_reserve.ICardReserve:
        return self._card_reserve

    def get_sponsor_reserve(self) -> i_sponsor_reserve.ISponsorReserve:
        return self._sponsor_reserve

    def get_payment_manager(self) -> i_payment_manager.IPaymentManager:
        return self._payment_manager
