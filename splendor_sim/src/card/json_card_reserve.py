import copy
import typing

import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_card_manager as i_card_manager
import splendor_sim.interfaces.card.i_deck as i_deck
import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.card.card_reserve as card_reserve
import splendor_sim.src.card.json_card_manager as json_card_manager
import splendor_sim.src.card.json_deck as json_deck
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator


class JsonCardReserve(
    card_reserve.CardReserve, i_json_buildable_object.IJsonBuildableObject
):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_DECK_SCHEMA)

    def __init__(
        self,
        card_manager: i_card_manager.ICardManager,
        number_of_cards_on_sale: int,
        decks: typing.Set[i_deck.IDeck],
        cards_on_sale: typing.Set[i_card.ICard],
    ):
        super(JsonCardReserve, self).__init__(
            card_manager, number_of_cards_on_sale, decks, cards_on_sale
        )

    @classmethod
    def build_from_json(
        cls,
        json: typing.Dict,
        incomplete_game_state: i_incomplete_game_state.IIncompleteGameState,
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        card_manager = json_card_manager.JsonCardManager.build_from_json(
            json["card_manager"], incomplete_game_state
        )
        incomplete_game_state.set_card_manager(card_manager)

        number_of_cards_on_sale = json["number_of_cards_on_sale"]
        decks = set()
        for deck_json in json["decks"]:
            decks.add(
                json_deck.JsonDeck.build_from_json(deck_json, incomplete_game_state)
            )

        cards_on_sale = set()
        for card_name in json["cards_on_sale"]:
            if not card_manager.is_card_in_manager_by_name(card_name):
                raise ValueError("card not in card manager")
            cards_on_sale.add(card_manager.get_card_by_name(card_name))

        return cls(card_manager, number_of_cards_on_sale, decks, cards_on_sale)

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_CARD_RESERVE_SCHEMA)
