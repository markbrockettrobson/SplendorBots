import abc
import typing

import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type


class IPlayerCoinInventory(abc.ABC):
    @abc.abstractmethod
    def __init__(self, coin_type_manager: i_coin_type_manager.ICoinTypeManager):
        """

        :param coin_type_manager: holds all the coin types
               <i_coin_type_manager.ICoinTypeManager>
        """

    @abc.abstractmethod
    def get_coins(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        """

        :return: dictionary mapping each coin type in the manager to the amount the player has
                 <typing.Dict[i_coin_type.ICoinType, int]>
        """

    @abc.abstractmethod
    def get_number_of_coins(self) -> int:
        """

        :return: the total number of coins in the inventory
        """

    @abc.abstractmethod
    def has_minimum(self, minimum: typing.Dict[i_coin_type.ICoinType, int]) -> bool:
        """

        :param minimum: dictionary mapping each coin type in the manager to the minimum amount to test against
               <typing.Dict[i_coin_type.ICoinType, int]>
        :return: true if the player has at least minimum coins of each type
                 <bool>
        """

    @abc.abstractmethod
    def add_coins(self, coins: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        """

        :param coins:  dictionary mapping each coin type in the manager to the amount of coins to add
               <typing.Dict[i_coin_type.ICoinType, int]>
        :return: None
        """

    @abc.abstractmethod
    def remove_coins(self, coins: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        """

        :param coins: dictionary mapping each coin type in the manager to the amount to remove
               <typing.Dict[i_coin_type.ICoinType, int]>
        :return: None
        """
