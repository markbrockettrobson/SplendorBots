import unittest
import unittest.mock as mock
import copy
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.src.card.deck as deck


class TestDeck(unittest.TestCase):

    def setUp(self):
        self._tier = 2
        self._mock_card_list = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in range(10)]
        self._mock_card_set = set(self._mock_card_list)
        for card in self._mock_card_list:
            card.get_tier.return_value = 2

    def test_deck_init_valid_cards(self):
        # Arrange
        # Act
        test_deck = deck.Deck(self._tier, self._mock_card_set)
        while test_deck.has_next():
            # Assert
            self.assertIn(test_deck.next(), self._mock_card_set)

    def test_deck_init_invalid_tier(self):
        # Arrange
        self._tier = 0
        # Act
        with self.assertRaises(ValueError):
            # Assert
            _ = deck.Deck(self._tier, self._mock_card_set)

    def test_deck_init_invalid_cards_tier(self):
        # Arrange
        self._mock_card_list[4].get_tier.return_value = 3
        # Act
        with self.assertRaises(ValueError):
            # Assert
            _ = deck.Deck(self._tier, self._mock_card_set)

    def test_deck_card_set_post_init_immutability(self):
        # Arrange
        test_deck = deck.Deck(self._tier, self._mock_card_set)
        number_seen = 0
        pre_mutation = copy.copy(self._mock_card_set)
        # Act
        self._mock_card_set.pop()
        while test_deck.has_next():
            # Assert
            number_seen += 1
            self.assertIn(test_deck.next(), pre_mutation)
        self.assertTrue(number_seen, len(pre_mutation))

    def test_deck_has_next(self):
        # Arrange
        test_deck = deck.Deck(self._tier, self._mock_card_set)
        # Act
        # Assert
        self.assertEqual(test_deck.get_tier(), self._tier)

    def test_deck_has_next(self):
        # Arrange
        test_deck = deck.Deck(self._tier, self._mock_card_set)
        expect = [True, True, True, True, True, True, True, True, True, True, False]
        real = []
        # Act
        while test_deck.has_next():
            real.append(test_deck.has_next())
            test_deck.next()
        real.append(test_deck.has_next())
        # Assert
        self.assertEqual(expect, real)

    def test_deck_next(self):
        # Arrange
        test_deck = deck.Deck(self._tier, self._mock_card_set)
        real = []
        # Act
        while test_deck.has_next():
            real.append(test_deck.next())

        for card in real:
            # Assert
            self.assertIn(card, self._mock_card_set)

    def test_deck_number_remaining_cards(self):
        # Arrange
        test_deck = deck.Deck(self._tier, self._mock_card_set)
        expect = [10 - i for i in range(11)]
        real = []
        # Act
        while test_deck.has_next():
            real.append(test_deck.number_remaining_cards())
            test_deck.next()
        real.append(test_deck.number_remaining_cards())
        # Assert
        self.assertEqual(expect, real)

    def test_deck_get_remaining_cards(self):
        # Arrange
        test_deck = deck.Deck(self._tier, self._mock_card_set)
        # Act
        while test_deck.has_next():
            befor = test_deck.get_remaining_cards()
            test_deck.next()
            after = test_deck.get_remaining_cards()
            # Assert
            for card in after:
                self.assertIn(card, self._mock_card_set)
                self.assertIn(card, befor)
            self.assertEqual(len(befor), len(after) + 1)

    def test_deck_get_remaining_cards_immutability(self):
        # Arrange
        test_deck = deck.Deck(self._tier, self._mock_card_set)
        card_set = test_deck.get_remaining_cards()
        pre_mutaion = copy.copy(card_set)
        # Act
        card_set.pop()
        # Assert
        self.assertEqual(pre_mutaion, test_deck.get_remaining_cards())
