import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.sponsor.sponsor as sponsor


class JsonSponsor(sponsor.Sponsor, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_SPONSOR_SCHEMA)

    def __init__(
            self,
            name: str,
            victory_points: int,
            cost: typing.Dict[i_coin_type.ICoinType, int]
    ):
        super(JsonSponsor, self).__init__(name, victory_points, cost)

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict,
            incomplete_game_state: i_incomplete_game_state.IIncompleteGameState
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        coin_manager = incomplete_game_state.get_coin_reserve().get_manager()
        cost = {}  # type: typing.Dict[i_coin_type.ICoinType, int]

        for coin_json in json["cost"]:
            coin_name = coin_json["coin_name"]
            count = coin_json["count"]

            if not coin_manager.is_coin_in_manager_by_name(coin_name):
                raise ValueError("coin not in manager")
            coin = coin_manager.get_coin_by_name(coin_name)
            if coin in cost:
                raise ValueError("coin name repeated")
            cost[coin] = count
            
        return cls(
            json['name'],
            json['victory_points'],
            cost
        )

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_SPONSOR_SCHEMA)
