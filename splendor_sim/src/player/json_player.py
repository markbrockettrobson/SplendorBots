import copy
import typing

import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.json_player_card_inventory as json_player_card_inventory
import splendor_sim.src.player.json_player_coin_inventory as json_player_coin_inventory
import splendor_sim.src.player.json_player_sponsor_inventory as json_player_sponsor_inventory
import splendor_sim.src.player.player as player


class JsonPlayer(player.Player, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_PLAYER)

    def __init__(
        self,
        name: str,
        coin_inventory: i_player_coin_inventory.IPlayerCoinInventory,
        card_inventory: i_player_card_inventory.IPlayerCardInventory,
        sponsor_inventory: i_player_sponsor_inventory.IPlayerSponsorInventory,
    ):
        super(JsonPlayer, self).__init__(
            name, coin_inventory, card_inventory, sponsor_inventory
        )

    @classmethod
    def build_from_json(
        cls,
        json: typing.Dict,
        incomplete_game_state: i_incomplete_game_state.IIncompleteGameState,
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        name = json["name"]
        coin_inventory = json_player_coin_inventory.JsonPlayerCoinInventory.build_from_json(
            json["coin_inventory"], incomplete_game_state
        )
        card_inventory = json_player_card_inventory.JsonPlayerCardInventory.build_from_json(
            json["card_inventory"], incomplete_game_state
        )
        sponsor_inventory = json_player_sponsor_inventory.JsonPlayerSponsorInventory.build_from_json(
            json["sponsor_inventory"], incomplete_game_state
        )

        json_player = cls(name, coin_inventory, card_inventory, sponsor_inventory)

        return json_player

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_PLAYER)
