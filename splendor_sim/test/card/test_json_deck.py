import unittest
import unittest.mock as mock

import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_card_manager as i_card_manager
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.card.json_deck as json_deck
import splendor_sim.src.factories.json_schemas as json_schemas


class TestJsonDeck(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            'splendor_sim.src.card.json_deck.JsonDeck._JSON_VALIDATOR',
            autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._deck_patcher = mock.patch(
            'splendor_sim.src.card.deck.Deck.__init__',
            autospec=True
        )
        self._mock_deck = self._deck_patcher.start()
        self.addCleanup(self._deck_patcher.stop)

        self._mock_cards = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in range(10)]
        for i, card in enumerate(self._mock_cards):
            card.get_name.return_value = "card %d" % i

        self._name_to_card_dict = {"card %d" % i: card for i, card in enumerate(self._mock_cards)}

        self._mock_card_set = set(self._mock_cards)

        self._mock_tier = 1
        self._mock_json = {
            'tier': self._mock_tier,
            'cards': [
                card.get_name() for card in self._mock_cards
            ]
        }

        self._mock_game_state = mock.create_autospec(spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True)
        self._mock_card_manager = mock.create_autospec(spec=i_card_manager.ICardManager, spec_set=True)

        self._mock_game_state.get_card_manager.return_value = self._mock_card_manager
        self._mock_card_manager.get_card_by_name.side_effect = lambda name: self._name_to_card_dict[name]
        self._mock_card_manager.is_card_in_manager_by_name.return_value = True

    def test_json_deck_init(self):
        # Arrange
        # Act
        object_pointer = json_deck.JsonDeck(
            self._mock_tier,
            self._mock_cards
        )
        # Assert
        self._mock_deck.assert_called_once_with(
            object_pointer,
            self._mock_tier,
            self._mock_cards
        )

    def test_json_deck_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_deck.JsonDeck.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_deck.assert_called_once_with(
            object_pointer,
            self._mock_tier,
            self._mock_cards
        )

    def test_json_deck_type_build_from_json_invalid_json(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_deck.JsonDeck.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_deck_type_build_from_json_invalid_card_not_in_manager(self):
        # Arrange
        self._mock_card_manager.is_card_in_manager_by_name.side_effect = [True, False, True]
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_deck.JsonDeck.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_deck_type_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_DECK_SCHEMA,
            json_deck.JsonDeck.get_json_schema()
        )

    def test_json_deck_type_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_deck.JsonDeck.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_DECK_SCHEMA,
            json_deck.JsonDeck.get_json_schema()
        )
