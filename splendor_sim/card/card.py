import abc
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type

class ICoinType(abc.ABC):
    @abc.abstractmethod
    def __init__(self,
                 level: int,
                 victory_points: int,
                 discount: i_coin_type.ICoinType,
                 cost: typing.Dict[i_coin_type.ICoinType, int]):
        """

        :param level: the level or tear of the card
               <int>
        :param victory_points: the number of victory points that this card gives the payer
               <int>
        :param discount: The discount the card provides the owner
               <i_coin_type.ICoinType>
        :param cost: the cost of the card
               <typing.Dict[i_coin_type.ICoinType, int]>
        """
