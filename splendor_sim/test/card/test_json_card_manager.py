import unittest
import unittest.mock as mock

import splendor_sim.src.card.json_card_manager as json_card_manager
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.card.i_card as i_card


class TestJsonCardManager(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            'splendor_sim.src.card.json_card_manager.JsonCardManager._JSON_VALIDATOR',
            autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._card_manager_patcher = mock.patch(
            'splendor_sim.src.card.card_manager.CardManager.__init__',
            autospec=True
        )
        self._mock_card_manager = self._card_manager_patcher.start()
        self.addCleanup(self._card_manager_patcher.stop)

        self._json_card_patcher = mock.patch(
            'splendor_sim.src.card.json_card.JsonCard',
            autospec=True
        )
        self._mock_json_card = self._json_card_patcher.start()
        self.addCleanup(self._json_card_patcher.stop)

        self._mock_cards = [mock.create_autospec(spec=i_card.ICard, spec_set=True)]
        for i, card in enumerate(self._mock_cards):
            card.get_name.return_value = "card %d" % i

        self._mock_card_set = set(self._mock_cards)
        self._mock_json_card.build_from_json.side_effect = self._mock_cards

        self._mock_json = {
            'cards': [
                {'mock_card_json': card.get_name()} for card in self._mock_cards
            ]
        }

        self._mock_game_state = mock.create_autospec(spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True)

    def test_json_card_manager_init(self):
        # Arrange
        # Act
        object_pointer = json_card_manager.JsonCardManager(
            self._mock_card_set
        )
        # Assert
        self._mock_card_manager.assert_called_once_with(
            object_pointer,
            self._mock_card_set
        )

    def test_json_card_manager_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_card_manager.JsonCardManager.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_card_manager.assert_called_once_with(
            object_pointer,
            self._mock_card_set
        )

    def test_json_card_manager_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_card_manager.JsonCardManager.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_card_manager_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_CARD_MANAGER_SCHEMA,
            json_card_manager.JsonCardManager.get_json_schema()
        )

    def test_json_card_manager_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_card_manager.JsonCardManager.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_CARD_MANAGER_SCHEMA,
            json_card_manager.JsonCardManager.get_json_schema()
        )
