import unittest
import unittest.mock as mock
import copy

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.sponsor.sponsor_reserve as sponsor_reserve


class TestSponsorReserve(unittest.TestCase):

    def setUp(self):
        self._number_of_sponsors = 5

        self._sponsor_list = [
            mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True) for _ in range(self._number_of_sponsors)
        ]

    def test_sponsor_reserve_init_valid(self):
        # Arrange
        self._sponsor_list = []
        # Act
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(self._sponsor_list)
        # Assert
        self.assertEqual(test_sponsor_reserve.get_remaining_sponsor_list(), self._sponsor_list)

    def test_sponsor_reserve_sponsor_list_post_init_immutability(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(self._sponsor_list)
        pre_mutation = copy.copy(self._sponsor_list)
        # Act
        self._sponsor_list.pop()
        # Assert
        self.assertEqual(set(test_sponsor_reserve.get_remaining_sponsor_list()), set(pre_mutation))

    def test_sponsor_reserve_get_remaining_sponsor_list(self):
        # Arrange
        # Act
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(self._sponsor_list)
        # Assert
        self.assertEqual(set(test_sponsor_reserve.get_remaining_sponsor_list()), set(self._sponsor_list))

    def test_sponsor_reserve_get_remaining_sponsor_list_empty(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(self._sponsor_list)
        for sponsor in self._sponsor_list:
            test_sponsor_reserve.remove_sponsor(sponsor)
        # Act
        # Assert
        self.assertEqual(test_sponsor_reserve.get_remaining_sponsor_list(), [])

    def test_sponsor_reserve_get_remaining_sponsor_list_immutability(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(self._sponsor_list)
        return_value = test_sponsor_reserve.get_remaining_sponsor_list()
        pre_mutation = copy.copy(return_value)
        # Act
        return_value.pop()
        # Assert
        self.assertEqual(test_sponsor_reserve.get_remaining_sponsor_list(), pre_mutation)

    def test_sponsor_reserve_remove_sponsor(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(self._sponsor_list)
        # Act
        for i, sponsor in enumerate(self._sponsor_list):
            test_sponsor_reserve.remove_sponsor(sponsor)
            # Assert
            self.assertEqual(len(test_sponsor_reserve.get_remaining_sponsor_list()), self._number_of_sponsors - i - 1)

    def remove_sponsor_not_in_reserve(self):
        # Arrange
        test_sponsor_reserve = sponsor_reserve.SponsorReserve(self._sponsor_list)
        new_sponsor = mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True)
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_sponsor_reserve.remove_sponsor(new_sponsor)
