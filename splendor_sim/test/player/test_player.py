import unittest
import unittest.mock as mock

import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.player as player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self._mock_name = 'mock_name'
        self._mock_coin_inventory = \
            mock.create_autospec(spec=i_player_coin_inventory.IPlayerCoinInventory, spec_set=True)
        self._mock_card_inventory = \
            mock.create_autospec(spec=i_player_card_inventory.IPlayerCardInventory, spec_set=True)
        self._mock_sponsor_inventory = \
            mock.create_autospec(spec=i_player_sponsor_inventory.IPlayerSponsorInventory, spec_set=True)

        self._mock_coin_inventory.to_json.return_value = {'mock coin inventory': 'json'}
        self._mock_card_inventory.to_json.return_value = {'mock card inventory': 'json'}
        self._mock_sponsor_inventory.to_json.return_value = {'mock sponsor inventory': 'json'}

    def test_player_init(self):
        # Arrange
        # Act
        test_player = player.Player(
            self._mock_name,
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        # Assert
        self.assertEqual(test_player.get_name(), self._mock_name)
        self.assertEqual(test_player.get_coin_inventory(), self._mock_coin_inventory)
        self.assertEqual(test_player.get_card_inventory(), self._mock_card_inventory)
        self.assertEqual(test_player.get_sponsor_inventory(), self._mock_sponsor_inventory)

    def test_player_get_name(self):
        # Arrange
        test_player = player.Player(
            self._mock_name,
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        # Act
        # Assert
        self.assertEqual(test_player.get_name(), self._mock_name)

    def test_player_get_coin_inventory(self):
        # Arrange
        test_player = player.Player(
            self._mock_name,
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        # Act
        # Assert
        self.assertEqual(test_player.get_coin_inventory(), self._mock_coin_inventory)

    def test_player_get_card_inventory(self):
        # Arrange
        test_player = player.Player(
            self._mock_name,
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        # Act
        # Assert
        self.assertEqual(test_player.get_card_inventory(), self._mock_card_inventory)

    def test_player_get_sponsor_inventory(self):
        # Arrange
        test_player = player.Player(
            self._mock_name,
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        # Act
        # Assert
        self.assertEqual(test_player.get_sponsor_inventory(), self._mock_sponsor_inventory)

    def test_player_to_json(self):
        # Arrange
        test_player = player.Player(
            self._mock_name,
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        # Act
        # Assert
        self.assertEqual(
            test_player.to_json(),
            {
                'name': 'mock_name',
                'coin_inventory': {'mock coin inventory': 'json'},
                'card_inventory': {'mock card inventory': 'json'},
                'sponsor_inventory': {'mock sponsor inventory': 'json'}
            }
        )

    def test_player_to_json_complies_with_schema(self):
        # Arrange
        test_player = player.Player(
            self._mock_name,
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        test_json_validator = json_validator.JsonValidator(json_schemas.JSON_PLAYER)
        # Act
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(test_player.to_json())
        )
