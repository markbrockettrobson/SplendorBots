import abc
import typing

import splendor_sim.interfaces.data_types.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.data_types.i_coin_type as i_coin_type


class ICoinReserve(abc.ABC):
    @abc.abstractmethod
    def __init__(self, coin_type_manager: i_coin_type_manager.ICoinTypeManager):
        """

        :param coin_type_manager: holds all the coin types
               <i_coin_type_manager.ICoinTypeManager>
        """

    @abc.abstractmethod
    def get_coins_remaining(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        """

        :return: dictionary mapping each coin type in the manager to the remaining amount
                 <typing.Dict[i_coin_type.ICoinType, int]>
        """

    @abc.abstractmethod
    def get_coins_maximum(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        """

        :return: dictionary mapping each coin type in the manager to the maximum amount
                 <typing.Dict[i_coin_type.ICoinType, int]>
        """

    @abc.abstractmethod
    def has_minimum(self, minimum: typing.Dict[i_coin_type.ICoinType, int]) -> bool:
        """

        :param minimum: dictionary mapping each coin type in the manager to the minimum amount to test against
               <typing.Dict[i_coin_type.ICoinType, int]>
        :return: true if the reserve has at least minimum coins of each type
        """


    @abc.abstractmethod
    def add_coins(self, added_coins: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        """

        :param added_coins:  dictionary mapping each coin type in the manager to the amount of coins to add
               <typing.Dict[i_coin_type.ICoinType, int]>
        :return: None
        """

    @abc.abstractmethod
    def remove_coins(self, removed_coins: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        """

        :param removed_coins: dictionary mapping each coin type in the manager to the amount to remove
               <typing.Dict[i_coin_type.ICoinType, int]>
        :return:
        """
