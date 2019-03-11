import copy
import unittest
import unittest.mock as mock

import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.src.player.player_manager as player_manager


class TestPlayerManager(unittest.TestCase):

    def setUp(self):
        self._number_of_players = 4
        self._mock_player_set = \
            {
                mock.create_autospec(spec=i_player.IPlayer, spec_set=True)
                for _ in range(self._number_of_players)
            }

    def test_player_manager_init_valid(self):
        # Arrange
        # Act
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Assert
        self.assertEqual(test_player_manager.get_player_set(), self._mock_player_set)
        pass

    def test_player_manager_init_player_set_immutability(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Act
        pre_mutation = copy.copy(self._mock_player_set)
        self._mock_player_set.pop()
        # Assert
        self.assertEqual(test_player_manager.get_player_set(), pre_mutation)

    def test_player_manager_get_player_set(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Act
        # Assert
        self.assertEqual(test_player_manager.get_player_set(), self._mock_player_set)

    def test_player_manager_get_player_set_immutability(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Act
        return_value = test_player_manager.get_player_set()
        pre_mutation = copy.copy(return_value)
        return_value.pop()
        # Assert
        self.assertEqual(test_player_manager.get_player_set(), pre_mutation)

    def test_player_manager_get_current_player(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Act
        # Assert
        self.assertIn(test_player_manager.get_current_player(), self._mock_player_set)

    def test_player_manager_get_current_player_multiple_calls(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Act
        last_call = test_player_manager.get_current_player()
        # Assert
        self.assertEqual(test_player_manager.get_current_player(), last_call)

    def test_player_manager_next_players_turn(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Act
        last_call = test_player_manager.get_current_player()
        # Assert
        self.assertNotEqual(test_player_manager.next_players_turn(), last_call)

    def test_player_manager_next_players_turn_rap_around(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Act
        player_list = []
        for _ in range(self._number_of_players * 2):
            player_list.append(test_player_manager.next_players_turn())
        # Assert
        for player in player_list:
            self.assertEqual(test_player_manager.next_players_turn(), player)

    def test_player_manager_get_turn_number(self):
        # Arrange
        test_player_manager = player_manager.PlayerManager(self._mock_player_set)
        # Act
        for i in range(1, 20):
            for _ in range(self._number_of_players):
                test_player_manager.next_players_turn()
            # Assert
            self.assertEqual(test_player_manager.get_turn_number(), i + 1)
