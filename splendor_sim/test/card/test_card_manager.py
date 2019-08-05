import copy
import unittest
import unittest.mock as mock

import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.src.card.card_manager as card_manager
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator


class TestCardManager(unittest.TestCase):
    def setUp(self):
        self._mock_card_list = [
            mock.create_autospec(spec=i_card.ICard, spec_set=True) for _ in range(30)
        ]
        self._mock_card_set = set(self._mock_card_list)
        for i, _mock_card in enumerate(self._mock_card_list):
            _mock_card.get_tier.return_value = i % 3 + 1
            _mock_card.get_name.return_value = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[
                i
            ]
            _mock_card.to_json.return_value = {
                "json": "mock json for card %s" % _mock_card.get_name()
            }

    def test_card_manager_init_valid(self):
        # Arrange
        # Act
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Assert
        self.assertEqual(test_card_manager.get_card_set(), self._mock_card_set)
        self.assertEqual(len(test_card_manager.get_card_tier(1)), 10)
        self.assertEqual(len(test_card_manager.get_card_tier(2)), 10)
        self.assertEqual(len(test_card_manager.get_card_tier(3)), 10)

    def test_card_manager_init_invalid_repeated_card_name(self):
        # Arrange
        self._mock_card_list[1].get_name.return_value = "a"
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = card_manager.CardManager(self._mock_card_set)

    def test_card_manager_card_list_post_init_immutability(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        pre_mutation = copy.copy(self._mock_card_set)
        # Act
        self._mock_card_set.pop()
        # Assert
        self.assertEqual(pre_mutation, test_card_manager.get_card_set())

    def test_card_manager_get_tier(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Act
        # Assert
        self.assertEqual(test_card_manager.get_tiers(), {1, 2, 3})

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
        expected = {
            1: {self._mock_card_list[i] for i in range(0, 30, 3)},
            2: {self._mock_card_list[i] for i in range(1, 30, 3)},
            3: {self._mock_card_list[i] for i in range(2, 30, 3)},
        }
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

    def test_card_manager_is_card_in_manager_by_name_true(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Act
        # Assert
        self.assertTrue(test_card_manager.is_card_in_manager_by_name("a"))
        self.assertTrue(test_card_manager.is_card_in_manager_by_name("r"))
        self.assertTrue(test_card_manager.is_card_in_manager_by_name("q"))
        self.assertTrue(test_card_manager.is_card_in_manager_by_name("A"))

    def test_card_manager_is_card_in_manager_by_name_false(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Act
        # Assert
        self.assertFalse(test_card_manager.is_card_in_manager_by_name("Z"))
        self.assertFalse(test_card_manager.is_card_in_manager_by_name("K"))
        self.assertFalse(test_card_manager.is_card_in_manager_by_name("F"))
        self.assertFalse(test_card_manager.is_card_in_manager_by_name("1"))

    def test_card_manager_get_card_by_name(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Act
        # Assert
        self.assertEqual(
            test_card_manager.get_card_by_name("a"), self._mock_card_list[0]
        )
        self.assertEqual(
            test_card_manager.get_card_by_name("z"), self._mock_card_list[25]
        )

    def test_card_manager_get_card_by_name_name_not_in_manger(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = test_card_manager.get_card_by_name("Z")

    def test_card_manager_to_json(self):
        # Arrange
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        expected_json = {"cards": [card.to_json() for card in self._mock_card_set]}
        # Act
        # Assert
        self.assertCountEqual(
            expected_json["cards"], test_card_manager.to_json()["cards"]
        )

    def test_card_manager_to_json_complies_with_schema(self):
        # Arrange
        test_json_validator = json_validator.JsonValidator(
            json_schemas.JSON_CARD_MANAGER_SCHEMA
        )
        # Act
        test_card_manager = card_manager.CardManager(self._mock_card_set)
        # Assert
        self.assertTrue(test_json_validator.validate_json(test_card_manager.to_json()))
