import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.player.json_player_manager as json_player_manager


class TestJsonPlayerCoinInventory(unittest.TestCase):
    def set_up_validator(self):
        self._validator_patcher = mock.patch(
            "splendor_sim.src.player.json_player_manager.JsonPlayerManager._JSON_VALIDATOR",
            autospec=True,
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

    def set_up_json_player(self):
        self._json_player_patcher = mock.patch(
            "splendor_sim.src.player.json_player_manager.json_player.JsonPlayer",
            autospec=True,
        )
        self._mock_player_init = self._json_player_patcher.start()
        self.addCleanup(self._json_player_patcher.stop)
        self._mock_player_sponsor_inventory = mock.create_autospec(
            spec=i_player_sponsor_inventory.IPlayerSponsorInventory, spec_set=True
        )

        self._mock_players = [
            mock.create_autospec(spec=i_player.IPlayer, spec_set=True) for _ in range(3)
        ]
        self._mock_player_json_map = {
            index: player for index, player in enumerate(self._mock_players)
        }
        for index, player in enumerate(self._mock_players):
            player.get_name.return_value = "%d" % index
        self._mock_player_init.build_from_json.side_effect = lambda x, _: self._mock_player_json_map[
            x["mock_json"]
        ]

    def setUp(self):
        self._player_manager_patcher = mock.patch(
            "splendor_sim.src.player.json_player_manager.player_manager.PlayerManager.__init__",
            autospec=True,
        )
        self._mock_player_manager = self._player_manager_patcher.start()
        self.addCleanup(self._player_manager_patcher.stop)

        self.set_up_validator()
        self.set_up_json_player()

        self._mock_turn_number = 2

        self._mock_json = {
            "players": [
                {"mock_json": index} for index, player in enumerate(self._mock_players)
            ],
            "current_player": self._mock_players[0].get_name(),
            "turn_number": self._mock_turn_number,
        }

        self._mock_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True
        )

    def test_json_player_init(self):
        # Arrange
        # Act
        object_pointer = json_player_manager.JsonPlayerManager(
            self._mock_players, self._mock_players[0], self._mock_turn_number
        )
        # Assert
        self._mock_player_manager.assert_called_once_with(
            object_pointer,
            self._mock_players,
            self._mock_players[0],
            self._mock_turn_number,
        )

    def test_json_player_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_player_manager.JsonPlayerManager.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_player_manager.assert_called_once_with(
            object_pointer,
            self._mock_players,
            self._mock_players[0],
            self._mock_turn_number,
        )
        calls = [
            mock.call({"mock_json": index}, self._mock_game_state)
            for index in range(len(self._mock_players))
        ]
        self._mock_player_init.build_from_json.assert_has_calls(calls)

    def test_json_player_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_manager.JsonPlayerManager.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_player_build_from_json_invalid_current_player_unknown(self):
        # Arrange
        self._mock_json["current_player"] = "new unknown name"
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_manager.JsonPlayerManager.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_player_sponsor_inventory_get_json_schema(self):
        # Arrange
        object_pointer = json_player_manager.JsonPlayerManager.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Act
        # Assert
        self.assertEqual(
            object_pointer.get_json_schema(), json_schemas.JSON_PLAYER_MANAGER
        )

    def test_json_player_sponsor_inventory_get_json_schema_immutability(self):
        # Arrange
        object_pointer = json_player_manager.JsonPlayerManager.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Act
        object_pointer.get_json_schema().pop(list(object_pointer.get_json_schema())[0])
        # Assert
        self.assertEqual(
            object_pointer.get_json_schema(), json_schemas.JSON_PLAYER_MANAGER
        )
