import copy
import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.sponsor.sponsor as sponsor


class TestSponsor(unittest.TestCase):
    def setUp(self):
        self._mock_name = "sponsor_name"

        self._mock_victory_points = 3
        self._mock_coin_type_list = [mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(3)]
        for i, coin in enumerate(self._mock_coin_type_list):
            coin.get_name.return_value = 'ABCDEF'[i]

        self._mock_cost = {}
        for card in self._mock_coin_type_list:
            self._mock_cost[card] = 2

    def test_sponsor_init_valid(self):
        # Arrange
        # Act
        test_sponsor = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        # Assert
        self.assertEqual(test_sponsor.get_victory_points(), self._mock_victory_points)
        self.assertEqual(test_sponsor.get_cost(), self._mock_cost)

    def test_sponsor_init_invalid_victory_points(self):
        # Arrange
        self._mock_victory_points = 0
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)

    def test_sponsor_init_invalid_cost_empty(self):
        # Arrange
        self._mock_cost = {}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)

    def test_sponsor_init_invalid_cost_negative_cost(self):
        # Arrange
        self._mock_cost[self._mock_coin_type_list[0]] = -1
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)

    def test_sponsor_init_cost_post_init_immutability(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        pre_mutation = copy.copy(self._mock_cost)
        # Act
        self._mock_cost.pop(list(self._mock_cost.keys())[0])
        # Assert
        self.assertEqual(test_sponsor.get_cost(), pre_mutation)

    def test_sponsor_get_name(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        # Act
        # Assert
        self.assertEqual(test_sponsor.get_name(), self._mock_name)

    def test_sponsor_get_victory_points(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        # Act
        # Assert
        self.assertEqual(test_sponsor.get_victory_points(), self._mock_victory_points)

    def test_sponsor_get_cost(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        # Act
        # Assert
        self.assertEqual(test_sponsor.get_cost(), self._mock_cost)

    def test_sponsor_get_cost_immutability(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        return_value = test_sponsor.get_cost()
        pre_mutation = copy.copy(return_value)
        # Act
        return_value.pop(list(return_value)[0])
        # Assert
        self.assertEqual(test_sponsor.get_cost(), pre_mutation)

    def test_sponsor_to_json(self):
        # Arrange
        test_sponsor = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        # Act
        # Assert
        expected = {
            "name": self._mock_name,
            "victory_points": self._mock_victory_points,
            "cost": [
                {
                    'coin_name': coin.get_name(),
                    'count': number
                }
                for coin, number in self._mock_cost.items()
            ]
        }
        real = test_sponsor.to_json()
        self.assertEqual(real['name'], expected['name'])
        self.assertEqual(real['victory_points'], expected['victory_points'])
        self.assertCountEqual(real['cost'], expected['cost'])

    def test_sponsor_to_json_complies_with_schema(self):
        # Arrange
        test_json_validator = json_validator.JsonValidator(json_schemas.JSON_SPONSOR_SCHEMA)
        # Act
        test_sponsor = sponsor.Sponsor(self._mock_name, self._mock_victory_points, self._mock_cost)
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(test_sponsor.to_json())
        )
