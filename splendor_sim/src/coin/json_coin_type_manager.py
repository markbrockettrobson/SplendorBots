import copy
import typing

import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.src.coin.coin_type_manager as coin_type_manager
import splendor_sim.src.coin.json_coin_type as json_buildable_coin_type


class JsonCoinTypeManager(coin_type_manager.CoinTypeManager, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_COIN_TYPE_MANAGER_SCHEMA)

    def __init__(
            self,
            coin_type_set: typing.Set[i_coin_type.ICoinType],
            coin_equivalents: typing.Set[typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]]
    ):
        super(JsonCoinTypeManager, self).__init__(coin_type_set, coin_equivalents)

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict
    ):

        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        coin_set = JsonCoinTypeManager._build_coin_type_set(
            json['coin_types']
        )
        coin_equivalents = JsonCoinTypeManager._build_coin_coin_equivalents(
            coin_set,
            json['coin_equivalents']
        )
        return cls(
            coin_set,
            coin_equivalents
        )

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_COIN_TYPE_MANAGER_SCHEMA)

    @staticmethod
    def _build_coin_type_set(json_coin_list: typing.List) -> typing.Set[i_coin_type.ICoinType]:
        return {
            json_buildable_coin_type.JsonCoinType.build_from_json(json_coin) for json_coin in json_coin_list
        }

    @staticmethod
    def _build_coin_coin_equivalents(
            coin_list: typing.Set[i_coin_type.ICoinType],
            json_coin_equivalents: typing.List
    ) -> typing.Set[typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]]:
        coin_equivalents = set()
        coin_name_map = {coin.get_name(): coin for coin in coin_list}

        for json_coin_equivalent in json_coin_equivalents:
            if json_coin_equivalent['coin_name'] not in coin_name_map.keys() or \
                 json_coin_equivalent['equivalent_coins_name'] not in coin_name_map.keys():
                raise ValueError("Coin equivalent name not in coin_types")
            coin_one = coin_name_map[json_coin_equivalent['coin_name']]
            coin_two = coin_name_map[json_coin_equivalent['equivalent_coins_name']]
            coin_equivalents.add((coin_one, coin_two))
        return coin_equivalents
