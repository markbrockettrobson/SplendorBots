import abc

import splendor_sim.interfaces.card.i_card_manager as i_card_manager
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve


class IIncompleteGameState(abc.ABC):

    @abc.abstractmethod
    def __init__(
            self
    ):
        """

        """

    @abc.abstractmethod
    def set_player_manager(self, player_manager: i_player_manager.IPlayerManager) -> None:
        """

        :param player_manager:
               <i_player_manager.IPlayerManager>
        :return:
        """

    @abc.abstractmethod
    def get_player_manager(self) -> i_player_manager.IPlayerManager:
        """

        :return: the player_manager that is used to hold the state of the player
                 <i_player_manager.IPlayerManager>
        """

    @abc.abstractmethod
    def set_coin_reserve(self, coin_reserve: i_coin_reserve.ICoinReserve) -> None:
        """

        :param coin_reserve:
               <i_coin_reserve.ICoinReserve>
        :return:
        """

    @abc.abstractmethod
    def get_coin_reserve(self) -> i_coin_reserve.ICoinReserve:
        """

        :return: the coin_reserve that is used to hold the state of the coins
                 <i_coin_reserve.ICoinReserve>
        """

    @abc.abstractmethod
    def set_card_reserve(self, card_reserve: i_card_reserve.ICardReserve) -> None:
        """

        :param card_reserve:
               <i_card_reserve.ICardReserve>
        :return:
        """

    @abc.abstractmethod
    def get_card_reserve(self) -> i_card_reserve.ICardReserve:
        """

        :return: the card_reserve that is used to hold the state of the cards
                 <i_card_reserve.ICardReserve>
        """

    @abc.abstractmethod
    def set_sponsor_reserve(self, sponsor_reserve: i_sponsor_reserve.ISponsorReserve) -> None:
        """

        :param sponsor_reserve:
               <i_sponsor_reserve.ISponsorReserve>
        :return:
        """

    @abc.abstractmethod
    def get_sponsor_reserve(self) -> i_sponsor_reserve.ISponsorReserve:
        """

        :return: the sponsor_reserve that is used to hold the state of the sponsors
                 <i_sponsor_reserve.ISponsorReserve>
        """

    @abc.abstractmethod
    def get_card_manager(self) -> i_card_manager.ICardManager:
        """

        :return: the sponsor_reserve that is used to hold the state of the sponsors
                 <i_card_manager.ICardManager>
        """

    @abc.abstractmethod
    def set_card_manager(self, card_manager: i_card_manager.ICardManager) -> None:
        """

        :return: the sponsor_reserve that is used to hold the state of the sponsors
                 <i_card_manager.ICardManager>
        """
