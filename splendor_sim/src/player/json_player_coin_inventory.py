import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.player_coin_inventory as player_coin_inventory


class JsonPlayerCoinInventory(
    player_coin_inventory.PlayerCoinInventory,
    i_json_buildable_object.IJsonBuildableObject,
):

    _JSON_VALIDATOR = json_validator.JsonValidator(
        json_schemas.JSON_PLAYER_COIN_INVENTORY
    )

    def __init__(
        self,
        coin_type_manager: i_coin_type_manager.ICoinTypeManager,
        current_coins: typing.Dict[i_coin_type.ICoinType, int],
    ):
        super(JsonPlayerCoinInventory, self).__init__(coin_type_manager, current_coins)

    @classmethod
    def build_from_json(
        cls,
        json: typing.Dict,
        incomplete_game_state: i_incomplete_game_state.IIncompleteGameState,
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        coin_type_manager = incomplete_game_state.get_coin_reserve().get_manager()
        coin_stocks = {}
        for coin_json in json["coin_stocks"]:
            coin_name = coin_json["coin_name"]
            count = coin_json["count"]
            if not coin_type_manager.is_coin_in_manager_by_name(coin_name):
                raise ValueError("coin name not in manager.")
            coin_stocks[coin_type_manager.get_coin_by_name(coin_name)] = count

        json_player_coin_inventory = cls(coin_type_manager, coin_stocks)

        return json_player_coin_inventory

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_PLAYER_COIN_INVENTORY)
