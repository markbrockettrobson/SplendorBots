import unittest

import splendor_sim.src.coin.coin_type as coin_type
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator


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

    def test_coin_type_to_json(self):
        # Arrange
        # Act
        test_coin_type = coin_type.CoinType(self._name, self._total_number)
        # Assert
        self.assertEqual(
            test_coin_type.to_json(), {"name": "emerald", "total_number": 7}
        )

    def test_coin_type_to_json_complies_with_schema(self):
        # Arrange
        test_json_validator = json_validator.JsonValidator(
            json_schemas.JSON_COIN_TYPE_SCHEMA
        )
        # Act
        test_coin_type = coin_type.CoinType(self._name, self._total_number)
        # Assert
        self.assertTrue(test_json_validator.validate_json(test_coin_type.to_json()))
