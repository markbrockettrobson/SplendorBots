import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.coin.json_coin_type as json_coin_type
import splendor_sim.src.factories.json_schemas as json_schemas


class TestJsonCoinType(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            "splendor_sim.src.coin.json_coin_type.JsonCoinType._JSON_VALIDATOR",
            autospec=True,
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._coin_type_patcher = mock.patch(
            "splendor_sim.src.coin.coin_type.CoinType.__init__", autospec=True
        )
        self._mock_coin_type = self._coin_type_patcher.start()
        self.addCleanup(self._coin_type_patcher.stop)

        self._mock_name = "name"
        self._mock_total_number = 10
        self._mock_json = {
            "name": self._mock_name,
            "total_number": self._mock_total_number,
        }

        self._mock_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True
        )

    def test_json_coin_type_init(self):
        # Arrange
        # Act
        object_pointer = json_coin_type.JsonCoinType(
            self._mock_name, self._mock_total_number
        )
        # Assert
        self._mock_coin_type.assert_called_once_with(
            object_pointer, self._mock_name, self._mock_total_number
        )

    def test_json_coin_type_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_coin_type.JsonCoinType.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_coin_type.assert_called_once_with(
            object_pointer, self._mock_name, self._mock_total_number
        )

    def test_json_coin_type_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_coin_type.JsonCoinType.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_coin_type_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_COIN_TYPE_SCHEMA,
            json_coin_type.JsonCoinType.get_json_schema(),
        )

    def test_json_coin_type_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_coin_type.JsonCoinType.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_COIN_TYPE_SCHEMA,
            json_coin_type.JsonCoinType.get_json_schema(),
        )
