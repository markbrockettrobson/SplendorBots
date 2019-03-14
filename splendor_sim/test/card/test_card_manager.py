import copy
import unittest
import unittest.mock as mock
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.src.card.card_manager as card_manager


class TestCardManager(unittest.TestCase):

    def setUp(self):
        self._mock_card_list = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in range(30)]
        self._mock_card_set = set(self._mock_card_list)
        for i, _mock_card in enumerate(self._mock_card_list):
            _mock_card.get_tier.return_value = i % 3 + 1

    def test_card_manager_init_valid(self):
        # Arrange
        # Act
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Assert
        self.assertEqual(test_card_manager.get_card_set(), self._mock_card_set)
        self.assertEqual(len(test_card_manager.get_card_tier(1)), 10)
        self.assertEqual(len(test_card_manager.get_card_tier(2)), 10)
        self.assertEqual(len(test_card_manager.get_card_tier(3)), 10)

    def test_card_manager_card_list_post_init_immutability(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        pre_mutation = copy.copy(self._mock_card_set)
        # Act
        self._mock_card_set.pop()
        # Assert
        self.assertEqual(pre_mutation, test_card_manager.get_card_set())

    def test_card_manager_get_card_list(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Act
        card_set = test_card_manager.get_card_set()
        # Assert
        self.assertEqual(card_set, self._mock_card_set)

    def test_card_manager_get_card_tier(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        expected = {1: {self._mock_card_list[i] for i in range(0, 30, 3)},
                    2: {self._mock_card_list[i] for i in range(1, 30, 3)},
                    3: {self._mock_card_list[i] for i in range(2, 30, 3)}}
        for i in range(1, 4):
            # Act
            card_set = test_card_manager.get_card_tier(i)
            # Assert
            self.assertEqual(expected[i], card_set)

    def test_card_manager_get_card_tier_unknown_tier(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = test_card_manager.get_card_tier(20)

    def test_card_manager_card_list_immutability(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        pre_mutation = test_card_manager.get_card_set()
        # Act
        pre_mutation.pop()
        # Assert
        self.assertEqual(self._mock_card_set, test_card_manager.get_card_set())
