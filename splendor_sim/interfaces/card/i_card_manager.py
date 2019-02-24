import abc
import typing
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manger
import splendor_sim.interfaces.card.i_card as i_card


class ICardManager(abc.ABC):
    @abc.abstractmethod
    def __init__(self,
                 card_list: typing.List[i_card.ICard],
                 coin_type_manger: i_coin_type_manger.ICoinTypeManager):
        """

        :param card_list: a list of cards in the game
               <typing.List[i_card.ICoinType]>
        :param coin_type_manger: a coin manager holding all coin types
               <i_coin_type_manger.ICoinTypeManager>
        """

    @abc.abstractmethod
    def get_tiers(self) -> typing.List[int]:
        """

        :return: a list of all tiers
                 <typing.List[int]>
        """

    @abc.abstractmethod
    def get_card_list(self) -> typing.List[i_card.ICard]:
        """

        :return: a list of all cards
                <typing.List[i_card.ICoinType]>
        """

    @abc.abstractmethod
    def get_card_tier(self, tier: int) -> typing.List[i_card.ICard]:
        """

        :param tier: the tier to select
               <int>
        :return: a list of all cards in the given tier
                 <typing.List[i_card.ICoinType]>
        """
