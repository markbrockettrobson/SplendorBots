import unittest
import unittest.mock as mock
import copy

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.sponsor.sponsor_manager as sponsor_manager


class TestSponsorManager(unittest.TestCase):

    def setUp(self):
        self._seed = 1000
        self._number_of_sponsors = 5
        self._number_of_sponsor_options = 10

        self._sponsor_list = [
            mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True) for _ in range(self._number_of_sponsor_options)
        ]

    def test_sponsor_manager_init_valid(self):
        # Arrange
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._seed, self._number_of_sponsors, self._sponsor_list)
        # Assert
        self.assertEqual(len(test_sponsor_manager.get_sponsor_list()), self._number_of_sponsors)

    def test_sponsor_manager_init_valid_number_of_sponsors_zero(self):
        # Arrange
        self._number_of_sponsors = 0
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._seed, self._number_of_sponsors, self._sponsor_list)
        # Assert
        self.assertEqual(len(test_sponsor_manager.get_sponsor_list()), self._number_of_sponsors)

    def test_sponsor_manager_init_invalid_number_of_sponsors_negative(self):
        # Arrange
        self._number_of_sponsors = -3
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor_manager.SponsorManager(self._seed,
                                               self._number_of_sponsors,
                                               self._sponsor_list)

    def test_sponsor_manager_init_invalid_number_of_sponsors_less_sponsors(self):
        # Arrange
        self._number_of_sponsors = 11
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor_manager.SponsorManager(self._seed,
                                               self._number_of_sponsors,
                                               self._sponsor_list)

    def test_sponsor_manager_init_sponsor_list_post_init_immutability(self):
        # Arrange
        test_sponsor_manager = sponsor_manager.SponsorManager(self._seed, self._number_of_sponsors, self._sponsor_list)
        pre_mutation = copy.copy(self._sponsor_list)
        # Act
        self._sponsor_list.pop()
        # Assert
        self.assertEqual(test_sponsor_manager.get_sponsor_list(), pre_mutation)

    def test_sponsor_manager_get_sponsor_list(self):
        # Arrange
        # Act
        test_sponsor_manager = sponsor_manager.SponsorManager(self._seed, self._number_of_sponsors, self._sponsor_list)
        # Assert
        for card in test_sponsor_manager.get_sponsor_list():
            self.assertIn(card, self._sponsor_list)
        self.assertEqual(len(test_sponsor_manager.get_sponsor_list()), self._number_of_sponsors)

    def test_sponsor_manager_get_sponsor_list_immutability(self):
        # Arrange
        test_sponsor_manager = sponsor_manager.SponsorManager(self._seed, self._number_of_sponsors, self._sponsor_list)
        sponsor_list = test_sponsor_manager.get_sponsor_list()
        pre_mutation = copy.copy(sponsor_list)
        # Act
        sponsor_list.pop()
        # Assert
        self.assertEqual(test_sponsor_manager.get_sponsor_list(), pre_mutation)
