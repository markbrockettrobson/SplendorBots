import unittest
import unittest.mock as mock
import typing

import splendor_sim.interfaces.game_state.i_game_state as i_game_state
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.player.i_player as i_player


class TestCollectSingleCoinTypeAction(unittest.TestCase):

    def setUp(self):
        pass

    def test_collect_single_coin_type_action_init_valid(self):
        pass

    def test_collect_single_coin_type_action_init_invalid_coin_type(self):
        pass

    def test_collect_single_coin_type_action_init_invalid_number_of_coins(self):
        pass

    def test_collect_single_coin_type_action_init_invalid_request_high_invalid_number(self):
        pass

    def test_collect_single_coin_type_action_init_invalid_request_low_invalid_number(self):
        pass

    def test_collect_single_coin_type_action_init_invalid_request_zero_invalid_number(self):
        pass

    def test_collect_single_coin_type_action_validate_true(self):
        pass

    def test_collect_single_coin_type_action_validate_false(self):
        pass

    def test_collect_single_coin_type_action_execute_invalid_game_state(self):
        pass

    def test_collect_single_coin_type_action_execute_coins_leave_reserve(self):
        pass

    def test_collect_single_coin_type_action_execute_player_gains_coins(self):
        pass
