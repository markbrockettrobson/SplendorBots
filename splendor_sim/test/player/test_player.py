import unittest
import unittest.mock as mock
import splendor_sim.src.player.player as player
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self._mock_coin_inventory = \
            mock.create_autospec(spec=i_player_coin_inventory.IPlayerCoinInventory, spec_set=True)
        self._mock_card_inventory = \
            mock.create_autospec(spec=i_player_card_inventory.IPlayerCardInventory, spec_set=True)
        self._mock_sponsor_inventory = \
            mock.create_autospec(spec=i_player_sponsor_inventory.IPlayerSponsorInventory, spec_set=True)

    def test_player_init(self):
        # Arrange
        # Act
        test_player = player.Player(
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        # Assert
        self.assertEqual(test_player.get_coin_inventory(), self._mock_coin_inventory)
        self.assertEqual(test_player.get_card_inventory(), self._mock_card_inventory)
        self.assertEqual(test_player.get_sponsor_inventory(), self._mock_sponsor_inventory)

    def test_player_get_coin_inventory(self):
        # Arrange
        test_player = player.Player(
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
            self._mock_coin_inventory,
            self._mock_card_inventory,
            self._mock_sponsor_inventory
        )
        # Act
        # Assert
        self.assertEqual(test_player.get_sponsor_inventory(), self._mock_sponsor_inventory)
