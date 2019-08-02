import copy
import typing

import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.player.player_card_inventory as player_card_inventory


class JsonPlayerCardInventory(player_card_inventory.PlayerCardInventory, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_PLAYER_CARD_INVENTORY)

    def __init__(
            self,
            max_reserved_cards: int,
            reserved_cards: typing.Set[i_card.ICard],
            cards: typing.Set[i_card.ICard]
    ):
        super(JsonPlayerCardInventory, self).__init__(max_reserved_cards, reserved_cards, cards)

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict,
            incomplete_game_state: i_incomplete_game_state.IIncompleteGameState
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        card_manager = incomplete_game_state.get_card_manager()

        reserved_cards: typing.Set[i_card.ICard] = set()
        for card_name in json["reserved_cards"]:
            if not card_manager.is_card_in_manager_by_name(card_name):
                raise ValueError("card name not in manager.")
            reserved_cards.add(card_manager.get_card_by_name(card_name))

        cards: typing.Set[i_card.ICard] = set()
        for card_name in json["cards"]:
            if not card_manager.is_card_in_manager_by_name(card_name):
                raise ValueError("card name not in manager.")
            cards.add(card_manager.get_card_by_name(card_name))

        json_player_card_inventory = cls(
            json["max_reserved_cards"],
            reserved_cards,
            cards
        )

        return json_player_card_inventory

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_PLAYER_CARD_INVENTORY)
