import typing
import unittest
import unittest.mock as mock
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type


class TestPlayerCardInventory(unittest.TestCase):

    def setUp(self):
        pass

    def test_player_card_inventory_init_valid(self):
        pass

    def test_player_card_inventory_init_invalid_max_reserved_cards(self):
        pass

    def test_player_card_inventory_add_card_valid(self):
        pass

    def test_player_card_inventory_add_card_card_already_in_set(self):
        pass

    def test_player_card_inventory_add_card_to_reserved(self):
        pass

    def test_player_card_inventory_add_card_to_reserved_card_already_in_set(self):
        pass

    def test_player_card_inventory_add_card_to_reserved_already_full(self):
        pass

    def test_player_card_inventory_get_total_discount(self):
        pass

    def test_player_card_inventory_get_total_discount_immutability(self):
        pass

    def test_player_card_inventory_get_victory_points(self):
        pass

    def test_player_card_inventory_get_victory_points_reserved_cards_do_not_count(self):
        pass

    def test_player_card_inventory_get_card_list(self):
        pass

    def test_player_card_inventory_get_card_list_immutability(self):
        pass

    def test_player_card_inventory_get_reserved_card_list(self):
        pass

    def test_player_card_inventory_get_reserved_card_list_immutability(self):
        pass
