import abc
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type


class ICard(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        tier: int,
        victory_points: int,
        discount: i_coin_type.ICoinType,
        cost: typing.Dict[i_coin_type.ICoinType, int],
        name: str = None,
    ):
        """

        :param tier: the level or tier of the card
               <int>
        :param victory_points: the number of victory points that this card gives the payer
               <int>
        :param discount: the discount the card provides the owner
               <i_coin_type.ICoinType>
        :param cost: the cost of the card
               <typing.Dict[i_coin_type.ICoinType, int]>
        :param name: the name of the card will auto gen if None
               <str>
        """

    @abc.abstractmethod
    def get_tier(self) -> int:
        """

        :return: the level or tier of the card
                 <int>
        """

    @abc.abstractmethod
    def get_victory_points(self) -> int:
        """

        :return: the number of victory points that this card gives the payer
                 <int>
        """

    @abc.abstractmethod
    def get_discount(self) -> i_coin_type.ICoinType:
        """

        :return: the discount the card provides the owner
                 <i_coin_type.ICoinType>
        """

    @abc.abstractmethod
    def get_cost(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        """

        :return: the cost of the card
                 <typing.Dict[i_coin_type.ICoinType, int]>
        """

    @abc.abstractmethod
    def get_name(self) -> str:
        """

        :return: the name of the card
                 <str>
        """

    @abc.abstractmethod
    def to_json(self) -> typing.Dict:
        """

        :return: a json dict of the card
                 <typing.Dict>
        """
