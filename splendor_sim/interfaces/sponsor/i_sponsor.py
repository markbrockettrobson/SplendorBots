import abc
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type


class ISponsor(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            victory_points: int,
            cost: typing.Dict[i_coin_type.ICoinType, int]
    ):
        """

        :param victory_points:
               <int>
        :param cost:
               <typing.Dict[i_coin_type.ICoinType, int]>
        """

    @abc.abstractmethod
    def get_victory_points(self) -> int:
        """

        :return: the number of victory points given by the sponsor
                 <int>
        """

    @abc.abstractmethod
    def get_cost(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        """

        :return: the cost of the sponsor
                 <typing.Dict[i_coin_type.ICoinType, int]>
        """
