import unittest
import unittest.mock as mock

import splendor_sim.src.card.json_card_reserve as json_card_reserve
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.card.i_card_manager as i_card_manager
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_deck as i_deck


class TestJsonCardReserve(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            'splendor_sim.src.card.json_card_reserve.JsonCardReserve._JSON_VALIDATOR',
            autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._card_reserve_patcher = mock.patch(
            'splendor_sim.src.card.card_reserve.CardReserve.__init__',
            autospec=True
        )
        self._mock_card_reserve = self._card_reserve_patcher.start()
        self.addCleanup(self._card_reserve_patcher.stop)

        self._mock_cards_on_sale = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in range(6)]
        self._mock_cards_on_sale_set = set(self._mock_cards_on_sale)
        for i, card in enumerate(self._mock_cards_on_sale):
            card.get_name.return_value = "card name %d" % i

        self._json_card_manager_build_from_json_patcher = mock.patch(
            'splendor_sim.src.card.json_card_reserve.json_card_manager.JsonCardManager',
            autospec=True
        )
        self._mock_json_coin_type_manager_build_from_json = self._json_card_manager_build_from_json_patcher.start()
        self.addCleanup(self._json_card_manager_build_from_json_patcher.stop)
        self._mock_card_manager = mock.create_autospec(spec=i_card_manager.ICardManager, spec_set=True)
        self._mock_json_coin_type_manager_build_from_json.build_from_json.return_value = self._mock_card_manager
        self._mock_card_manager.is_card_in_manager_by_name.return_value = True
        self._mock_card_manager.get_card_by_name.side_effect = self._mock_cards_on_sale

        self._json_deck_build_from_json_patcher = mock.patch(
            'splendor_sim.src.card.json_card_reserve.json_deck.JsonDeck',
            autospec=True
        )
        self._mock_json_deck_build_from_json = self._json_deck_build_from_json_patcher.start()
        self.addCleanup(self._json_deck_build_from_json_patcher.stop)
        self._mock_decks = [mock.create_autospec(spec=i_deck.IDeck, spec_set=True) for _ in range(3)]
        self._mock_decks_set = set(self._mock_decks)
        self._mock_json_deck_build_from_json.build_from_json.side_effect = self._mock_decks

        self._mock_number_of_cards_on_sale = 2

        self._mock_json = {
            "card_manager": {"mock": "json"},
            "number_of_cards_on_sale": self._mock_number_of_cards_on_sale,
            "decks": [
                {"mock": "deck 1 json"},
                {"mock": "deck 2 json"},
                {"mock": "deck 3 json"},
            ],
            "cards_on_sale": [
                card.get_name() for card in self._mock_cards_on_sale
            ]
        }

        self._mock_game_state = mock.create_autospec(spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True)

    def test_json_card_reserve_init(self):
        # Arrange
        # Act
        object_pointer = json_card_reserve.JsonCardReserve(
            self._mock_card_manager,
            self._mock_number_of_cards_on_sale,
            self._mock_decks_set,
            self._mock_cards_on_sale_set
        )
        # Assert
        self._mock_card_reserve.assert_called_once_with(
            object_pointer,
            self._mock_card_manager,
            self._mock_number_of_cards_on_sale,
            self._mock_decks_set,
            self._mock_cards_on_sale_set
        )

    def test_json_card_reserve_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_card_reserve.JsonCardReserve.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_card_reserve.assert_called_once_with(
            object_pointer,
            self._mock_card_manager,
            self._mock_number_of_cards_on_sale,
            self._mock_decks_set,
            self._mock_cards_on_sale_set
        )

    def test_json_card_reserve_type_build_from_json_invalid_json(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_card_reserve.JsonCardReserve.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_card_reserve_type_build_from_json_invalid_card_not_in_manager(self):
        # Arrange
        self._mock_card_manager.is_card_in_manager_by_name.side_effect = [True, False, True]
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_card_reserve.JsonCardReserve.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_card_reserve_type_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_CARD_RESERVE_SCHEMA,
            json_card_reserve.JsonCardReserve.get_json_schema()
        )

    def test_json_card_reserve_type_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_card_reserve.JsonCardReserve.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_CARD_RESERVE_SCHEMA,
            json_card_reserve.JsonCardReserve.get_json_schema()
        )
