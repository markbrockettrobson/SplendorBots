import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.card.json_card as json_card
import splendor_sim.src.factories.json_schemas as json_schemas


class TestJsonCard(unittest.TestCase):
    def _set_up_coin(self):
        self._mock_coin_list = [
            mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
            for _ in range(3)
        ]
        self._mock_coin_name_map = {
            name: self._mock_coin_list[i] for i, name in enumerate("ABC")
        }

        self._mock_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True
        )
        self._mock_coin_reserve = mock.create_autospec(
            spec=i_coin_reserve.ICoinReserve, spec_set=True
        )
        self._mock_coin_type_manager = mock.create_autospec(
            spec=i_coin_type_manager.ICoinTypeManager, spec_set=True
        )

        self._mock_game_state.get_coin_reserve.return_value = self._mock_coin_reserve
        self._mock_coin_reserve.get_manager.return_value = self._mock_coin_type_manager
        self._mock_coin_type_manager.get_coin_by_name.side_effect = lambda name: self._mock_coin_name_map[
            name
        ]
        self._mock_coin_type_manager.is_coin_in_manager_by_name.side_effect = (
            lambda name: name in self._mock_coin_name_map
        )

    def _make_mock_json(self):
        self._mock_cost_dict = [
            {"coin_name": "B", "count": 1},
            {"coin_name": "C", "count": 1},
        ]

        self._mock_json = {
            "name": self._mock_name,
            "tier": self._mock_tier,
            "victory_points": self._mock_victory_points,
            "discounted_coin_type_name": "A",
            "cost": self._mock_cost_dict,
        }

    def setUp(self):
        self._validator_patcher = mock.patch(
            "splendor_sim.src.card.json_card.JsonCard._JSON_VALIDATOR", autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._card_patcher = mock.patch(
            "splendor_sim.src.card.card.Card.__init__", autospec=True
        )
        self._mock_card = self._card_patcher.start()
        self.addCleanup(self._card_patcher.stop)

        self._mock_name = "name"
        self._mock_total_number = 10
        self._mock_json = {
            "name": self._mock_name,
            "total_number": self._mock_total_number,
        }

        self._set_up_coin()

        self._mock_tier = 1
        self._mock_victory_points = 2
        self._mock_card_name = "card_name"
        self._mock_discount = self._mock_coin_list[0]
        self._mock_cost = {self._mock_coin_list[1]: 1, self._mock_coin_list[2]: 1}

        self._make_mock_json()

    def test_json_card_init(self):
        # Arrange
        # Act
        object_pointer = json_card.JsonCard(
            self._mock_tier,
            self._mock_victory_points,
            self._mock_discount,
            self._mock_cost,
            self._mock_name,
        )
        # Assert
        self._mock_card.assert_called_once_with(
            object_pointer,
            self._mock_tier,
            self._mock_victory_points,
            self._mock_discount,
            self._mock_cost,
            self._mock_name,
        )

    def test_json_card_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_card.JsonCard.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_card.assert_called_once_with(
            object_pointer,
            self._mock_tier,
            self._mock_victory_points,
            self._mock_discount,
            self._mock_cost,
            self._mock_name,
        )

    def test_json_card_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_card.JsonCard.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_card_build_from_json_coin_reserve_none(self):
        # Arrange
        self._mock_game_state.get_coin_reserve.return_value = None
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_card.JsonCard.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_card_build_from_json_discount_unknown(self):
        # Arrange
        self._mock_json["discounted_coin_type_name"] = "Z"
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_card.JsonCard.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_card_build_from_json_coin_cost_unknown(self):
        # Arrange
        self._mock_cost_dict.append({"coin_name": "Z", "count": 1})
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_card.JsonCard.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_card_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_CARD_SCHEMA, json_card.JsonCard.get_json_schema()
        )

    def test_json_card_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_card.JsonCard.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_CARD_SCHEMA, json_card.JsonCard.get_json_schema()
        )
