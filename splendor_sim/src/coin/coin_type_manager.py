import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager


class CoinTypeManager(i_coin_type_manager.ICoinTypeManager):
    def __init__(
        self,
        coin_type_set: typing.Set[i_coin_type.ICoinType],
        coin_equivalents: typing.Set[
            typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]
        ],
    ):

        self._coin_type_set = copy.copy(coin_type_set)

        self._usage_map = (
            {}
        )  # type: typing.Dict[i_coin_type.ICoinType, typing.Set[i_coin_type.ICoinType]]
        self._equivalent_map = (
            {}
        )  # type: typing.Dict[i_coin_type.ICoinType, typing.Set[i_coin_type.ICoinType]]
        for coin in self._coin_type_set:
            self._usage_map[coin] = {coin}
            self._equivalent_map[coin] = {coin}

        for coin, use in coin_equivalents:
            if (coin not in self._coin_type_set) or (use not in self._coin_type_set):
                raise ValueError("coin equivalents must be in coin type set")
            self._usage_map[coin].add(use)
            self._equivalent_map[use].add(coin)

        self._create_name_map()

    def get_coin_set(self) -> typing.Set[i_coin_type.ICoinType]:
        return copy.copy(self._coin_type_set)

    def get_equivalent_coins(
        self, coin_type: i_coin_type.ICoinType
    ) -> typing.Set[i_coin_type.ICoinType]:
        if coin_type not in self._coin_type_set:
            raise ValueError("coin type must be in coin type set")
        return copy.copy(self._equivalent_map[coin_type])

    def get_coin_usage(
        self, coin_type: i_coin_type.ICoinType
    ) -> typing.Set[i_coin_type.ICoinType]:
        if coin_type not in self._coin_type_set:
            raise ValueError("coin type must be in coin type set")
        return copy.copy(self._usage_map[coin_type])

    def _create_name_map(self):
        self._name_map = {}  # type: typing.Dict[str, i_coin_type.ICoinType]
        for coin in self._coin_type_set:
            if coin.get_name() in self._name_map:
                raise ValueError("Two coins can not have the same name.")
            self._name_map[coin.get_name()] = coin

    def get_coin_by_name(self, name: str) -> i_coin_type.ICoinType:
        if not self.is_coin_in_manager_by_name(name):
            raise ValueError("No coin of that name in manager.")
        return self._name_map[name]

    def is_coin_in_manager_by_name(self, name: str) -> bool:
        return name in self._name_map

    def get_name_set(self) -> typing.Set[str]:
        return set(self._name_map.keys())

    def to_json(self) -> typing.Dict:
        coin_equivalents = []
        for coin, use_set in self._usage_map.items():
            for use in use_set:
                if coin is not use:
                    coin_equivalents.append(
                        {
                            "coin_name": coin.get_name(),
                            "equivalent_coins_name": use.get_name(),
                        }
                    )
        return {
            "coin_types": [coin.to_json() for coin in self.get_coin_set()],
            "coin_equivalents": coin_equivalents,
        }
