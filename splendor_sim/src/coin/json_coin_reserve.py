import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.coin.coin_reserve as coin_reserve
import splendor_sim.src.coin.json_coin_type_manager as json_coin_type_manager
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator


class JsonCoinReserve(
    coin_reserve.CoinReserve, i_json_buildable_object.IJsonBuildableObject
):

    _JSON_VALIDATOR = json_validator.JsonValidator(
        json_schemas.JSON_COIN_RESERVE_SCHEMA
    )

    def __init__(
        self,
        coin_type_manager: json_coin_type_manager.JsonCoinTypeManager,
        coin_stocks: typing.Dict[i_coin_type.ICoinType, int] = None,
    ):
        super(JsonCoinReserve, self).__init__(coin_type_manager, coin_stocks)

    @classmethod
    def build_from_json(
        cls,
        json: typing.Dict,
        incomplete_game_state: i_incomplete_game_state.IIncompleteGameState,
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        coin_type_manager = json_coin_type_manager.JsonCoinTypeManager.build_from_json(
            json["coin_type_manager"], incomplete_game_state
        )
        json_coin_reserve = cls(
            coin_type_manager,
            cls._make_coin_stocks(coin_type_manager, json["coin_stocks"]),
        )

        return json_coin_reserve

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_COIN_RESERVE_SCHEMA)

    @staticmethod
    def _make_coin_stocks(
        coin_type_manager: json_coin_type_manager.JsonCoinTypeManager, json: typing.List
    ) -> typing.Dict[i_coin_type.ICoinType, int]:
        coin_stock = {}
        name_set = coin_type_manager.get_name_set()
        for item in json:
            name = item["coin_name"]
            value = item["count"]
            if name not in name_set:
                raise ValueError("coin name not in coin manager")
            coin_stock[coin_type_manager.get_coin_by_name(name)] = value
        return coin_stock
