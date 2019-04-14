import unittest
import unittest.mock as mock

import splendor_sim.src.coin.json_buildable_coin_type as json_buildable_coin_type


class TestJsonBuildableCoinType(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            'splendor_sim.src.coin.json_buildable_coin_type.JsonBuildableCoinType._JSON_VALIDATOR',
            autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._coin_type_patcher = mock.patch(
            'splendor_sim.src.coin.coin_type.CoinType.__init__',
            autospec=True
        )
        self._mock_coin_type = self._coin_type_patcher.start()
        self.addCleanup(self._coin_type_patcher.stop)

        self._mock_name = "name"
        self._mock_total_number = 10
        self._mock_json = {
            "name": self._mock_name,
            "total_number": self._mock_total_number
        }

    def test_json_buildable_coin_type_init(self):
        # Arrange
        # Act
        object_pointer = json_buildable_coin_type.JsonBuildableCoinType(self._mock_name, self._mock_total_number)
        # Assert
        self._mock_coin_type.assert_called_once_with(object_pointer, self._mock_name, self._mock_total_number)

    def test_json_buildable_coin_type_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_buildable_coin_type.JsonBuildableCoinType.build_from_json(
            self._mock_json
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_coin_type.assert_called_once_with(object_pointer, self._mock_name, self._mock_total_number)

    def test_json_buildable_coin_type_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_buildable_coin_type.JsonBuildableCoinType.build_from_json(
                self._mock_json
            )

    def test_json_buildable_coin_type_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            {
                'name': {
                    'type': 'string'
                },
                'total_number': {
                    'type': 'integer'
                }
            },
            json_buildable_coin_type.JsonBuildableCoinType.get_json_schema()
        )

    def test_json_buildable_coin_type_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_buildable_coin_type.JsonBuildableCoinType.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            {
                'name': {
                    'type': 'string'
                },
                'total_number': {
                    'type': 'integer'
                }
            },
            json_buildable_coin_type.JsonBuildableCoinType.get_json_schema()
        )
