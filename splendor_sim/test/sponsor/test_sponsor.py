import copy
import unittest
import unittest.mock as mock
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.src.sponsor.sponsor as sponsor


class TestSponsor(unittest.TestCase):

    def setUp(self):
        self._victory_points = 3
        self._mock_coin_type_list = [mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(3)]
        self._cost = {}
        for card in self._mock_coin_type_list:
            self._cost[card] = 2

    def test_sponsor_init_valid(self):
        # Arrange
        # Act
        test_sponsor = sponsor.Sponsor(self._victory_points, self._cost)
        # Assert
        self.assertEqual(test_sponsor.get_victory_points(), self._victory_points)
        self.assertEqual(test_sponsor.get_cost(), self._cost)

    def test_sponsor_init_invalid_victory_points(self):
        # Arrange
        self._victory_points = 0
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor.Sponsor(self._victory_points, self._cost)

    def test_sponsor_init_invalid_cost_empty(self):
        # Arrange
        self._cost = {}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor.Sponsor(self._victory_points, self._cost)

    def test_sponsor_init_invalid_cost_negative_cost(self):
        # Arrange
        self._cost[self._mock_coin_type_list[0]] = -1
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor.Sponsor(self._victory_points, self._cost)

    def test_sponsor_init_cost_post_init_immutability(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._victory_points, self._cost)
        pre_mutation = copy.copy(self._cost)
        # Act
        self._cost.pop(list(self._cost.keys())[0])
        # Assert
        self.assertEqual(test_sponsor.get_cost(), pre_mutation)

    def test_sponsor_get_victory_points(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._victory_points, self._cost)
        # Act
        # Assert
        self.assertEqual(test_sponsor.get_victory_points(), self._victory_points)

    def test_sponsor_get_cost(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._victory_points, self._cost)
        # Act
        # Assert
        self.assertEqual(test_sponsor.get_cost(), self._cost)

    def test_sponsor_get_cost_immutability(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._victory_points, self._cost)
        return_value = test_sponsor.get_cost()
        pre_mutation = copy.copy(return_value)
        # Act
        return_value.pop(list(return_value)[0])
        # Assert
        self.assertEqual(test_sponsor.get_cost(), pre_mutation)
