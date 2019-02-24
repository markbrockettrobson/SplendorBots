import unittest
import unittest.mock as mock
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.coin.coin_type_manager as coin_type_manager


class TestCoinTypeManager(unittest.TestCase):

    def setUp(self):
        self._mock_coin_type_list = [mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(6)]
        self._mock_coin_equivalents = [(self._mock_coin_type_list[i],
                                        self._mock_coin_type_list[5])
                                       for i in range(5)]

    def test_coin_type_manager_test_get_coin_list(self):
        # Arrange
        test_coin_type_manager = coin_type_manager.CoinTypeManager(self._mock_coin_type_list, [])
        # Act
        result = test_coin_type_manager.get_coin_list()
        # Assert
        for coin in self._mock_coin_type_list:
            self.assertIn(coin, result)

    def test_coin_type_manager_test_get_equivalent_coins(self):
        # Arrange
        test_coin_type_manager = coin_type_manager.CoinTypeManager(self._mock_coin_type_list,
                                                                   self._mock_coin_equivalents)
        # Act
        result = test_coin_type_manager.get_equivalent_coins(self._mock_coin_type_list[0])
        # Assert
        self.assertIn(self._mock_coin_type_list[0], result)
        self.assertIn(self._mock_coin_type_list[5], result)

    def test_coin_type_manager_test_get_equivalent_coins_single_entry(self):
        # Arrange
        test_coin_type_manager = coin_type_manager.CoinTypeManager(self._mock_coin_type_list,
                                                                   self._mock_coin_equivalents)
        # Act
        result = test_coin_type_manager.get_equivalent_coins(self._mock_coin_type_list[5])
        # Assert
        self.assertEqual([self._mock_coin_type_list[5]], result)

    def test_coin_type_manager_test_get_coin_usage(self):
        # Arrange
        test_coin_type_manager = coin_type_manager.CoinTypeManager(self._mock_coin_type_list,
                                                                   self._mock_coin_equivalents)
        # Act
        result = test_coin_type_manager.get_coin_usage(self._mock_coin_type_list[5])
        # Assert
        for coin in self._mock_coin_type_list:
            self.assertIn(coin, result)

    def test_coin_type_manager_test_get_coin_usage_single_entry(self):
        # Arrange
        test_coin_type_manager = coin_type_manager.CoinTypeManager(self._mock_coin_type_list,
                                                                   self._mock_coin_equivalents)
        # Act
        result = test_coin_type_manager.get_coin_usage(self._mock_coin_type_list[0])
        # Assert
        self.assertEqual([self._mock_coin_type_list[0]], result)
