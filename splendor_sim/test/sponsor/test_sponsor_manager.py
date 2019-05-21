import unittest
import unittest.mock as mock
import copy

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.src.sponsor.sponsor_manager as sponsor_manager
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.factories.json_schemas as json_schemas


class TestSponsorManager(unittest.TestCase):
    def setUp(self):
        self._number_of_sponsors = 5

        self._mock_sponsor_set = {
            mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True) for _ in range(self._number_of_sponsors)
        }
        for i, sponsor in enumerate(self._mock_sponsor_set):
            sponsor.get_name.return_value = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
            sponsor.to_json.return_value = {"Mock Json": sponsor.get_name()}

    def test_sponsor_manager_init_valid(self):
        # Arrange
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Assert
        self.assertEqual(len(test_sponsor_manager.get_sponsor_set()), self._number_of_sponsors)

    def test_sponsor_manager_init_invalid_repeated_name(self):
        # Arrange
        list(self._mock_sponsor_set)[0].get_name.return_value = "common_name"
        list(self._mock_sponsor_set)[1].get_name.return_value = "common_name"
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor_manager.SponsorManager(self._mock_sponsor_set)

    def test_sponsor_manager_init_sponsor_list_post_init_immutability(self):
        # Arrange
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Act
        for _ in range(len(self._mock_sponsor_set)):
            self._mock_sponsor_set.pop()
        # Assert
        self.assertEqual(len(test_sponsor_manager.get_sponsor_set()), self._number_of_sponsors)

    def test_sponsor_manager_get_sponsor_set(self):
        # Arrange
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Assert
        for card in test_sponsor_manager.get_sponsor_set():
            self.assertIn(card, self._mock_sponsor_set)
        self.assertEqual(len(test_sponsor_manager.get_sponsor_set()), self._number_of_sponsors)

    def test_sponsor_manager_get_sponsor_list_immutability(self):
        # Arrange
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        sponsor_list = test_sponsor_manager.get_sponsor_set()
        pre_mutation = copy.copy(sponsor_list)
        # Act
        sponsor_list.pop()
        # Assert
        self.assertEqual(test_sponsor_manager.get_sponsor_set(), pre_mutation)

    def test_sponsor_manager_is_sponsor_in_manager_by_name_true(self):
        # Arrange
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Assert
        self.assertTrue(test_sponsor_manager.is_sponsor_in_manager_by_name("A"))

    def test_sponsor_manager_is_sponsor_in_manager_by_name_false(self):
        # Arrange
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Assert
        self.assertFalse(test_sponsor_manager.is_sponsor_in_manager_by_name("A Name not in manager"), False)

    def test_sponsor_manager_get_sponsor_by_name_true(self):
        # Arrange
        test_sponsor = list(self._mock_sponsor_set)[0]
        test_sponsor.get_name.return_value = "test_name"
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Assert
        self.assertEqual(test_sponsor_manager.get_sponsor_by_name("test_name"), test_sponsor)

    def test_sponsor_manager_get_sponsor_by_name_false(self):
        # Arrange
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Assert
        # Assert
        with self.assertRaises(ValueError):
            _ = test_sponsor_manager.get_sponsor_by_name("test_name")

    def test_sponsor_manager_to_json(self):
        # Arrange
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Act
        # Assert
        expected = {
            "sponsors": [sponsor.to_json() for sponsor in self._mock_sponsor_set],
        }
        real = test_sponsor_manager.to_json()
        self.assertCountEqual(real['sponsors'], expected['sponsors'])

    def test_sponsor_manager_to_json_complies_with_schema(self):
        # Arrange
        test_json_validator = json_validator.JsonValidator(json_schemas.JSON_SPONSOR_MANAGER_SCHEMA)
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._mock_sponsor_set)
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(test_sponsor_manager.to_json())
        )
