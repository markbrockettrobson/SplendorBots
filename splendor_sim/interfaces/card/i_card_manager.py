import abc
import typing
import splendor_sim.interfaces.card.i_card as i_card


class ICardManager(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            card_set: typing.Set[i_card.ICard]
    ):
        """

        :param card_set: a set of cards in the game
               <typing.Set[i_card.ICoinType]>
        """

    @abc.abstractmethod
    def get_tiers(self) -> typing.Set[int]:
        """

        :return: a set of all tiers
                 <typing.Set[int]>
        """

    @abc.abstractmethod
    def get_card_set(self) -> typing.Set[i_card.ICard]:
        """

        :return: a set of all cards
                <typing.Set[i_card.ICoinType]>
        """

    @abc.abstractmethod
    def get_card_tier(self, tier: int) -> typing.Set[i_card.ICard]:
        """

        :param tier: the tier to select
               <int>
        :return: a set of all cards in the given tier
                 <typing.Set[i_card.ICoinType]>
        """
