import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.sponsor.json_sponsor as json_sponsor


class TestJsonSponsor(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            'splendor_sim.src.sponsor.json_sponsor.JsonSponsor._JSON_VALIDATOR',
            autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._sponsor_patcher = mock.patch(
            'splendor_sim.src.sponsor.sponsor.Sponsor.__init__',
            autospec=True
        )
        self._mock_sponsor = self._sponsor_patcher.start()
        self.addCleanup(self._sponsor_patcher.stop)
        self._mock_coin_name_map = {}  # type: typing.Dict[i_coin_type.ICoinType, int]
        self._mock_coins = [
            mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
            for _ in range(10)
        ]

        for i, coin in enumerate(self._mock_coins):
            coin_name = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
            coin.get_name.return_value = coin_name
            self._mock_coin_name_map[coin_name] = coin

        self._mock_name = "name"
        self._mock_victory_points = 4
        self._mock_cost = {coin: 3 for coin in self._mock_coins}
        self._mock_cost_json = [
            {
                'coin_name': coin.get_name(),
                'count': 3
            }
            for coin in self._mock_coins

        ]

        self._mock_json = {
            "name": self._mock_name,
            "victory_points": self._mock_victory_points,
            "cost": self._mock_cost_json
        }

        self._mock_game_state = mock.create_autospec(spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True)
        self._mock_coin_reserve = mock.create_autospec(spec=i_coin_reserve.ICoinReserve, spec_set=True)
        self._mock_coin_type_manager = mock.create_autospec(spec=i_coin_type_manager.ICoinTypeManager, spec_set=True)

        self._mock_game_state.get_coin_reserve.return_value = self._mock_coin_reserve
        self._mock_coin_reserve.get_manager.return_value = self._mock_coin_type_manager
        self._mock_coin_type_manager.get_coin_by_name.side_effect = lambda name: self._mock_coin_name_map[name]
        self._mock_coin_type_manager.is_coin_in_manager_by_name.side_effect = \
            lambda name: name in self._mock_coin_name_map

    def test_json_sponsor_init(self):
        # Arrange
        # Act
        object_pointer = json_sponsor.JsonSponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        # Assert
        self._mock_sponsor.assert_called_once_with(
            object_pointer,
            self._mock_name,
            self._mock_victory_points,
            self._mock_cost
        )

    def test_json_sponsor_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_sponsor.JsonSponsor.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_sponsor.assert_called_once_with(
            object_pointer,
            self._mock_name,
            self._mock_victory_points,
            self._mock_cost
        )

    def test_json_sponsor_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_sponsor.JsonSponsor.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_sponsor_build_from_json_invalid_unknown_coin_name(self):
        # Arrange
        self._mock_cost_json.append(
            {
                'coin_name': "not a coin name",
                'count': 3
            }
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_sponsor.JsonSponsor.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_sponsor_build_from_json_invalid_repeated_coin_name(self):
        # Arrange
        self._mock_cost_json.append(
            {
                'coin_name': "A",
                'count': 3
            }
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_sponsor.JsonSponsor.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_sponsor_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_SPONSOR_SCHEMA,
            json_sponsor.JsonSponsor.get_json_schema()
        )

    def test_json_sponsor_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_sponsor.JsonSponsor.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_SPONSOR_SCHEMA,
            json_sponsor.JsonSponsor.get_json_schema()
        )
