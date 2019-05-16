import unittest
import unittest.mock as mock

import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.card.i_card_manager as i_card_manager
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve
import splendor_sim.src.game_state.incomplete_game_state as incomplete_game_state


class TestIncompleteGameState(unittest.TestCase):
    def setUp(self):
        self._mock_player_manager = mock.create_autospec(spec=i_player_manager.IPlayerManager, spec_set=True)
        self._mock_coin_reserve = mock.create_autospec(spec=i_coin_reserve.ICoinReserve, spec_set=True)
        self._mock_card_reserve = mock.create_autospec(spec=i_card_reserve.ICardReserve, spec_set=True)
        self._mock_card_manager = mock.create_autospec(spec=i_card_manager.ICardManager, spec_set=True)
        self._mock_sponsor_reserve = mock.create_autospec(spec=i_sponsor_reserve.ISponsorReserve, spec_set=True)

    def test_incomplete_game_state_get_player_manager(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        test_game_state.set_player_manager(self._mock_player_manager)
        # Act
        # Assert
        self.assertEqual(test_game_state.get_player_manager(), self._mock_player_manager)

    def test_incomplete_game_state_get_player_manager_no_manager(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = test_game_state.get_player_manager()

    def test_incomplete_game_state_get_coin_reserve(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        test_game_state.set_coin_reserve(self._mock_coin_reserve)
        # Act
        # Assert
        self.assertEqual(test_game_state.get_coin_reserve(), self._mock_coin_reserve)

    def test_incomplete_game_state_get_coin_reserve_no_reserve(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = test_game_state.get_coin_reserve()

    def test_incomplete_game_state_get_card_reserve(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        test_game_state.set_card_reserve(self._mock_coin_reserve)
        # Act
        # Assert
        self.assertEqual(test_game_state.get_card_reserve(), self._mock_coin_reserve)

    def test_incomplete_game_state_get_card_reserve_no_reserve(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = test_game_state.get_card_reserve()

    def test_incomplete_game_state_get_sponsor_reserve(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        test_game_state.set_sponsor_reserve(self._mock_sponsor_reserve)
        # Act
        # Assert
        self.assertEqual(test_game_state.get_sponsor_reserve(), self._mock_sponsor_reserve)

    def test_incomplete_game_state_get_sponsor_reserve_no_reserve(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = test_game_state.get_sponsor_reserve()

    def test_incomplete_game_state_get_card_manager(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        test_game_state.set_card_manager(self._mock_card_manager)
        # Act
        # Assert
        self.assertEqual(test_game_state.get_card_manager(), self._mock_card_manager)

    def test_incomplete_game_state_get_card_manager_no_reserve(self):
        # Arrange
        test_game_state = incomplete_game_state.IncompleteGameState()
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = test_game_state.get_card_manager()
