import abc
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type


class ICoinTypeManager(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            coin_type_list: typing.List[i_coin_type.ICoinType],
            coin_equivalents: typing.List[typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]]
    ):
        """

        :param coin_type_list: a list of all coin types
               <typing.List[i_coin_type.ICoinType]>
        :param coin_equivalents: a list of tuples (coin, use) meaning that coin can be used as use as well
               all coins can be ued for costs of their own type
               <typing.List[typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]]>
        """

    @abc.abstractmethod
    def get_coin_list(self) -> typing.List[i_coin_type.ICoinType]:
        """

        :return: a list of all coin types
                 <typing.List[i_coin_type.ICoinType]>
        """

    @abc.abstractmethod
    def get_equivalent_coins(
            self,
            coin_type: i_coin_type.ICoinType
    ) -> typing.List[i_coin_type.ICoinType]:
        """

        :param coin_type: the coin type that you need to pay
               <i_coin_type.ICoinType>
        :return: a list of all coin type that can be used
                 <typing.List[i_coin_type.ICoinType]>
        """

    @abc.abstractmethod
    def get_coin_usage(
            self,
            coin_type: i_coin_type.ICoinType
    ) -> typing.List[i_coin_type.ICoinType]:
        """

        :param coin_type: the coin type that you have
               <i_coin_type.ICoinType>
        :return: a list of all coin type that it can be used for
                 <typing.List[i_coin_type.ICoinType]>
        """
