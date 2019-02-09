import unittest

from splendor_sim.collection_rules.select_multiple_same_coins_rule import SelectMultipleSameCoinsRule
# Todo test for in-valid vars


class TestSelectMultipleSameCoinsRule(unittest.TestCase):

    def setUp(self):
        self._max_number = 2
        self._required_remaining_coins = 2
        self._valid_color_ids = [0, 1, 2, 3, 4]
        self._select_multiple_same_coins_rule = SelectMultipleSameCoinsRule(self._max_number,
                                                                            self._required_remaining_coins,
                                                                            self._valid_color_ids)

    def test_str(self):
        # Arrange
        expected = 'select up to 2 coins from one of [0, 1, 2, 3, 4]'
        # Act
        real = self._select_multiple_same_coins_rule.__str__()
        # Assert
        self.assertEqual(real, expected)

    def test_get_description(self):
        # Arrange
        expected = 'select up to 2 coins from one of [0, 1, 2, 3, 4]'
        # Act
        real = self._select_multiple_same_coins_rule.get_description()
        # Assert
        self.assertEqual(real, expected)

    def test_is_valid_valid_options(self):
        # Arrange
        test_list = [([2, 0, 0, 0, 0],
                      [5, 5, 5, 5, 5],
                      "test 1st 0coin"),

                     ([0, 0, 0, 0, 2],
                      [5, 5, 5, 5, 5],
                      "test last 0coin"),

                     ([0, 0, 0, 2, 0],
                      [5, 5, 5, 5, 5, 5, 5, 5, 5],
                      "test longer current reserves"),

                     ([0, 0, 0, 0, 0],
                      [5, 5, 5, 5, 5],
                      "test select no coins"),

                     ([0, 0, 0, 2, 0],
                      [1, 5, 5, 4, 1],
                      "test select coin with minimum remaining"),

                     ([0, 0, 0, 1, 0],
                      [5, 5, 5, 5, 5],
                      "test select less than n coins")]

        for requested_coins, current_reserves, _ in test_list:
            # Act
            # Assert
            self.assertTrue(self._select_multiple_same_coins_rule.is_valid(requested_coins, current_reserves))

    def test_is_valid_non_valid_options(self):
        # Arrange
        test_list = [([3, 0, 0, 0, 0],
                      [5, 5, 5, 5, 5],
                      "test request more then n coins"),

                     ([2, 1, 0, 0, 0],
                      [5, 5, 5, 5, 5],
                      "test request more then one type of coin"),

                     ([0, 2, 0, 0, 0],
                      [0, 0, 0, 5, 5],
                      "test select un-available no coins"),

                     ([0, 2, 0, 0, 0],
                      [0, 1, 0, 5, 5],
                      "test select a coins with out minimum remaining"),

                     ([0, 0, 0, 0, 0, 2],
                      [5, 5, 5, 5, 5, 5],
                      "test select invalid color coin")]

        for requested_coins, current_reserves, _ in test_list:
            # Act
            # Assert
            self.assertFalse(self._select_multiple_same_coins_rule.is_valid(requested_coins, current_reserves))
