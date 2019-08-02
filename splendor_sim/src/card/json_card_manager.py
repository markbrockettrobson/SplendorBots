import copy
import typing

import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.card.card_manager as card_manager
import splendor_sim.src.card.json_card as json_card
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator


class JsonCardManager(card_manager.CardManager, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_CARD_MANAGER_SCHEMA)

    def __init__(
            self,
            card_set: typing.Set[i_card.ICard]
    ):
        super(JsonCardManager, self).__init__(
            card_set
        )

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict,
            incomplete_game_state: i_incomplete_game_state.IIncompleteGameState
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        card_set = set()
        for card_json in json["cards"]:
            card_set.add(json_card.JsonCard.build_from_json(card_json, incomplete_game_state))

        return cls(
            card_set
        )

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_CARD_MANAGER_SCHEMA)
