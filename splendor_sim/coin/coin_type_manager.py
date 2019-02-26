import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager


class CoinTypeManager(i_coin_type_manager.ICoinTypeManager):

    def __init__(self,
                 coin_type_list: typing.List[i_coin_type.ICoinType],
                 coin_equivalents: typing.List[typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]]):

        self._coin_type_list = copy.copy(coin_type_list)

        self._usage_map = {}  # type: typing.Dict[i_coin_type.ICoinType, typing.List[i_coin_type.ICoinType]]
        self._equivalent_map = {}  # type: typing.Dict[i_coin_type.ICoinType, typing.List[i_coin_type.ICoinType]]
        for coin in self._coin_type_list:
            self._usage_map[coin] = [coin]
            self._equivalent_map[coin] = [coin]

        for coin, use in coin_equivalents:
            if (coin not in self._coin_type_list) or (use not in self._coin_type_list):
                raise ValueError("coin equivalents must be in coin type list")
            self._usage_map[coin].append(use)
            self._equivalent_map[use].append(coin)

    def get_coin_list(self) -> typing.List[i_coin_type.ICoinType]:
        return copy.copy(self._coin_type_list)

    def get_equivalent_coins(self,
                             coin_type: i_coin_type.ICoinType
                             ) -> typing.List[i_coin_type.ICoinType]:
        if coin_type not in self._coin_type_list:
            raise ValueError("coin type must be in coin type list")
        return copy.copy(self._equivalent_map[coin_type])

    def get_coin_usage(self,
                       coin_type: i_coin_type.ICoinType
                       ) -> typing.List[i_coin_type.ICoinType]:
        if coin_type not in self._coin_type_list:
            raise ValueError("coin type must be in coin type list")
        return copy.copy(self._usage_map[coin_type])
