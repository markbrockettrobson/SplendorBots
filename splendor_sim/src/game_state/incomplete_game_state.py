import splendor_sim.interfaces.card.i_card_manager as i_card_manager
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve


class IncompleteGameState(i_incomplete_game_state.IIncompleteGameState):
    def __init__(self):
        self._player_manager = None
        self._coin_reserve = None
        self._card_reserve = None
        self._card_manager = None
        self._sponsor_reserve = None

    def set_player_manager(
        self, player_manager: i_player_manager.IPlayerManager
    ) -> None:
        self._player_manager = player_manager

    def get_player_manager(self) -> i_player_manager.IPlayerManager:
        if not self._player_manager:
            raise ValueError("no player manager")
        return self._player_manager

    def set_coin_reserve(self, coin_reserve: i_coin_reserve.ICoinReserve) -> None:
        self._coin_reserve = coin_reserve

    def get_coin_reserve(self) -> i_coin_reserve.ICoinReserve:
        if not self._coin_reserve:
            raise ValueError("no coin reserve")
        return self._coin_reserve

    def set_card_reserve(self, card_reserve: i_card_reserve.ICardReserve) -> None:
        self._card_reserve = card_reserve

    def get_card_reserve(self) -> i_card_reserve.ICardReserve:
        if not self._card_reserve:
            raise ValueError("no coin reserve")
        return self._card_reserve

    def set_sponsor_reserve(
        self, sponsor_reserve: i_sponsor_reserve.ISponsorReserve
    ) -> None:
        self._sponsor_reserve = sponsor_reserve

    def get_sponsor_reserve(self) -> i_sponsor_reserve.ISponsorReserve:
        if not self._sponsor_reserve:
            raise ValueError("no coin reserve")
        return self._sponsor_reserve

    def set_card_manager(self, card_manager: i_card_manager.ICardManager) -> None:
        self._card_manager = card_manager

    def get_card_manager(self) -> i_card_manager.ICardManager:
        if not self._card_manager:
            raise ValueError("no coin reserve")
        return self._card_manager
