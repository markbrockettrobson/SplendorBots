import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.player.json_player as json_player


class TestJsonPlayerCoinInventory(unittest.TestCase):

    def set_up_validator(self):
        self._validator_patcher = mock.patch(
            'splendor_sim.src.player.json_player.JsonPlayer._JSON_VALIDATOR',
            autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

    def set_up_player_sponsor_inventory(self):
        self._json_player_sponsor_inventory_patcher = mock.patch(
            'splendor_sim.src.player.json_player.json_player_sponsor_inventory.JsonPlayerSponsorInventory',
            autospec=True
        )
        self._mock_player_sponsor_inventory_init = self._json_player_sponsor_inventory_patcher.start()
        self.addCleanup(self._json_player_sponsor_inventory_patcher.stop)
        self._mock_player_sponsor_inventory = mock.create_autospec(
            spec=i_player_sponsor_inventory.IPlayerSponsorInventory,
            spec_set=True
        )
        self._mock_player_sponsor_inventory_init.build_from_json.return_value = self._mock_player_sponsor_inventory

    def set_up_player_card_inventory(self):
        self._json_player_card_inventory_patcher = mock.patch(
            'splendor_sim.src.player.json_player.json_player_card_inventory.JsonPlayerCardInventory',
            autospec=True
        )
        self._mock_player_card_inventory_init = self._json_player_card_inventory_patcher.start()
        self.addCleanup(self._json_player_card_inventory_patcher.stop)
        self._mock_player_card_inventory = mock.create_autospec(
            spec=i_player_card_inventory.IPlayerCardInventory,
            spec_set=True
        )
        self._mock_player_card_inventory_init.build_from_json.return_value = self._mock_player_card_inventory

    def set_up_player_coin_inventory(self):
        self._json_player_coin_inventory_patcher = mock.patch(
            'splendor_sim.src.player.json_player.json_player_coin_inventory.JsonPlayerCoinInventory',
            autospec=True
        )
        self._mock_json_player_coin_inventory_init = self._json_player_coin_inventory_patcher.start()
        self.addCleanup(self._json_player_coin_inventory_patcher.stop)
        self._mock_player_coin_inventory = mock.create_autospec(
            spec=i_player_coin_inventory.IPlayerCoinInventory,
            spec_set=True
        )
        self._mock_json_player_coin_inventory_init.build_from_json.return_value = self._mock_player_coin_inventory

    def setUp(self):

        self._player_patcher = mock.patch(
            'splendor_sim.src.player.json_player.player.Player.__init__',
            autospec=True
        )
        self._mock_player = self._player_patcher.start()
        self.addCleanup(self._player_patcher.stop)

        self.set_up_validator()
        self.set_up_player_sponsor_inventory()
        self.set_up_player_card_inventory()
        self.set_up_player_coin_inventory()

        self._mock_name = 'mock name'

        self._mock_json = {
            'name': self._mock_name,
            'coin_inventory': {'mock json': 'coin_inventory'},
            'card_inventory': {'mock json': 'card_inventory'},
            'sponsor_inventory': {'mock json': 'sponsor_inventory'}
        }

        self._mock_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState,
            spec_set=True
        )

    def test_json_player_init(self):
        # Arrange
        # Act
        object_pointer = json_player.JsonPlayer(
            self._mock_name,
            self._mock_player_coin_inventory,
            self._mock_player_card_inventory,
            self._mock_player_sponsor_inventory
        )
        # Assert
        self._mock_player.assert_called_once_with(
            object_pointer,
            self._mock_name,
            self._mock_player_coin_inventory,
            self._mock_player_card_inventory,
            self._mock_player_sponsor_inventory
        )

    def test_json_player_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_player.JsonPlayer.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_player.assert_called_once_with(
            object_pointer,
            self._mock_name,
            self._mock_player_coin_inventory,
            self._mock_player_card_inventory,
            self._mock_player_sponsor_inventory
        )
        self._mock_player_sponsor_inventory_init.build_from_json.assert_called_once_with(
            {'mock json': 'sponsor_inventory'},
            self._mock_game_state
        )
        self._mock_player_card_inventory_init.build_from_json.assert_called_once_with(
            {'mock json': 'card_inventory'},
            self._mock_game_state
        )
        self._mock_json_player_coin_inventory_init.build_from_json.assert_called_once_with(
            {'mock json': 'coin_inventory'},
            self._mock_game_state
        )

    def test_json_player_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player.JsonPlayer.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_player_sponsor_inventory_get_json_schema(self):
        # Arrange
        object_pointer = json_player.JsonPlayer.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Act
        # Assert
        self.assertEqual(object_pointer.get_json_schema(), json_schemas.JSON_PLAYER)

    def test_json_player_sponsor_inventory_get_json_schema_immutability(self):
        # Arrange
        object_pointer = json_player.JsonPlayer.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Act
        object_pointer.get_json_schema().pop(list(object_pointer.get_json_schema())[0])
        # Assert
        self.assertEqual(object_pointer.get_json_schema(), json_schemas.JSON_PLAYER)
