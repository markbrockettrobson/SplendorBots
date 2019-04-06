import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_payment_manager as i_payment_manager
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.src.action.purchase_reserved_card_action as purchase_reserved_card_action


class TestPurchaseReservedCardAction(unittest.TestCase):

    def setUp(self):
        self._mock_coin_types = [mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(4)]
        self._mock_valid_coin_type_set = {
            self._mock_coin_types[0],
            self._mock_coin_types[1],
            self._mock_coin_types[2],
        }
        self._mock_card = mock.create_autospec(spec=i_card.ICard, spec_set=True)

        self._mock_player = mock.create_autospec(spec=i_player.IPlayer, spec_set=True)
        self._mock_coin_inventory = mock.create_autospec(
            spec=i_player_coin_inventory.IPlayerCoinInventory,
            spec_set=True
        )
        self._mock_coin_inventory.has_minimum.return_value = True
        self._mock_card_inventory = mock.create_autospec(
            spec=i_player_card_inventory.IPlayerCardInventory,
            spec_set=True
        )
        self._mock_card_inventory.get_reserved_card_set.return_value = {
            self._mock_card
        }
        self._mock_player.get_coin_inventory.return_value = self._mock_coin_inventory
        self._mock_player.get_card_inventory.return_value = self._mock_card_inventory
        self._mock_coins = {
            self._mock_coin_types[0]: 2,
            self._mock_coin_types[1]: 2,
            self._mock_coin_types[2]: 4,
        }

        self._mock_game_state = mock.create_autospec(spec=i_game_state.IGameState, spec_set=True)

        self._mock_coin_reserve = mock.create_autospec(spec=i_coin_reserve.ICoinReserve, spec_set=True)
        self._mock_game_state.get_coin_reserve.return_value = self._mock_coin_reserve

        self._mock_card_reserve = mock.create_autospec(spec=i_card_reserve.ICardReserve, spec_set=True)
        self._mock_game_state.get_card_reserve.return_value = self._mock_card_reserve

        self._mock_payment_manager = mock.create_autospec(spec=i_payment_manager.IPaymentManager, spec_set=True)
        self._mock_payment_manager.validate_payment.return_value = True
        self._mock_game_state.get_payment_manager.return_value = self._mock_payment_manager

    def test_purchase_reserve_card_action_init_valid(self):
        # Arrange
        # Act
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertTrue(test_action.validate(self._mock_game_state))

    def test_purchase_reserved_card_action_init_mock_coins_immutability(self):
        # Arrange
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        self._mock_coins.pop(self._mock_coin_types[0])
        # Assert
        self.assertTrue(test_action.validate(self._mock_game_state))

    def test_purchase_reserved_card_action_invalid_coin_type(self):
        # Arrange
        self._mock_coins = {
            self._mock_coin_types[3]: 2
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = purchase_reserved_card_action.PurchaseReservedCardAction(
                self._mock_valid_coin_type_set,
                self._mock_player,
                self._mock_coins,
                self._mock_card
            )

    def test_purchase_reserved_card_action_init_validate_true(self):
        # Arrange
        # Act
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertTrue(test_action.validate(self._mock_game_state))

    def test_purchase_reserved_card_action_validate_false_player_out_of_coins(self):
        # Arrange
        self._mock_coin_inventory.has_minimum.return_value = False
        # Act
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertFalse(test_action.validate(self._mock_game_state))

    def test_purchase_reserved_card_action_validate_false_card_not_in_reserve(self):
        # Arrange
        self._mock_card_inventory.get_reserved_card_set.return_value = {}
        # Act
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertFalse(test_action.validate(self._mock_game_state))

    def test_purchase_reserved_card_action_validate_false_invalid_payment(self):
        # Arrange
        self._mock_payment_manager.validate_payment.return_value = False
        # Act
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Assert
        self.assertFalse(test_action.validate(self._mock_game_state))

    def test_purchase_reserved_card_action_execute_validate_false(self):
        # Arrange
        self._mock_payment_manager.validate_payment.return_value = False
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_action.execute(self._mock_game_state)

    def test_purchase_reserved_card_action_execute_coins_added_to_reserve(self):
        # Arrange
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_coin_reserve.add_coins.assert_called_once_with(self._mock_coins)

    def test_purchase_reserved_card_action_execute_coins_removed_from_player(self):
        # Arrange
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_coin_inventory.remove_coins.assert_called_once_with(self._mock_coins)

    def test_purchase_reserved_card_action_execute_card_remove_from_reserved_card_set(self):
        # Arrange
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_card_inventory.remove_from_reserved_card_set.assert_called_once_with(self._mock_card)

    def test_purchase_reserved_card_action_execute_card_added_to_player_inventory(self):
        # Arrange
        test_action = purchase_reserved_card_action.PurchaseReservedCardAction(
            self._mock_valid_coin_type_set,
            self._mock_player,
            self._mock_coins,
            self._mock_card
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_card_inventory.add_card.assert_called_once_with(self._mock_card)
