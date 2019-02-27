import copy
import unittest
import unittest.mock as mock
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve


class TestCardReserve(unittest.TestCase):

    def setUp(self):
        self._decks = 3
        self._cards_per_deck = 6
        self._mock_deck = \
            [mock.create_autospec(spec=i_card_reserve.ICardReserve, spec_set=True) for _ in range(self._decks)]
        self._mock_cards = []
        for deck in self._mock_deck:
            new_mock_cards = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in
                              range(self._cards_per_deck)]
            self._mock_cards.append(new_mock_cards)
            deck.next.side_effect = new_mock_cards

    def test_card_reserve_init_valid(self):
        pass

    def test_card_reserve_init_invalid_cards_on_sale(self):
        pass

    def test_card_reserve_init_invalid_decks(self):
        pass

    def test_card_reserve_deck_post_init_immutability(self):
        pass


    def test_card_reserve_get_cards_for_sale_all_cards(self):
        pass

    def test_card_reserve_get_cards_for_sale_one_short(self):
        pass

    def test_card_reserve_get_cards_for_sale_one_empty(self):
        pass

    def test_card_reserve_get_cards_for_sale_all_empty(self):
        pass

    def test_card_reserve_get_cards_for_sale_immutability(self):
        pass


    def test_card_reserve_get_cards_for_sale_by_tier_invalid_tier(self):
        pass

    def test_card_reserve_get_cards_for_sale_by_tier_cards_all_cards(self):
        pass

    def test_card_reserve_get_cards_for_sale_by_tier_cards_one_short(self):
        pass

    def test_card_reserve_get_cards_for_sale_by_tier_cards_one_empty(self):
        pass

    def test_card_reserve_get_cards_for_sale_by_tier_all_empty(self):
        pass

    def test_card_reserve_get_cards_for_sale_by_tier_immutability(self):
        pass


    def test_card_reserve_remove_card_card_for_sale(self):
        pass

    def test_card_reserve_remove_card_card_not_for_sale(self):
        pass

    def test_card_reserve_remove_card_card_replaced(self):
        pass

    def test_card_reserve_remove_card_not_replaced_out_of_deck(self):
        pass


    def test_card_reserve_remove_top_of_deck(self):
        pass

    def test_card_reserve_remove_top_of_deck_invalid_tier(self):
        pass

    def test_card_reserve_remove_top_of_deck_empty(self):
        pass


    def test_card_reserve_get_remaining_cards(self):
        pass

    def test_card_reserve_get_remaining_cards_empty(self):
        pass

    def test_card_reserve_get_remaining_cards_immutability(self):
        pass



    def test_card_reserve_get_remaining_cards_by_tier(self):
        pass

    def test_card_reserve_get_remaining_cards_by_tier_invalid_tier(self):
        pass

    def test_card_reserve_get_remaining_cards_by_tier_empty(self):
        pass

    def test_card_reserve_get_remaining_cards_by_tier_immutability(self):
        pass


    def test_card_reserve_get_number_of_remaining_cards(self):
        pass



    def test_card_reserve_get_number_of_remaining_cards_by_tier(self):
        pass

    def test_card_reserve_get_number_of_remaining_cards_by_tier_invalid_tier(self):
        pass