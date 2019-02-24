import unittest
import unittest.mock as mock
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.card.card as card


class TestCard(unittest.TestCase):

    def setUp(self):
        self._tier = 1
        self._victory_points = 0
        self._discount = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        self._cost = {mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True): 1 for _ in range(3)}

    def test_card_init_valid(self):
        # Arrange
        # Act
        test_card = card.Card(self._tier,
                              self._victory_points,
                              self._discount,
                              self._cost)

        # Assert
        self.assertEqual(test_card.get_tier(), self._tier)
        self.assertEqual(test_card.get_victory_points(), self._victory_points)
        self.assertEqual(test_card.get_discount(), self._discount)
        self.assertEqual(test_card.get_cost(), self._cost)

    def test_card_init_invalid_tier(self):
        # Arrange
        self._tier = 0
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = card.Card(self._tier,
                          self._victory_points,
                          self._discount,
                          self._cost)

    def test_card_init_invalid_victory_points(self):
        # Arrange
        self._victory_points = -1
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = card.Card(self._tier,
                          self._victory_points,
                          self._discount,
                          self._cost)

    def test_card_init_invalid_cost(self):
        # Arrange
        self._cost[list(self._cost)[0]] = -1
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = card.Card(self._tier,
                          self._victory_points,
                          self._discount,
                          self._cost)
