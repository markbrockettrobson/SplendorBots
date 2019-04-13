import abc
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type


class ICoinTypeManager(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            coin_type_list: typing.Set[i_coin_type.ICoinType],
            coin_equivalents: typing.Set[typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]]
    ):
        """

        :param coin_type_list: a list of all coin types
               <typing.Set[i_coin_type.ICoinType]>
        :param coin_equivalents: a list of tuples (coin, use) meaning that coin can be used as use as well
               all coins can be ued for costs of their own type
               <typing.Set[typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]]>
        """

    @abc.abstractmethod
    def get_coin_set(self) -> typing.Set[i_coin_type.ICoinType]:
        """

        :return: a list of all coin types
                 <typing.Set[i_coin_type.ICoinType]>
        """

    @abc.abstractmethod
    def get_equivalent_coins(
            self,
            coin_type: i_coin_type.ICoinType
    ) -> typing.Set[i_coin_type.ICoinType]:
        """

        :param coin_type: the coin type that you need to pay
               <i_coin_type.ICoinType>
        :return: a list of all coin type that can be used
                 <typing.Set[i_coin_type.ICoinType]>
        """

    @abc.abstractmethod
    def get_coin_usage(
            self,
            coin_type: i_coin_type.ICoinType
    ) -> typing.Set[i_coin_type.ICoinType]:
        """

        :param coin_type: the coin type that you have
               <i_coin_type.ICoinType>
        :return: a list of all coin type that it can be used for
                 <typing.Set[i_coin_type.ICoinType]>
        """

    @abc.abstractmethod
    def get_coin_by_name(
            self,
            name: str
    ) -> i_coin_type.ICoinType:
        """

        :param name: the name of the coin you want to get
               <str>
        :return: the coin type requested if in manager
                 <i_coin_type.ICoinType>
        """

    @abc.abstractmethod
    def is_coin_in_manager_by_name(
            self,
            name: str
    ) -> bool:
        """

        :param name: the name of the coin you want to get
               <str>
        :return: true if the manager has a coin with that name
                 <bool>
        """
