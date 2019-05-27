import copy
import typing

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.sponsor.json_sponsor as json_sponsor
import splendor_sim.src.sponsor.sponsor_manager as sponsor_manager


class JsonSponsorManager(sponsor_manager.SponsorManager, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_SPONSOR_MANAGER_SCHEMA)

    def __init__(
            self,
            sponsor_set: typing.Set[i_sponsor.ISponsor]
    ):
        super(JsonSponsorManager, self).__init__(sponsor_set)

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict,
            incomplete_game_state: i_incomplete_game_state.IIncompleteGameState
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        sponsor_set = set()  # type: typing.Set[i_sponsor.ISponsor]
        for sponsor_json in json["sponsors"]:
            sponsor_set.add(json_sponsor.JsonSponsor.build_from_json(sponsor_json, incomplete_game_state))

        return cls(
            sponsor_set
        )

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_SPONSOR_MANAGER_SCHEMA)
