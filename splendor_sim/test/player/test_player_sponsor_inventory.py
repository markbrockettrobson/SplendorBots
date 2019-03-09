import copy
import unittest
import unittest.mock as mock

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.src.player.player_sponsor_inventory as player_sponsor_inventory


class TestPlayerSponsorInventory(unittest.TestCase):

    def setUp(self):
        self._mock_sponsors = [mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True) for _ in range(10)]
        for sponsor in self._mock_sponsors:
            sponsor.get_victory_points.return_value = 2

    def test_player_sponsor_inventory_init(self):
        # Arrange
        # Act
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory()
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_total_victory_points(), 0)
        self.assertEqual(test_player_sponsor_inventory.get_sponsor_list(), [])

    def test_player_sponsor_inventory_get_sponsor_list_empty(self):
        # Arrange
        # Act
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory()
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_sponsor_list(), [])

    def test_player_sponsor_inventory_get_sponsor_list(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory()
        # Act
        for sponsor in self._mock_sponsors:
            test_player_sponsor_inventory.add_sponsor(sponsor)
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_sponsor_list(), list(set(self._mock_sponsors)))

    def test_player_sponsor_inventory_get_sponsor_list_immutability(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory()
        for sponsor in self._mock_sponsors:
            test_player_sponsor_inventory.add_sponsor(sponsor)
        return_value = test_player_sponsor_inventory.get_sponsor_list()
        premutaion = copy.copy(return_value)
        # Act
        return_value.pop()
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_sponsor_list(), premutaion)

    def test_player_sponsor_inventory_add_sponsor(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory()
        # Act
        for i, sponsor in enumerate(self._mock_sponsors):
            test_player_sponsor_inventory.add_sponsor(sponsor)
            # Assert
            self.assertEqual(test_player_sponsor_inventory.get_total_victory_points(), (i+1) * 2)
        self.assertEqual(test_player_sponsor_inventory.get_sponsor_list(), list(set(self._mock_sponsors)))

    def test_player_sponsor_inventory_add_sponsor_sponsor_in_inventory(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory()
        test_player_sponsor_inventory.add_sponsor(self._mock_sponsors[0])
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_player_sponsor_inventory.add_sponsor(self._mock_sponsors[0])

    def test_player_sponsor_inventory_get_total_victory_points(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory()
        # Act
        for i, sponsor in enumerate(self._mock_sponsors):
            test_player_sponsor_inventory.add_sponsor(sponsor)
            # Assert
            self.assertEqual(test_player_sponsor_inventory.get_total_victory_points(), (i + 1) * 2)

    def test_player_sponsor_inventory_get_total_victory_points_empty(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory()
        # Act
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_total_victory_points(), 0)
