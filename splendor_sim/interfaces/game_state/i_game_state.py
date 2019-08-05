import abc

import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_payment_manager as i_payment_manager
import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve


class IGameState(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        player_manager: i_player_manager.IPlayerManager,
        coin_reserve: i_coin_reserve.ICoinReserve,
        card_reserve: i_card_reserve.ICardReserve,
        sponsor_reserve: i_sponsor_reserve.ISponsorReserve,
        payment_manager: i_payment_manager.IPaymentManager,
    ):
        """

        :param player_manager: used to hold the state of the player
               <i_player_manager.IPlayerManager>
        :param coin_reserve: used to hold the state of the coins
               <i_coin_reserve.ICoinReserve>
        :param card_reserve: used to hold the state of the cards
               <i_card_reserve.ICardReserve>
        :param sponsor_reserve: used to hold the state of the sponsors
               <i_sponsor_reserve.ISponsorReserve>
        :param payment_manager: used to test if payments are valid
               <i_payment_manager.IPaymentManager>
        """

    @abc.abstractmethod
    def get_player_manager(self) -> i_player_manager.IPlayerManager:
        """

        :return: the player_manager that is used to hold the state of the player
                 <i_player_manager.IPlayerManager>
        """

    @abc.abstractmethod
    def get_coin_reserve(self) -> i_coin_reserve.ICoinReserve:
        """

        :return: the coin_reserve that is used to hold the state of the coins
                 <i_coin_reserve.ICoinReserve>
        """

    @abc.abstractmethod
    def get_card_reserve(self) -> i_card_reserve.ICardReserve:
        """

        :return: the card_reserve that is used to hold the state of the cards
                 <i_card_reserve.ICardReserve>
        """

    @abc.abstractmethod
    def get_sponsor_reserve(self) -> i_sponsor_reserve.ISponsorReserve:
        """

        :return: the sponsor_reserve that is used to hold the state of the sponsors
                 <i_sponsor_reserve.ISponsorReserve>
        """

    @abc.abstractmethod
    def get_payment_manager(self) -> i_payment_manager.IPaymentManager:
        """

        :return: the payment_manager that is used to test if payments are valid
                 <i_payment_manager.IPaymentManager>
        """
