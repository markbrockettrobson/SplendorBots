import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve
import splendor_sim.src.action.purchase_sponsor_action as purchase_sponsor_action


class TestPurchaseSponsorAction(unittest.TestCase):

    def setUp(self):
        self._mock_coin_types = [mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(3)]
        self._mock_sponsors = [mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True) for _ in range(3)]
        self._mock_sponsors_cost = {
            self._mock_coin_types[0]: 3,
            self._mock_coin_types[1]: 3,
            self._mock_coin_types[2]: 3,
        }
        for sponsor in self._mock_sponsors:
            sponsor.get_cost.return_value = self._mock_sponsors_cost

        self._mock_player = mock.create_autospec(spec=i_player.IPlayer, spec_set=True)
        self._mock_card_inventory = mock.create_autospec(
            spec=i_player_card_inventory.IPlayerCardInventory,
            spec_set=True
        )
        self._mock_card_inventory.get_total_discount.return_value = {
            self._mock_coin_types[0]: 3,
            self._mock_coin_types[1]: 3,
            self._mock_coin_types[2]: 3,
        }
        self._mock_player.get_card_inventory.return_value = self._mock_card_inventory
        self._mock_sponsor_inventory = mock.create_autospec(
            spec=i_player_sponsor_inventory.IPlayerSponsorInventory,
            spec_set=True
        )
        self._mock_player.get_sponsor_inventory.return_value = self._mock_sponsor_inventory

        self._mock_game_state = mock.create_autospec(spec=i_game_state.IGameState, spec_set=True)
        self._mock_sponsor_reserve = mock.create_autospec(spec=i_sponsor_reserve.ISponsorReserve, spec_set=True)
        self._mock_sponsor_reserve.get_remaining_sponsor_set.return_value = {
            self._mock_sponsors[0],
            self._mock_sponsors[1]
        }
        self._mock_game_state.get_sponsor_reserve.return_value = self._mock_sponsor_reserve

    def test_purchase_sponsor_action_init_valid(self):
        # Arrange
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        # Assert
        self.assertTrue(
            test_action.validate(self._mock_game_state)
        )

    def test_purchase_sponsor_action_validate_false_sponsor_not_available(self):
        # Arrange
        self._mock_sponsor_reserve.get_remaining_sponsor_set.return_value = {
            self._mock_sponsors[1],
            self._mock_sponsors[2]
        }
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        # Assert
        self.assertFalse(
            test_action.validate(self._mock_game_state),
        )

    def test_purchase_sponsor_action_validate_false_player_cant_afford(self):
        # Arrange
        self._mock_card_inventory.get_total_discount.return_value = {
            self._mock_coin_types[0]: 3,
            self._mock_coin_types[1]: 3,
            self._mock_coin_types[2]: 2,
        }
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        # Assert
        self.assertFalse(
            test_action.validate(self._mock_game_state),
        )

    def test_purchase_sponsor_action_validate_false_player_cant_afford_missing_coin_type(self):
        # Arrange
        self._mock_card_inventory.get_total_discount.return_value = {
            self._mock_coin_types[0]: 3,
            self._mock_coin_types[2]: 3,
        }
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        # Assert
        self.assertFalse(
            test_action.validate(self._mock_game_state),
        )

    def test_purchase_sponsor_action_execute_invalid_sponsor_not_available(self):
        # Arrange
        self._mock_sponsor_reserve.get_remaining_sponsor_set.return_value = {
            self._mock_sponsors[1],
            self._mock_sponsors[2]
        }
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_action.execute(self._mock_game_state)

    def test_purchase_sponsor_action_execute_invalid_player_cant_afford(self):
        # Arrange
        self._mock_card_inventory.get_total_discount.return_value = {
            self._mock_coin_types[0]: 3,
            self._mock_coin_types[1]: 3,
            self._mock_coin_types[2]: 2,
        }
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_action.execute(self._mock_game_state)

    def test_purchase_sponsor_action_execute_invalid_player_cant_afford_missing_coin_type(self):
        # Arrange
        self._mock_card_inventory.get_total_discount.return_value = {
            self._mock_coin_types[0]: 3,
            self._mock_coin_types[2]: 3,
        }
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_action.execute(self._mock_game_state)

    def test_purchase_sponsor_action_execute_player_gets_sponsor(self):
        # Arrange
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_sponsor_inventory.add_sponsor.assert_called_once_with(self._mock_sponsors[0])

    def test_purchase_sponsor_action_execute_sponsor_removed_from_reserve(self):
        # Arrange
        test_action = purchase_sponsor_action.PurchaseCardAction(
            self._mock_player,
            self._mock_sponsors[0]
        )
        # Act
        test_action.execute(self._mock_game_state)
        # Assert
        self._mock_sponsor_reserve.remove_sponsor.assert_called_once_with(self._mock_sponsors[0])
