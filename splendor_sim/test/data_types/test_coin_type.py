import unittest
import splendor_sim.data_types.coin_type as coin_type


class TestCoinType(unittest.TestCase):

    def setUp(self):
        self._name = "emerald"
        self._total_number = 7

    def test_coin_type_init_valid_arguments(self):
        # Arrange
        # Act
        test_coin_type = coin_type.CoinType(self._name, self._total_number)
        # Assert
        self.assertEqual(test_coin_type.get_name(), self._name)
        self.assertEqual(test_coin_type.get_total_number(), self._total_number)

    def test_coin_type_init_invalid_argument_total_number_zero(self):
        # Arrange
        self._total_number = 0
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = coin_type.CoinType(self._name, self._total_number)

    def test_coin_type_init_invalid_argument_total_number_negative(self):
        # Arrange
        self._total_number = -1
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = coin_type.CoinType(self._name, self._total_number)
