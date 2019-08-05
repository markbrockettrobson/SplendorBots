import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.coin.json_coin_type_manager as json_coin_type_manager
import splendor_sim.src.factories.json_schemas as json_schemas


class TestJsonCoinTypeManager(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            "splendor_sim.src.coin.json_coin_type_manager.JsonCoinTypeManager._JSON_VALIDATOR",
            autospec=True,
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._coin_type_manager_patcher = mock.patch(
            "splendor_sim.src.coin.coin_type_manager.CoinTypeManager.__init__",
            autospec=True,
        )
        self._mock_coin_type_manager = self._coin_type_manager_patcher.start()
        self.addCleanup(self._coin_type_manager_patcher.stop)

        self._mock_coin_types = [
            mock.create_autospec(spec=i_coin_type.ICoinType, specset=True)
            for _ in range(6)
        ]
        self._mock_coin_type_set = set(self._mock_coin_types)

        for i, coin in enumerate(self._mock_coin_types):
            coin.get_name.return_value = "name_%d" % i

        self._mock_coin_equivalents = {
            (self._mock_coin_types[5], self._mock_coin_types[0]),
            (self._mock_coin_types[5], self._mock_coin_types[1]),
            (self._mock_coin_types[5], self._mock_coin_types[2]),
            (self._mock_coin_types[5], self._mock_coin_types[3]),
            (self._mock_coin_types[5], self._mock_coin_types[4]),
        }

        self._mock_json = {
            "coin_types": [
                {"name": "name_0", "total_number": 10},
                {"name": "name_1", "total_number": 10},
                {"name": "name_2", "total_number": 10},
                {"name": "name_3", "total_number": 10},
                {"name": "name_4", "total_number": 10},
                {"name": "name_5", "total_number": 4},
            ],
            "coin_equivalents": [
                {"coin_name": "name_5", "equivalent_coins_name": "name_0"},
                {"coin_name": "name_5", "equivalent_coins_name": "name_1"},
                {"coin_name": "name_5", "equivalent_coins_name": "name_2"},
                {"coin_name": "name_5", "equivalent_coins_name": "name_3"},
                {"coin_name": "name_5", "equivalent_coins_name": "name_4"},
            ],
        }

        self._json_coin_patcher = mock.patch(
            "splendor_sim.src.coin.json_coin_type.JsonCoinType", autospec=True
        )
        self._mock_json_coin_type = self._json_coin_patcher.start()
        self.addCleanup(self._json_coin_patcher.stop)
        self._mock_json_coin_type.build_from_json.side_effect = self._mock_coin_types

        self._mock_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True
        )

    def test_json_coin_type_manager_init(self):
        # Arrange
        # Act
        object_pointer = json_coin_type_manager.JsonCoinTypeManager(
            self._mock_coin_type_set, self._mock_coin_equivalents
        )
        # Assert
        self._mock_coin_type_manager.assert_called_once_with(
            object_pointer, self._mock_coin_type_set, self._mock_coin_equivalents
        )

    def test_json_coin_type_manager_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_coin_type_manager.JsonCoinTypeManager.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_coin_type_manager.assert_called_once_with(
            object_pointer, self._mock_coin_type_set, self._mock_coin_equivalents
        )

    def test_json_coin_type_manager_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_coin_type_manager.JsonCoinTypeManager.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_coin_type_manager_build_from_json_invalid_un_known_equivalent_coin_name(
        self
    ):
        # Arrange
        self._mock_json["coin_equivalents"].append(
            {"coin_name": "name_unknown", "equivalent_coins_name": "name_4"}
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_coin_type_manager.JsonCoinTypeManager.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_coin_type_manager_build_from_json_invalid_un_known_equivalent_equivalent_coins_name(
        self
    ):
        # Arrange
        self._mock_json["coin_equivalents"].append(
            {"coin_name": "name_0", "equivalent_coins_name": "name_unknown"}
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_coin_type_manager.JsonCoinTypeManager.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_coin_type_manager_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_COIN_TYPE_MANAGER_SCHEMA,
            json_coin_type_manager.JsonCoinTypeManager.get_json_schema(),
        )

    def test_json_coin_type_manager_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_coin_type_manager.JsonCoinTypeManager.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_COIN_TYPE_MANAGER_SCHEMA,
            json_coin_type_manager.JsonCoinTypeManager.get_json_schema(),
        )
