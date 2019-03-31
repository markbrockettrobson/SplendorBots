import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.src.action.reserve_card_action as reserve_card_action


class TestReserveCardAction(unittest.TestCase):

    def setUp(self):
        self._mock_card = mock.create_autospec(spec=i_card.ICard, spec_set=True)
        self._mock_coin_type = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        self._mock_valid_coin_type_set = {self._mock_coin_type}

        self._mock_player = mock.create_autospec(spec=i_player.IPlayer, spec_set=True)
        self._mock_coin_inventory = mock.create_autospec(
            spec=i_player_coin_inventory.IPlayerCoinInventory,
            spec_set=True
        )
        self._mock_card_inventory = mock.create_autospec(
            spec=i_player_card_inventory.IPlayerCardInventory,
            spec_set=True
        )
        self._mock_card_inventory.get_max_number_of_reserved_cards.return_value = 3
        self._mock_card_inventory.get_number_of_reserved_cards.return_value = 0

        self._mock_player.get_coin_inventory.return_value = self._mock_coin_inventory
        self._mock_player.get_card_inventory.return_value = self._mock_card_inventory
        self._mock_coins = {self._mock_coin_type: 1}

        self._mock_game_state = mock.create_autospec(spec=i_game_state.IGameState, spec_set=True)

        self._mock_coin_reserve = mock.create_autospec(spec=i_coin_reserve.ICoinReserve, spec_set=True)
        self._mock_game_state.get_coin_reserve.return_value = self._mock_coin_reserve
        self._mock_coin_reserve.has_minimum.return_value = True

        self._mock_card_reserve = mock.create_autospec(spec=i_card_reserve.ICardReserve, spec_set=True)
        self._mock_game_state.get_card_reserve.return_value = self._mock_card_reserve
        self._mock_card_reserve.get_cards_for_sale.return_value = {self._mock_card}

    def test_reserve_card_action_init_valid(self):
        # Arrange
        # Act
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertEqual(
            test_action.validate(self._mock_game_state),
            True
        )

    def test_reserve_card_action_post_init_valid_mock_coins_immutability(self):
        # Arrange
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        self._mock_valid_coin_type_set.pop()
        # Assert
        self.assertEqual(
            test_action.validate(self._mock_game_state),
            True
        )

    def test_reserve_card_action_init_invalid_coin_type(self):
        # Arrange
        self._mock_valid_coin_type_set = \
            set(mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(1))
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = reserve_card_action.ReserveCardAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins,
                self._mock_card
            )

    def test_reserve_card_action_init_invalid_coin_request_high_number(self):
        # Arrange
        self._mock_coins = {self._mock_coin_type: 2}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = reserve_card_action.ReserveCardAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins,
                self._mock_card
            )

    def test_reserve_card_action_init_invalid_coin_request_low_number(self):
        # Arrange
        self._mock_coins = {self._mock_coin_type: -1}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = reserve_card_action.ReserveCardAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins,
                self._mock_card
            )

    def test_reserve_card_action_init_invalid_coin_request_type(self):
        # Arrange
        self._mock_coins = {mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True): 1}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = reserve_card_action.ReserveCardAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins,
                self._mock_card
            )

    def test_reserve_card_action_validate_true(self):
        # Arrange
        # Act
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertEqual(
            test_action.validate(self._mock_game_state),
            True
        )

    def test_reserve_card_action_validate_false_out_of_coins(self):
        # Arrange
        self._mock_coin_reserve.has_minimum.return_value = False
        # Act
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertEqual(
            test_action.validate(self._mock_game_state),
            False
        )

    def test_reserve_card_action_validate_false_can_not_reserve_more_cards(self):
        # Arrange
        self._mock_card_inventory.get_number_of_reserved_cards.return_value = 3
        # Act
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertEqual(
            test_action.validate(self._mock_game_state),
            False
        )

    def test_reserve_card_action_validate_false_card_not_for_sale(self):
        # Arrange
        self._mock_card_reserve.get_cards_for_sale.return_value = {}
        # Act
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertEqual(
            test_action.validate(self._mock_game_state),
            False
        )

    def test_collect_three_coins_action_execute_invalid_game_state_out_of_coins(self):
        # Arrange
        self._mock_coin_reserve.has_minimum.return_value = False
        # Act
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        with self.assertRaises(ValueError):
            test_action.execute(self._mock_game_state)

    def test_collect_three_coins_action_execute_invalid_game_state_can_not_reserve_more_cards(self):
        # Arrange
        self._mock_card_inventory.get_number_of_reserved_cards.return_value = 3
        # Act
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        with self.assertRaises(ValueError):
            test_action.execute(self._mock_game_state)

    def test_collect_three_coins_action_execute_invalid_game_card_not_for_sale(self):
        # Arrange
        self._mock_card_reserve.get_cards_for_sale.return_value = {}
        # Act
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        with self.assertRaises(ValueError):
            test_action.execute(self._mock_game_state)

    def test_collect_three_coins_action_execute_coins_leave_reserve(self):
        # Arrange
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_coin_reserve.remove_coins.assert_called_once_with(self._mock_coins)

    def test_collect_three_coins_action_execute_player_gains_coins(self):
        # Arrange
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_coin_inventory.add_coins.assert_called_once_with(self._mock_coins)

    def test_collect_three_coins_action_execute_cards_leave_reserve(self):
        # Arrange
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_card_reserve.remove_card.assert_called_once_with(self._mock_card)

    def test_collect_three_coins_action_execute_player_gains_card(self):
        # Arrange
        test_action = reserve_card_action.ReserveCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_card_inventory.add_card_to_reserved.assert_called_once_with(self._mock_card)
