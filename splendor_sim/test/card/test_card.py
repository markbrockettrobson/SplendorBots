import copy
import unittest
import unittest.mock as mock
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.src.card.card as card


class TestCard(unittest.TestCase):

    def setUp(self):
        self._tier = 1
        self._victory_points = 0
        self._mock_coins = [mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(4)]
        for i, coin in enumerate(self._mock_coins):
            coin.get_name.return_value = "ABCD"[i]
        self._discount = self._mock_coins[0]
        self._cost = {coin: 1 for coin in self._mock_coins[1:]}
        self._name = "Card name"

    def test_card_init_valid(self):
        # Arrange
        # Act
        test_card = card.Card(self._tier,
                              self._victory_points,
                              self._discount,
                              self._cost,
                              self._name)

        # Assert
        self.assertEqual(test_card.get_tier(), self._tier)
        self.assertEqual(test_card.get_victory_points(), self._victory_points)
        self.assertEqual(test_card.get_discount(), self._discount)
        self.assertEqual(test_card.get_cost(), self._cost)
        self.assertEqual(test_card.get_name(), self._name)

    def test_card_init_default_name(self):
        # Arrange
        # Act
        test_card = card.Card(self._tier,
                              self._victory_points,
                              self._discount,
                              self._cost)

        # Assert
        self.assertEqual(test_card.get_name(), "T1_DA_V0_CB1C1D1")

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

    def test_card_cost_post_init_immutability(self):
        # Arrange
        test_card = card.Card(self._tier,
                              self._victory_points,
                              self._discount,
                              self._cost)
        pre_mutation = copy.copy(self._cost)
        # Act
        self._cost.pop(list(self._cost.keys())[0])
        # Assert
        self.assertEqual(pre_mutation, test_card.get_cost())

    def test_card_cost_immutability(self):
        # Arrange
        test_card = card.Card(self._tier,
                              self._victory_points,
                              self._discount,
                              self._cost)
        pre_mutation = test_card.get_cost()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(self._cost, test_card.get_cost())

    def test_card_to_json(self):
        # Arrange
        test_card = card.Card(self._tier,
                              self._victory_points,
                              self._discount,
                              self._cost,
                              self._name)
        # Act
        # Assert
        expected = {
            'tier': 1,
            'victory_points': 0,
            'discounted_coin_type_name': 'A',
            'cost': [
                {
                    'coin_name': 'B',
                    'count': 1
                },
                {
                    'coin_name': 'C',
                    'count': 1
                },
                {
                    'coin_name': 'D',
                    'count': 1
                }
            ],
            'name': self._name
        }
        real = test_card.to_json()
        self.assertEqual(real['tier'], expected['tier'])
        self.assertEqual(real['victory_points'], expected['victory_points'])
        self.assertEqual(real['discounted_coin_type_name'], expected['discounted_coin_type_name'])
        self.assertCountEqual(real['cost'], expected['cost'])
        self.assertEqual(real['name'], expected['name'])
