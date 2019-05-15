import copy
import typing

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.card.deck as deck


class JsonDeck(deck.Deck, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_DECK_SCHEMA)

    def __init__(
            self,
            tier: int,
            card_list_in_order: typing.List[i_card.ICard]
    ):
        super(JsonDeck, self).__init__(
            tier,
            card_list_in_order
        )

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict,
            incomplete_game_state: i_incomplete_game_state.IIncompleteGameState
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        card_list = []
        state_card_manager = incomplete_game_state.get_card_manager()
        for card_name in json['cards']:
            if not state_card_manager.is_card_in_manager_by_name(card_name):
                raise ValueError("Card not in manager")
            card_list.append(state_card_manager.get_card_by_name(card_name))

        return cls(
            json['tier'],
            card_list
        )

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_DECK_SCHEMA)
