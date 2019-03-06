import copy
import unittest
import unittest.mock as mock
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_deck as i_deck
import splendor_sim.src.card.card_reserve as card_reserve


class TestCardReserve(unittest.TestCase):

    def setUp(self):
        self._cards_on_sale = 3
        self._decks = 3
        self._cards_per_deck = 6
        self._mock_decks = \
            [mock.create_autospec(spec=i_deck.IDeck, spec_set=True) for _ in range(self._decks)]
        self._mock_cards_by_tier = []
        self._mock_cards = []
        mock_has_next = []

        for _ in range(self._cards_per_deck):
            mock_has_next.append(True)
        for _ in range(self._cards_per_deck):
            mock_has_next.append(False)
        for i, deck in enumerate(self._mock_decks):
            deck.number_remaining_cards.return_value = self._cards_per_deck - self._cards_on_sale
            new_mock_cards = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in
                              range(self._cards_per_deck)]

            self._mock_cards.extend(new_mock_cards)
            self._mock_cards_by_tier.append(new_mock_cards)
            deck.get_remaining_cards.return_value = set(self._mock_cards_by_tier[i])
            deck.next.side_effect = new_mock_cards
            deck.has_next.side_effect = mock_has_next
            deck.get_tier.return_value = i + 1

    def test_card_reserve_init_valid(self):
        # Arrange
        # Act
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Assert
        self.assertEqual(test_card_reserve.get_number_of_remaining_cards(), self._decks * self._cards_per_deck)

    def test_card_reserve_init_invalid_cards_on_sale(self):
        # Arrange
        self._cards_on_sale = 0
        # Act
        with self.assertRaises(ValueError):
            # Assert
            _ = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)

    def test_card_reserve_init_invalid_decks(self):
        # Arrange
        self._mock_decks = []
        # Act
        with self.assertRaises(ValueError):
            # Assert
            _ = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)

    def test_card_reserve_deck_post_init_immutability(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        self._mock_decks.pop()
        # Assert
        self.assertEqual(test_card_reserve.get_number_of_remaining_cards(), self._decks * self._cards_per_deck)

    def test_card_reserve_get_cards_for_sale_all_cards(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        returned_value = test_card_reserve.get_cards_for_sale()
        for card in returned_value:
            # Assert
            self.assertIn(card, self._mock_cards)
        self.assertEqual(len(returned_value), self._cards_on_sale * self._decks)

    def test_card_reserve_get_cards_for_sale_one_short(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck - self._cards_on_sale + 1):
            cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(1)
            test_card_reserve.remove_card(cards_in_tier[0])
        # Act
        returned_value = test_card_reserve.get_cards_for_sale()
        # Assert
        self.assertEqual(len(returned_value), self._decks * self._cards_on_sale - 1)

    def test_card_reserve_get_cards_for_sale_all_one_short(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        count = 0
        for i in range(self._decks):
            for _ in range(1 + self._cards_per_deck - self._cards_on_sale):
                cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(i + 1)
                test_card_reserve.remove_card(cards_in_tier[0])
                count += 1
        # Act
        returned_value = test_card_reserve.get_cards_for_sale()
        # Assert
        self.assertEqual(self._decks * self._cards_on_sale - self._decks, len(returned_value))

    def test_card_reserve_get_cards_for_sale_one_empty(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck):
            cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(1)
            test_card_reserve.remove_card(cards_in_tier[0])
        # Act
        returned_value = test_card_reserve.get_cards_for_sale()
        # Assert
        self.assertEqual(len(returned_value), self._decks * self._cards_on_sale - self._cards_on_sale)

    def test_card_reserve_get_cards_for_sale_all_empty(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck * self._decks):
            cards_in_tier = test_card_reserve.get_cards_for_sale()
            test_card_reserve.remove_card(cards_in_tier[0])
        # Act
        returned_value = test_card_reserve.get_cards_for_sale()
        # Assert
        self.assertEqual(len(returned_value), 0)

    def test_card_reserve_get_cards_for_sale_immutability(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        cards_in_tier = test_card_reserve.get_cards_for_sale()
        pre_mutation = copy.copy(cards_in_tier)
        # Act
        cards_in_tier.pop()
        # Assert
        self.assertEqual(test_card_reserve.get_cards_for_sale(), pre_mutation)

    def test_card_reserve_get_cards_for_sale_by_tier_invalid_tier(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        with self.assertRaises(ValueError):
            # Assert
            test_card_reserve.get_cards_for_sale_by_tier(100)

    def test_card_reserve_get_cards_for_sale_by_tier_cards_all_cards(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        returned_value = test_card_reserve.get_cards_for_sale_by_tier(2)
        for cards in returned_value:
            # Assert
            self.assertIn(cards, self._mock_cards)
        self.assertEqual(len(returned_value), self._cards_on_sale)

    def test_card_reserve_get_cards_for_sale_by_tier_cards_one_short(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck - self._cards_on_sale + 1):
            cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(1)
            test_card_reserve.remove_card(cards_in_tier[0])
        # Act
        returned_value = test_card_reserve.get_cards_for_sale_by_tier(1)
        # Assert
        self.assertEqual(len(returned_value), self._cards_on_sale - 1)

    def test_card_reserve_get_cards_for_sale_by_tier_cards_empty(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck):
            cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(1)
            test_card_reserve.remove_card(cards_in_tier[0])
        # Act
        returned_value = test_card_reserve.get_cards_for_sale_by_tier(1)
        # Assert
        self.assertEqual(len(returned_value), 0)

    def test_card_reserve_get_cards_for_sale_by_tier_immutability(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(2)
        pre_mutation = copy.copy(cards_in_tier)
        # Act
        cards_in_tier.pop()
        # Assert
        self.assertEqual(test_card_reserve.get_cards_for_sale_by_tier(2), pre_mutation)

    def test_card_reserve_remove_card_card_for_sale(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        returned_value = test_card_reserve.get_cards_for_sale()
        # Act
        test_card_reserve.remove_card(returned_value[0])
        # Assert
        self.assertNotIn(returned_value[0], test_card_reserve.get_cards_for_sale())

    def test_card_reserve_remove_card_card_not_for_sale(self):
        # Arrange
        new_mock_card = mock.create_autospec(spec=i_card.ICard, spec_set=True)
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        # Assert
        with self.assertRaises(ValueError):
            test_card_reserve.remove_card(new_mock_card)

    def test_card_reserve_remove_card_card_replaced(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        returned_value = test_card_reserve.get_cards_for_sale()
        test_card_reserve.remove_card(returned_value[0])
        # Act
        new_returned_value = test_card_reserve.get_cards_for_sale()
        # Assert
        self.assertEqual(len(new_returned_value), self._decks * self._cards_on_sale)

    def test_card_reserve_remove_card_not_replaced_out_of_deck(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck - self._cards_on_sale + 1):
            cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(1)
            test_card_reserve.remove_card(cards_in_tier[0])
        # Act
        new_returned_value = test_card_reserve.get_cards_for_sale()
        # Assert
        self.assertEqual(len(new_returned_value), self._decks * self._cards_on_sale - 1)

    def test_card_reserve_remove_top_of_deck(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        top_card = test_card_reserve.remove_top_of_deck(1)
        # Assert
        self.assertNotIn(top_card, test_card_reserve.get_cards_for_sale())

    def test_card_reserve_remove_top_of_deck_invalid_tier(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        with self.assertRaises(ValueError):
            # Assert
            test_card_reserve.remove_top_of_deck(100)

    def test_card_reserve_remove_top_of_deck_empty(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck):
            cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(1)
            test_card_reserve.remove_card(cards_in_tier[0])
        # Act
        with self.assertRaises(ValueError):
            # Assert
            test_card_reserve.remove_top_of_deck(100)

    def test_card_reserve_get_remaining_cards(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        # Assert
        self.assertEqual(test_card_reserve.get_remaining_cards(), set(self._mock_cards))

    def test_card_reserve_get_remaining_cards_empty(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck * self._decks):
            cards_in_tier = test_card_reserve.get_cards_for_sale()
            test_card_reserve.remove_card(cards_in_tier[0])

        for _, deck in enumerate(self._mock_decks):
            deck.get_remaining_cards.return_value = set()
        # Act
        # Assert
        self.assertEqual(test_card_reserve.get_remaining_cards(), set())

    def test_card_reserve_get_remaining_cards_immutability(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        card_list = test_card_reserve.get_remaining_cards()
        pre_mutation = copy.copy(card_list)
        # Act
        card_list.pop()
        # Assert
        self.assertEqual(test_card_reserve.get_remaining_cards(), pre_mutation)

    def test_card_reserve_get_remaining_cards_by_tier(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        # Assert
        self.assertEqual(test_card_reserve.get_remaining_cards_by_tier(1), set(self._mock_cards_by_tier[0]))

    def test_card_reserve_get_remaining_cards_by_tier_invalid_tier(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        with self.assertRaises(ValueError):
            # Assert
            test_card_reserve.get_remaining_cards_by_tier(100)

    def test_card_reserve_get_remaining_cards_by_tier_empty(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck):
            cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(1)
            test_card_reserve.remove_card(cards_in_tier[0])
        self._mock_decks[0].get_remaining_cards.return_value = set()
        # Act
        # Assert
        self.assertEqual(test_card_reserve.get_remaining_cards_by_tier(1), set())

    def test_card_reserve_get_remaining_cards_by_tier_immutability(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        card_list = test_card_reserve.get_remaining_cards_by_tier(1)
        pre_mutation = copy.copy(card_list)
        # Act
        card_list.pop()
        # Assert
        self.assertEqual(test_card_reserve.get_remaining_cards_by_tier(1), pre_mutation)

    def test_card_reserve_get_number_of_remaining_cards(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        # Assert
        self.assertEqual(test_card_reserve.get_number_of_remaining_cards(), self._cards_per_deck * self._decks)

    def test_card_reserve_get_number_of_remaining_cards_empty(self):
        # Arrange
        for deck in self._mock_decks:
            deck.number_remaining_cards.return_value = 0
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        for _ in range(self._cards_per_deck * self._decks):
            cards_in_tier = test_card_reserve.get_cards_for_sale()
            test_card_reserve.remove_card(cards_in_tier[0])
        # Act
        # Assert
        self.assertEqual(test_card_reserve.get_number_of_remaining_cards(), 0)

    def test_card_reserve_get_number_of_remaining_cards_by_tier(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        # Assert
        self.assertEqual(test_card_reserve.get_number_of_remaining_cards_by_tier(1), self._cards_per_deck)

    def test_card_reserve_get_number_of_remaining_cards_by_tier_invalid_tier(self):
        # Arrange
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        with self.assertRaises(ValueError):
            # Assert
            test_card_reserve.get_number_of_remaining_cards_by_tier(100)

    def test_card_reserve_get_number_of_remaining_cards_by_tier_empty(self):
        # Arrange
        self._mock_decks[0].number_remaining_cards.return_value = 0
        test_card_reserve = card_reserve.CardReserve(self._cards_on_sale, self._mock_decks)
        # Act
        for _ in range(self._cards_per_deck):
            cards_in_tier = test_card_reserve.get_cards_for_sale_by_tier(1)
            test_card_reserve.remove_card(cards_in_tier[0])
        # Assert
        self.assertEqual(test_card_reserve.get_number_of_remaining_cards_by_tier(1), 0)
