import copy
import unittest
import unittest.mock as mock

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.player_sponsor_inventory as player_sponsor_inventory


class TestPlayerSponsorInventory(unittest.TestCase):
    def setUp(self):
        self._mock_sponsors = [
            mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True)
            for _ in range(10)
        ]
        self._mock_sponsor_set = set(self._mock_sponsors)
        for index, sponsor in enumerate(self._mock_sponsors):
            sponsor.get_victory_points.return_value = 2
            sponsor.get_name.return_value = "%d" % index

    def test_player_sponsor_inventory_init(self):
        # Arrange
        # Act
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_total_victory_points(), 0)
        self.assertEqual(test_player_sponsor_inventory.get_sponsor_set(), set())

    def test_player_sponsor_inventory_init_started_sponsor(self):
        # Arrange
        # Act
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            self._mock_sponsor_set
        )
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_total_victory_points(), 20)
        self.assertEqual(
            test_player_sponsor_inventory.get_sponsor_set(), self._mock_sponsor_set
        )

    def test_player_sponsor_inventory_get_sponsor_list_empty(self):
        # Arrange
        # Act
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_sponsor_set(), set())

    def test_player_sponsor_inventory_get_sponsor_list(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        # Act
        for sponsor in self._mock_sponsors:
            test_player_sponsor_inventory.add_sponsor(sponsor)
        # Assert
        self.assertEqual(
            test_player_sponsor_inventory.get_sponsor_set(), self._mock_sponsor_set
        )

    def test_player_sponsor_inventory_get_sponsor_list_immutability(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        for sponsor in self._mock_sponsors:
            test_player_sponsor_inventory.add_sponsor(sponsor)
        return_value = test_player_sponsor_inventory.get_sponsor_set()
        premutaion = copy.copy(return_value)
        # Act
        return_value.pop()
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_sponsor_set(), premutaion)

    def test_player_sponsor_inventory_add_sponsor(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        # Act
        for i, sponsor in enumerate(self._mock_sponsors):
            test_player_sponsor_inventory.add_sponsor(sponsor)
            # Assert
            self.assertEqual(
                test_player_sponsor_inventory.get_total_victory_points(), (i + 1) * 2
            )
        self.assertEqual(
            test_player_sponsor_inventory.get_sponsor_set(), self._mock_sponsor_set
        )

    def test_player_sponsor_inventory_add_sponsor_sponsor_in_inventory(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        test_player_sponsor_inventory.add_sponsor(self._mock_sponsors[0])
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_player_sponsor_inventory.add_sponsor(self._mock_sponsors[0])

    def test_player_sponsor_inventory_get_total_victory_points(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        # Act
        for i, sponsor in enumerate(self._mock_sponsors):
            test_player_sponsor_inventory.add_sponsor(sponsor)
            # Assert
            self.assertEqual(
                test_player_sponsor_inventory.get_total_victory_points(), (i + 1) * 2
            )

    def test_player_sponsor_inventory_get_total_victory_points_empty(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        # Act
        # Assert
        self.assertEqual(test_player_sponsor_inventory.get_total_victory_points(), 0)

    def test_player_sponsor_inventory_to_json(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            set()
        )
        # Act
        # Assert
        self.assertEqual({"sponsors": []}, test_player_sponsor_inventory.to_json())

    def test_player_sponsor_inventory_to_json_non_empty(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            {self._mock_sponsors[1]}
        )
        # Act
        # Assert
        self.assertEqual(
            {"sponsors": [self._mock_sponsors[1].get_name()]},
            test_player_sponsor_inventory.to_json(),
        )

    def test_player_sponsor_inventory_to_json_complies_with_schema(self):
        # Arrange
        test_player_sponsor_inventory = player_sponsor_inventory.PlayerSponsorInventory(
            self._mock_sponsor_set
        )
        test_json_validator = json_validator.JsonValidator(
            json_schemas.JSON_PLAYER_SPONSOR_INVENTORY
        )
        # Act
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(test_player_sponsor_inventory.to_json())
        )
