import copy
import typing

import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.player_sponsor_inventory as player_sponsor_inventory


class JsonPlayerSponsorInventory(
    player_sponsor_inventory.PlayerSponsorInventory,
    i_json_buildable_object.IJsonBuildableObject,
):

    _JSON_VALIDATOR = json_validator.JsonValidator(
        json_schemas.JSON_PLAYER_SPONSOR_INVENTORY
    )

    def __init__(self, sponsors: typing.Set[i_sponsor.ISponsor]):
        super(JsonPlayerSponsorInventory, self).__init__(sponsors)

    @classmethod
    def build_from_json(
        cls,
        json: typing.Dict,
        incomplete_game_state: i_incomplete_game_state.IIncompleteGameState,
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        sponsor_manager = (
            incomplete_game_state.get_sponsor_reserve().get_sponsor_manager()
        )

        sponsors: typing.Set[i_sponsor.ISponsor] = set()
        for sponsor_name in json["sponsors"]:
            if not sponsor_manager.is_sponsor_in_manager_by_name(sponsor_name):
                raise ValueError("sponsor name not in manager.")
            sponsors.add(sponsor_manager.get_sponsor_by_name(sponsor_name))

        json_player_sponsor_inventory = cls(sponsors)

        return json_player_sponsor_inventory

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_PLAYER_SPONSOR_INVENTORY)
