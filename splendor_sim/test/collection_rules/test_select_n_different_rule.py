import unittest

from splendor_sim.collection_rules.select_n_different_rule import SelectNDifferentRule
# Todo test for in-valid vars


class TestSelectNDifferentRule(unittest.TestCase):

    def setUp(self):
        self._max_number = 3
        self._valid_color_ids = [0, 1, 2, 3, 4]
        self._select_n_different_rule = SelectNDifferentRule(self._max_number, self._valid_color_ids)

    def test_str(self):
        # Arrange
        expected = 'select up to 3 different coins from [0, 1, 2, 3, 4]'
        # Act
        real = self._select_n_different_rule.__str__()
        # Assert
        self.assertEqual(real, expected)

    def test_get_description(self):
        # Arrange
        expected = 'select up to 3 different coins from [0, 1, 2, 3, 4]'
        # Act
        real = self._select_n_different_rule.get_description()
        # Assert
        self.assertEqual(real, expected)

    def test_is_valid_valid_options(self):
        # Arrange
        test_list = [([1, 0, 1, 0, 1],
                      [5, 5, 5, 5, 5],
                      "test 1st and last coin"),

                     ([1, 1, 0, 1, 0],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5],
                      "test longer current reserves"),

                     ([0, 0, 0, 0, 0],
                      [5, 5, 5, 5, 5],
                      "test select no coins"),

                     ([1, 0, 0, 1, 1],
                      [1, 5, 5, 2, 1],
                      "test select last coin"),

                     ([1, 0, 0, 1, 0],
                      [5, 5, 5, 5, 5],
                      "test select less than n coins")]

        for requested_coins, current_reserves, _ in test_list:
            # Act
            # Assert
            self.assertTrue(self._select_n_different_rule.is_valid(requested_coins, current_reserves))

    def test_is_valid_non_valid_options(self):
        # Arrange
        test_list = [([1, 1, 1, 0, 1],
                      [5, 5, 5, 5, 5],
                      "test request more then n coins"),

                     ([2, 1, 0, 0, 0],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5],
                      "test request more then one of a type of coin"),

                     ([0, 1, 0, 1, 1],
                      [0, 0, 0, 5, 5],
                      "test select un-available no coins"),

                     ([0, 0, 0, 1, 1, 1],
                      [5, 5, 5, 5, 5, 5],
                      "test select invalid color coin")]

        for requested_coins, current_reserves, _ in test_list:

            # Act
            # Assert
            self.assertFalse(self._select_n_different_rule.is_valid(requested_coins, current_reserves))
