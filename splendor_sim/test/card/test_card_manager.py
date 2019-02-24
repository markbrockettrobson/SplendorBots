import unittest
import unittest.mock as mock
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.card.card_manager as card_manager


class TestCardManager(unittest.TestCase):

    def setUp(self):
        self._mock_coin_type_list = [mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(5)]
        self._mock_coin_type_manger = mock.create_autospec(spec=i_coin_type_manager.ICoinTypeManager, spec_set=True)
        self._mock_coin_type_manger.get_coin_list.return_value = self._mock_coin_type_list

        self._mock_card_list = [mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in range(30)]
        for i, _mock_card in enumerate(self._mock_card_list):
            _mock_card.get_tier.return_value = i % 3 + 1
            _mock_card.get_discount.return_value = self._mock_coin_type_list[i % len(self._mock_coin_type_list)]
            _mock_card.get_cost.return_value = {self._mock_coin_type_list[(i + 1) % len(self._mock_coin_type_list)]: 2,
                                                self._mock_coin_type_list[(i + 2) % len(self._mock_coin_type_list)]: 1}

    def test_card_manager_init_valid(self):
        # Arrange
        # Act
        test_card_manager = card_manager.CardManager(self._mock_card_list, self._mock_coin_type_manger)
        # Assert
        self.assertEqual(test_card_manager.get_card_list(), self._mock_card_list)
        self.assertEqual(len(test_card_manager.get_card_tier(1)), 10)
        self.assertEqual(len(test_card_manager.get_card_tier(2)), 10)
        self.assertEqual(len(test_card_manager.get_card_tier(3)), 10)

    def test_card_manager_init_invalid_card_discout(self):
        # Arrange
        self._mock_card_list[2].get_discount.return_value = \
            mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = card_manager.CardManager(self._mock_card_list, self._mock_coin_type_manger)

    def test_card_manager_init_invalid_card_cost(self):
        # Arrange
        self._mock_card_list[2].get_cost.return_value[
            mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)] = 3

        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = card_manager.CardManager(self._mock_card_list, self._mock_coin_type_manger)

    def test_card_manager_get_card_list(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_list, self._mock_coin_type_manger)
        # Act
        card_list = test_card_manager.get_card_list()
        # Assert
        self.assertEqual(card_list, self._mock_card_list)

    def test_card_manager_get_card_tier(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_list, self._mock_coin_type_manger)
        expected = {1: [self._mock_card_list[i] for i in range(0, 30, 3)],
                    2: [self._mock_card_list[i] for i in range(1, 30, 3)],
                    3: [self._mock_card_list[i] for i in range(2, 30, 3)]}
        for i in range(1, 4):
            # Act
            card_list = test_card_manager.get_card_tier(i)
            # Assert
            self.assertEqual(expected[i], card_list)

    def test_card_manager_get_card_tier_unknown_tier(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_list, self._mock_coin_type_manger)
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = test_card_manager.get_card_tier(20)
