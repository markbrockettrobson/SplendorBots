import copy
import unittest
import unittest.mock as mock

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_manager as i_sponsor_manager
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.sponsor.sponsor_reserve as sponsor_reserve


class TestSponsorReserve(unittest.TestCase):
    def setUp(self):
        self._number_of_sponsors = 5

        self._mock_sponsor_set = {
            mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True)
            for _ in range(self._number_of_sponsors)
        }
        for i, sponsor in enumerate(self._mock_sponsor_set):
            sponsor.get_name.return_value = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]

        self._mock_sponsor_manager = mock.create_autospec(
            spec=i_sponsor_manager.ISponsorManager, spec_set=True
        )
        self._mock_sponsor_manager.get_sponsor_set.return_value = self._mock_sponsor_set
        self._mock_sponsor_manager.to_json.return_value = {"mock": "json"}

    def test_sponsor_reserve_init_valid(self):
        # Arrange
        self._mock_sponsor_set = set()
        # Act
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        # Assert
        self.assertEqual(
            test_sponsor_reserve.get_remaining_sponsor_set(), self._mock_sponsor_set
        )

    def test_sponsor_reserve_init_invalid_sponsor_not_in_manager(self):
        # Arrange
        self._mock_sponsor_manager.get_sponsor_set.return_value = set()
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor_reserve.SponsorReserve(
                self._mock_sponsor_manager, self._mock_sponsor_set
            )

    def test_sponsor_reserve_sponsor_set_post_init_immutability(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        pre_mutation = copy.copy(self._mock_sponsor_set)
        # Act
        self._mock_sponsor_set.pop()
        # Assert
        self.assertEqual(
            set(test_sponsor_reserve.get_remaining_sponsor_set()), set(pre_mutation)
        )

    def test_sponsor_reserve_get_sponsor_set(self):
        # Arrange
        # Act
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        # Assert
        self.assertEqual(
            test_sponsor_reserve.get_sponsor_manager(), self._mock_sponsor_manager
        )

    def test_sponsor_reserve_get_remaining_sponsor_set(self):
        # Arrange
        # Act
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        # Assert
        self.assertEqual(
            set(test_sponsor_reserve.get_remaining_sponsor_set()),
            set(self._mock_sponsor_set),
        )

    def test_sponsor_reserve_get_remaining_sponsor_set_empty(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        for sponsor in self._mock_sponsor_set:
            test_sponsor_reserve.remove_sponsor(sponsor)
        # Act
        # Assert
        self.assertEqual(test_sponsor_reserve.get_remaining_sponsor_set(), set())

    def test_sponsor_reserve_get_remaining_sponsor_set_immutability(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        return_value = test_sponsor_reserve.get_remaining_sponsor_set()
        pre_mutation = copy.copy(return_value)
        # Act
        return_value.pop()
        # Assert
        self.assertEqual(test_sponsor_reserve.get_remaining_sponsor_set(), pre_mutation)

    def test_sponsor_reserve_remove_sponsor(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        # Act
        for i, sponsor in enumerate(self._mock_sponsor_set):
            test_sponsor_reserve.remove_sponsor(sponsor)
            # Assert
            self.assertEqual(
                len(test_sponsor_reserve.get_remaining_sponsor_set()),
                self._number_of_sponsors - i - 1,
            )

    def test_sponsor_reserve_remove_sponsor_not_in_reserve(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        new_sponsor = mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True)
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_sponsor_reserve.remove_sponsor(new_sponsor)

    def test_sponsor_reserve_to_json(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        # Act
        # Assert
        expected = {
            "sponsor_manager": self._mock_sponsor_manager.to_json(),
            "sponsors": [sponsor.get_name() for sponsor in self._mock_sponsor_set],
        }
        real = test_sponsor_reserve.to_json()
        self.assertEqual(real["sponsor_manager"], expected["sponsor_manager"])
        self.assertCountEqual(real["sponsors"], expected["sponsors"])

    def test_sponsor_reserve_to_json_complies_with_schema(self):
        # Arrange
        test_json_validator = json_validator.JsonValidator(
            json_schemas.JSON_SPONSOR_RESERVE_SCHEMA
        )
        # Act
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(
            self._mock_sponsor_manager, self._mock_sponsor_set
        )
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(test_sponsor_reserve.to_json())
        )
