import copy
import unittest
import unittest.mock as mock

import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.player_manager as player_manager


class TestPlayerManager(unittest.TestCase):
    def setUp(self):
        self._number_of_players = 4
        self._mock_player_list = [
            mock.create_autospec(spec=i_player.IPlayer, spec_set=True)
            for _ in range(self._number_of_players)
        ]
        for index, player in enumerate(self._mock_player_list):
            player.get_name.return_value = "%d" % index
            player.to_json.return_value = {"mock json": "%d" % index}

    def test_player_manager_init_valid(self):
        # Arrange
        # Act
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Assert
        self.assertEqual(test_player_manager.get_player_list(), self._mock_player_list)

    def test_player_manager_init_invalid_current_player_not_in_player_list(self):
        # Arrange
        new_mock_player = mock.create_autospec(spec=i_player.IPlayer, spec_set=True)
        new_mock_player.get_name.return_value = "not in set"
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = player_manager.PlayerManager(self._mock_player_list, new_mock_player, 1)

    def test_player_manager_init_invalid_duplicate_player_name(self):
        # Arrange
        self._mock_player_list[-1].get_name.return_value = self._mock_player_list[
            0
        ].get_name()
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = player_manager.PlayerManager(
                self._mock_player_list, self._mock_player_list[0], 1
            )

    def test_player_manager_init_invalid_turn_number(self):
        # Arrange
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = player_manager.PlayerManager(
                self._mock_player_list, self._mock_player_list[0], -200
            )

        with self.assertRaises(ValueError):
            _ = player_manager.PlayerManager(
                self._mock_player_list, self._mock_player_list[0], -1
            )

        with self.assertRaises(ValueError):
            _ = player_manager.PlayerManager(
                self._mock_player_list, self._mock_player_list[0], 0
            )

    def test_player_manager_init_player_list_immutability(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        pre_mutation = copy.copy(self._mock_player_list)
        self._mock_player_list.pop()
        # Assert
        self.assertEqual(test_player_manager.get_player_list(), pre_mutation)

    def test_player_manager_get_player_list(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        # Assert
        self.assertEqual(test_player_manager.get_player_list(), self._mock_player_list)

    def test_player_manager_get_player_list_immutability(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        return_value = test_player_manager.get_player_list()
        pre_mutation = copy.copy(return_value)
        return_value.pop()
        # Assert
        self.assertEqual(test_player_manager.get_player_list(), pre_mutation)

    def test_player_manager_get_player_set(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        # Assert
        self.assertEqual(
            test_player_manager.get_player_set(), set(self._mock_player_list)
        )

    def test_player_manager_get_player_set_immutability(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        return_value = test_player_manager.get_player_set()
        pre_mutation = copy.copy(return_value)
        return_value.pop()
        # Assert
        self.assertEqual(test_player_manager.get_player_set(), pre_mutation)

    def test_player_manager_get_current_player(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        # Assert
        self.assertIn(
            test_player_manager.get_current_player(), set(self._mock_player_list)
        )

    def test_player_manager_get_current_player_multiple_calls(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        last_call = test_player_manager.get_current_player()
        # Assert
        self.assertEqual(test_player_manager.get_current_player(), last_call)

    def test_player_manager_next_players_turn(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        last_call = test_player_manager.get_current_player()
        # Assert
        self.assertNotEqual(test_player_manager.next_players_turn(), last_call)

    def test_player_manager_next_players_turn_rap_around(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        player_list = []
        for _ in range(self._number_of_players * 2):
            player_list.append(test_player_manager.next_players_turn())
        # Assert
        for player in player_list:
            self.assertEqual(test_player_manager.next_players_turn(), player)

    def test_player_manager_get_turn_number(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[0], 1
        )
        # Act
        for i in range(1, 20):
            for _ in range(self._number_of_players):
                test_player_manager.next_players_turn()
            # Assert
            self.assertEqual(test_player_manager.get_turn_number(), i + 1)

    def test_player_manager_to_json(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[1], 1
        )
        # Act
        # Assert
        self.assertEqual(
            {
                "players": [
                    {"mock json": "%d" % index}
                    for index in range(self._number_of_players)
                ],
                "current_player": self._mock_player_list[1].get_name(),
                "turn_number": 1,
            },
            test_player_manager.to_json(),
        )

    def test_player_manager_to_json_complies_with_schema(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(
            self._mock_player_list, self._mock_player_list[1], 1
        )
        test_json_validator = json_validator.JsonValidator(
            json_schemas.JSON_PLAYER_MANAGER
        )
        # Act
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(test_player_manager.to_json())
        )
