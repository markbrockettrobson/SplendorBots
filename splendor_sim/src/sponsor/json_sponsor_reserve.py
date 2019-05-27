import copy
import typing

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_manager as i_sponsor_manager
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.sponsor.json_sponsor_manager as json_sponsor_manager
import splendor_sim.src.sponsor.sponsor_reserve as sponsor_reserve


class JsonSponsorReserve(sponsor_reserve.SponsorReserve, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_SPONSOR_RESERVE_SCHEMA)

    def __init__(
            self,
            sponsor_manager: i_sponsor_manager.ISponsorManager,
            sponsor_set: typing.Set[i_sponsor.ISponsor]
    ):
        super(JsonSponsorReserve, self).__init__(sponsor_manager, sponsor_set)

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict,
            incomplete_game_state: i_incomplete_game_state.IIncompleteGameState
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        sponsor_manager = json_sponsor_manager.JsonSponsorManager.build_from_json(
            json["sponsor_manager"],
            incomplete_game_state
        )

        sponsor_set = set()  # type: typing.Set[i_sponsor.ISponsor]
        for sponsor_name in json["sponsors"]:
            if not sponsor_manager.is_sponsor_in_manager_by_name(sponsor_name):
                raise ValueError("sponsor not in manager")
            sponsor_set.add(sponsor_manager.get_sponsor_by_name(sponsor_name))

        return cls(
            sponsor_manager,
            sponsor_set
        )

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_SPONSOR_RESERVE_SCHEMA)
