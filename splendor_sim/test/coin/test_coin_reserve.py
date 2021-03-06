import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.src.coin.coin_reserve as coin_reserve
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator


class TestCoinReserve(unittest.TestCase):
    def setUp(self):
        self._mock_coin_type_manager = mock.create_autospec(
            spec=i_coin_type_manager.ICoinTypeManager, spec_set=True
        )
        self._mock_coin_type_list = [
            mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
            for _ in range(6)
        ]
        self._mock_coin_type_manager.get_coin_set.return_value = set(
            self._mock_coin_type_list
        )
        self._mock_coin_type_manager.to_json.return_value = {
            "coin type manager json": "json"
        }
        for i, _mock_coin_type in enumerate(self._mock_coin_type_list):
            _mock_coin_type.get_total_number.return_value = 7
            _mock_coin_type.get_name.return_value = "%d" % i
        self._mock_coin_type_list[-1].get_total_number.return_value = 5

        self._return_dictionary = {coin: 7 for coin in self._mock_coin_type_list}
        self._return_dictionary[self._mock_coin_type_list[-1]] = 5

        self.test_coin_reserve = coin_reserve.CoinReserve(self._mock_coin_type_manager)

    def test_coin_reserve_init_coin_stocks(self):
        # Arrange
        self._return_dictionary[self._mock_coin_type_list[0]] = 2
        self._return_dictionary[self._mock_coin_type_list[1]] = 3
        expected = self._return_dictionary

        coin_stocks = {self._mock_coin_type_list[0]: 2, self._mock_coin_type_list[1]: 3}
        # Act
        self.test_coin_reserve = coin_reserve.CoinReserve(
            self._mock_coin_type_manager, coin_stocks
        )
        real = self.test_coin_reserve.get_coins_remaining()
        # Assert
        self.assertEqual(real, expected)

    def test_coin_reserve_init_coin_stocks_invalid_coin_type(self):
        # Arrange
        coin_stocks = {
            mock.create_autospec(
                spec=i_coin_type_manager.ICoinTypeManager, spec_set=True
            ): 5
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_coin_reserve = coin_reserve.CoinReserve(
                self._mock_coin_type_manager, coin_stocks
            )

    def test_coin_reserve_init_coin_stocks_invalid_coin_number_above_max(self):
        # Arrange
        coin_stocks = {self._mock_coin_type_list[0]: 50}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_coin_reserve = coin_reserve.CoinReserve(
                self._mock_coin_type_manager, coin_stocks
            )

    def test_coin_reserve_get_manager(self):
        # Arrange
        expected = self._mock_coin_type_manager
        # Act
        real = self.test_coin_reserve.get_manager()
        # Assert
        self.assertEqual(real, expected)

    def test_coin_reserve_get_coins_maximum(self):
        # Arrange
        expected = self._return_dictionary
        # Act
        real = self.test_coin_reserve.get_coins_maximum()
        # Assert
        self.assertEqual(real, expected)

    def test_coin_reserve_get_coins_remaining(self):
        # Arrange
        expected = self._return_dictionary
        # Act
        real = self.test_coin_reserve.get_coins_remaining()
        # Assert
        self.assertEqual(real, expected)

    def test_coin_reserve_has_minimum_true(self):
        # Arrange
        minimum = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 5,
        }

        # Act
        real = self.test_coin_reserve.has_minimum(minimum)
        # Assert
        self.assertTrue(real)

    def test_coin_reserve_has_minimum_false(self):
        # Arrange
        minimum = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[2]: 8,
            self._mock_coin_type_list[-1]: 5,
        }
        # Act
        real = self.test_coin_reserve.has_minimum(minimum)
        # Assert
        self.assertFalse(real)

    def test_coin_reserve_has_minimum_type_error_new_coin_type(self):
        # Arrange
        new_mock_coin = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        minimum = {new_mock_coin: 0}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = self.test_coin_reserve.has_minimum(minimum)

    def test_coin_reserve_add_coins(self):
        # Arrange
        remove = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 3,
            self._mock_coin_type_list[-1]: 3,
        }
        add = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[-1]: 1,
        }
        expected = self._return_dictionary
        expected[self._mock_coin_type_list[2]] -= 1
        expected[self._mock_coin_type_list[-1]] -= 2
        self.test_coin_reserve.remove_coins(remove)
        # Act
        self.test_coin_reserve.add_coins(add)
        real = self.test_coin_reserve.get_coins_remaining()
        # Assert
        self.assertEqual(real, expected)

    def test_coin_reserve_add_coins_above_max(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[-1]: 1,
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_coin_reserve.add_coins(add)

    def test_coin_reserve_add_coins_type_error_new_coin_type(self):
        # Arrange
        new_mock_coin = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        add = {new_mock_coin: 0}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_coin_reserve.add_coins(add)

    def test_coin_reserve_remove_coins(self):
        # Arrange
        remove = {
            self._mock_coin_type_list[0]: 7,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 3,
        }
        expected = self._return_dictionary
        expected[self._mock_coin_type_list[0]] -= 7
        expected[self._mock_coin_type_list[2]] -= 4
        expected[self._mock_coin_type_list[-1]] -= 3
        # Act
        self.test_coin_reserve.remove_coins(remove)
        real = self.test_coin_reserve.get_coins_remaining()
        # Assert
        self.assertEqual(real, expected)

    def test_coin_reserve_remove_coins_bellow_zero(self):
        # Arrange
        remove = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 7,
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_coin_reserve.remove_coins(remove)

    def test_coin_reserve_remove_coins_type_error_new_coin_type(self):
        # Arrange
        new_mock_coin = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        remove = {new_mock_coin: 0}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_coin_reserve.remove_coins(remove)

    def test_coin_reserve_get_coins_maximum_immutability(self):
        # Arrange
        pre_mutation = self.test_coin_reserve.get_coins_maximum()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertNotEqual(pre_mutation, self.test_coin_reserve.get_coins_maximum())

    def test_coin_reserve_get_coins_remaining_immutability(self):
        # Arrange
        pre_mutation = self.test_coin_reserve.get_coins_remaining()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertNotEqual(pre_mutation, self.test_coin_reserve.get_coins_remaining())

    def test_coin_reserve_to_json(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            {
                "coin_type_manager": {"coin type manager json": "json"},
                "coin_stocks": [],
            },
            self.test_coin_reserve.to_json(),
        )

    def test_coin_reserve_to_json_non_full(self):
        # Arrange
        coin_stocks = [{"coin_name": "0", "count": 2}]
        self.test_coin_reserve.remove_coins({self._mock_coin_type_list[0]: 5})
        # Act
        # Assert
        self.assertEqual(
            {
                "coin_type_manager": {"coin type manager json": "json"},
                "coin_stocks": coin_stocks,
            },
            self.test_coin_reserve.to_json(),
        )

    def test_coin_reserve_to_json_complies_with_schema(self):
        # Arrange
        test_json_validator = json_validator.JsonValidator(
            json_schemas.JSON_COIN_RESERVE_SCHEMA
        )
        # Act
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(self.test_coin_reserve.to_json())
        )
