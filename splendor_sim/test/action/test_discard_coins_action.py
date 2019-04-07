import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.src.action.discard_coins_action as discard_coins_action


class TestDiscardCoinsAction(unittest.TestCase):

    def setUp(self):
        self._mock_coin_type_list = [mock.create_autospec(spec=i_coin_type, spec_set=True) for _ in range(6)]
        self._mock_valid_coin_type_set = set(self._mock_coin_type_list)

        self._mock_player = mock.create_autospec(spec=i_player.IPlayer, spec_set=True)
        self._mock_coin_inventory = mock.create_autospec(
            spec=i_player_coin_inventory.IPlayerCoinInventory,
            spec_set=True
        )
        self._mock_coin_inventory.get_number_of_coins.return_value = 12
        self._mock_coin_inventory.has_minimum.return_value = True
        self._mock_player.get_coin_inventory.return_value = self._mock_coin_inventory
        self._mock_coins = {self._mock_coin_type_list[0]: 2}

        self._mock_game_state = mock.create_autospec(spec=i_game_state.IGameState, spec_set=True)
        self._mock_coin_reserve = mock.create_autospec(spec=i_coin_reserve.ICoinReserve, spec_set=True)
        self._mock_game_state.get_coin_reserve.return_value = self._mock_coin_reserve

    def test_discard_coins_action_init_valid(self):
        # Arrange
        # Act
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Assert
        self.assertEqual(
            test_action.validate(self._mock_game_state),
            True
        )

    def test_discard_coins_action_post_init_coin_type_set_immutability(self):
        # Arrange
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Act
        self._mock_coins.pop(list(self._mock_coins.keys())[0])
        # Assert
        self.assertTrue(test_action.validate(self._mock_game_state))

    def test_discard_coins_action_post_init_coins_immutability(self):
        # Arrange
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        self._mock_valid_coin_type_set = {self._mock_coin_type_list[1]}
        # Act
        self._mock_valid_coin_type_set.pop()
        # Assert
        self.assertTrue(test_action.validate(self._mock_game_state))

    def test_discard_coins_action_coins_invalid(self):
        # Arrange
        self._mock_coins = {
            mock.create_autospec(spec=i_coin_type, spec_set=True): 2,
            self._mock_coin_type_list[1]: 1
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = discard_coins_action.DiscardCoinsAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins
            )

    def test_discard_coins_action_coins_invalid_empty(self):
        # Arrange
        self._mock_coins = {}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = discard_coins_action.DiscardCoinsAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins
            )

    def test_discard_coins_action_init_invalid_request_low_number(self):
        # Arrange
        self._mock_coins = {self._mock_coin_type_list[1]: -1}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = discard_coins_action.DiscardCoinsAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins
            )

    def test_discard_coins_action_init_invalid_request_zero_number(self):
        # Arrange
        self._mock_coins = {self._mock_coin_type_list[0]: 0}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = discard_coins_action.DiscardCoinsAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins
            )

    def test_discard_coins_action_validate_true(self):
        # Arrange
        # Act
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Assert
        self.assertTrue(test_action.validate(self._mock_game_state))

    def test_discard_coins_action_validate_false_player_has_not_got_the_coins(self):
        # Arrange
        self._mock_coin_inventory.has_minimum.return_value = False
        # Act
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Assert
        self.assertFalse(test_action.validate(self._mock_game_state))

    def test_discard_coins_action_validate_false_discard_too_many(self):
        # Arrange
        self._mock_coin_inventory.get_number_of_coins.return_value = 11
        # Act
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Assert
        self.assertFalse(test_action.validate(self._mock_game_state))

    def test_discard_coins_action_validate_false_discard_too_few(self):
        # Arrange
        self._mock_coin_inventory.get_number_of_coins.return_value = 13
        # Act
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Assert
        self.assertFalse(test_action.validate(self._mock_game_state))

    def test_discard_coins_action_execute_coins_added_to_reserve(self):
        # Arrange
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_coin_reserve.add_coins.assert_called_once_with(self._mock_coins)

    def test_discard_coins_action_execute_player_coins_removed(self):
        # Arrange
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_coin_inventory.remove_coins.assert_called_once_with(self._mock_coins)

    def test_discard_coins_action_execute_validate_false(self):
        # Arrange
        self._mock_coin_inventory.get_number_of_coins.return_value = 13
        # Act
        test_action = discard_coins_action.DiscardCoinsAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins
        )
        # Assert
        with self.assertRaises(ValueError):
            test_action.execute(self._mock_game_state)
