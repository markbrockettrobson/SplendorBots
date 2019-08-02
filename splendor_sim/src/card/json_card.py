import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.card.card as card
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator


class JsonCard(card.Card, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_CARD_SCHEMA)

    def __init__(
            self,
            tier: int,
            victory_points: int,
            discount: i_coin_type.ICoinType,
            cost: typing.Dict[i_coin_type.ICoinType, int],
            name: str = None
    ):
        super(JsonCard, self).__init__(
            tier,
            victory_points,
            discount,
            cost,
            name
        )

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict,
            incomplete_game_state: i_incomplete_game_state.IIncompleteGameState
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")
        if not incomplete_game_state.get_coin_reserve():
            raise ValueError("Game state needs a coin reserve")

        coin_type_manager = incomplete_game_state.get_coin_reserve().get_manager()
        cls._validated_coin_name(json['discounted_coin_type_name'], coin_type_manager)

        for coin in json['cost']:
            coin_name = coin["coin_name"]
            cls._validated_coin_name(coin_name, coin_type_manager)

        coin_discount = coin_type_manager.get_coin_by_name(json['discounted_coin_type_name'])
        coin_costs = cls._build_coin_costs(json['cost'], coin_type_manager)

        return cls(
            json['tier'],
            json['victory_points'],
            coin_discount,
            coin_costs,
            json['name'],
        )

    @staticmethod
    def _validated_coin_name(
            coin_name: str,
            coin_type_manager: i_coin_type_manager.ICoinTypeManager
    ):
        if not coin_type_manager.is_coin_in_manager_by_name(coin_name):
            raise ValueError("Unknown discount coin type name ")

    @staticmethod
    def _build_coin_costs(
            json: typing.Dict,
            coin_type_manage: i_coin_type_manager.ICoinTypeManager,
    ) -> typing.Dict[i_coin_type.ICoinType, int]:
        coin_costs = {}
        for coin in json:
            coin_name = coin['coin_name']
            value = coin['count']
            coin_costs[coin_type_manage.get_coin_by_name(coin_name)] = value
        return coin_costs

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_CARD_SCHEMA)
