import unittest
import unittest.mock as mock

import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.player.json_player_card_inventory as json_player_card_inventory
import splendor_sim.interfaces.card.i_card_manager as i_card_manager
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state


class TestJsonPlayerCoinInventory(unittest.TestCase):

    def set_up_validator(self):
        self._validator_patcher = mock.patch(
            'splendor_sim.src.player.json_player_card_inventory.JsonPlayerCardInventory._JSON_VALIDATOR',
            autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

    def set_up_cards(self):
        self._mock_cards = [mock.create_autospec(spec=i_card.ICard, specset=True) for _ in range(6)]
        self._mock_card_sets = set(self._mock_cards)

        for i, card in enumerate(self._mock_cards):
            card.get_name.return_value = "name_%d" % i

        self._card_name_map = {card.get_name(): card for card in self._mock_cards}

    def set_up_player_card_inventory(self):
        self._player_card_inventory_patcher = mock.patch(
            'splendor_sim.src.player.json_player_card_inventory.player_card_inventory.PlayerCardInventory.__init__',
            autospec=True
        )
        self._mock_player_card_inventory_init = self._player_card_inventory_patcher.start()
        self.addCleanup(self._player_card_inventory_patcher.stop)

    def setUp(self):
        self.set_up_validator()
        self.set_up_cards()
        self.set_up_player_card_inventory()

        self._mock_json = {
            'max_reserved_cards': 4,
            'reserved_cards': [card.get_name() for card in self._mock_cards[:2]],
            'cards': [card.get_name() for card in self._mock_cards[2:]]
        }

        self._mock_game_state = mock.create_autospec(spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True)
        self._mock_card_manager = mock.create_autospec(spec=i_card_manager.ICardManager, spec_set=True)

        self._mock_game_state.get_card_manager.return_value = self._mock_card_manager
        self._mock_card_manager.get_card_by_name.side_effect = lambda name: self._card_name_map[name]
        self._mock_card_manager.is_card_in_manager_by_name.side_effect = \
            lambda name: name in self._card_name_map

    def test_json_player_card_inventory_init(self):
        # Arrange
        # Act
        object_pointer = json_player_card_inventory.JsonPlayerCardInventory(
            4,
            set(self._mock_cards[:2]),
            set(self._mock_cards[2:])
        )
        # Assert
        self._mock_player_card_inventory_init.assert_called_once_with(
            object_pointer,
            4,
            set(self._mock_cards[:2]),
            set(self._mock_cards[2:])
        )

    def test_json_player_card_inventory_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_player_card_inventory.JsonPlayerCardInventory.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_player_card_inventory_init.assert_called_once_with(
            object_pointer,
            4,
            set(self._mock_cards[:2]),
            set(self._mock_cards[2:])
        )

    def test_json_player_card_inventory_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_card_inventory.JsonPlayerCardInventory.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_player_card_inventory_build_from_json_invalid_card_name_not_in_manager(self):
        # Arrange
        self._mock_json['cards'].append("not a name in the manager")
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_card_inventory.JsonPlayerCardInventory.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_player_card_inventory_build_from_json_invalid_reserved_card_name_not_in_manager(self):
        # Arrange
        self._mock_json['reserved_cards'].append("not a name in the manager")
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_card_inventory.JsonPlayerCardInventory.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_player_card_inventory_get_json_schema(self):
        # Arrange
        object_pointer = json_player_card_inventory.JsonPlayerCardInventory.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Act
        # Assert
        self.assertEqual(object_pointer.get_json_schema(), json_schemas.JSON_PLAYER_CARD_INVENTORY)

    def test_json_player_card_inventory_get_json_schema_immutability(self):
        # Arrange
        object_pointer = json_player_card_inventory.JsonPlayerCardInventory.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Act
        object_pointer.get_json_schema().pop(list(object_pointer.get_json_schema())[0])
        # Assert
        self.assertEqual(object_pointer.get_json_schema(), json_schemas.JSON_PLAYER_CARD_INVENTORY)
