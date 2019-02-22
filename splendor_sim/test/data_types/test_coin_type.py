import unittest
import unittest.mock as mock
import splendor_sim.data_types.coin_type as coin_type


# todo type checking


class TestCoinReserve(unittest.TestCase):

    def setUp(self):
        self._patcher_isinstance = mock.patch('splendor_sim.data_types.coin_type.isinstance')
        self._mock_isinstance = self._patcher_isinstance.start()
        self._mock_isinstance.return_value = True
        self.addCleanup(self._patcher_isinstance.stop)

        self._name = "emerald"
        self._total_number = 7

    def test_coin_type_init_valid_arguments(self):
        # Arrange
        # Act
        test_coin_type = coin_type.CoinType(self._name, self._total_number)
        # Assert
        self.assertEqual(test_coin_type.get_name(), self._name)
        self.assertEqual(test_coin_type.get_total_number(), self._total_number)

    def test_coin_type_init_invalid_argument_name_non_str(self):
        # Arrange
        self._mock_isinstance.side_effect = [False, True]
        self._name = 2
        # Act
        # Assert
        with self.assertRaises(AssertionError):
            _ = coin_type.CoinType(self._name, self._total_number)

    def test_coin_type_init_invalid_argument_total_number_non_int(self):
        # Arrange
        self._mock_isinstance.side_effect = [True, False]
        self._total_number = 5.1
        # Act
        # Assert
        with self.assertRaises(AssertionError):
            _ = coin_type.CoinType(self._name, self._total_number)

    def test_coin_type_init_invalid_argument_total_number_zero(self):
        # Arrange
        self._total_number = 0
        # Act
        # Assert
        with self.assertRaises(AssertionError):
            _ = coin_type.CoinType(self._name, self._total_number)

    def test_coin_type_init_invalid_argument_total_number_negative(self):
        # Arrange
        self._total_number = -1
        # Act
        # Assert
        with self.assertRaises(AssertionError):
            _ = coin_type.CoinType(self._name, self._total_number)
