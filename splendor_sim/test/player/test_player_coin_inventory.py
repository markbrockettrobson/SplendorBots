import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.player_coin_inventory as player_coin_inventory


class TestPlayerCoinInventory(unittest.TestCase):
    def setUp(self):
        self._mock_coin_type_manager = mock.create_autospec(
            spec=i_coin_type_manager.ICoinTypeManager, spec_set=True
        )
        self._mock_coin_type_list = [
            mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
            for _ in range(6)
        ]
        self._mock_coin_type_set = set(self._mock_coin_type_list)
        self._mock_coin_type_manager.get_coin_set.return_value = (
            self._mock_coin_type_set
        )
        for i, _mock_coin_type in enumerate(self._mock_coin_type_list):
            _mock_coin_type.get_total_number.return_value = 7
            _mock_coin_type.get_name.return_value = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
        self._mock_coin_type_list[-1].get_total_number.return_value = 5

        self._return_dictionary = {coin: 7 for coin in self._mock_coin_type_list}
        self._return_dictionary[self._mock_coin_type_list[-1]] = 5

        self.test_player_coin_inventory = player_coin_inventory.PlayerCoinInventory(
            self._mock_coin_type_manager, {}
        )

    def test_player_coin_inventory_get_coins_remaining(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[-1]: 1,
        }
        expected = add
        self.test_player_coin_inventory = player_coin_inventory.PlayerCoinInventory(
            self._mock_coin_type_manager, add
        )
        # Act
        real = self.test_player_coin_inventory.get_coins()
        # Assert
        self.assertEqual(real, expected)

    def test_player_coin_inventory_get_coins_remaining_empty(self):
        # Arrange
        expected = {}
        # Act
        real = self.test_player_coin_inventory.get_coins()
        # Assert
        self.assertEqual(real, expected)

    def test_player_coin_inventory_has_minimum_true(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 12,
        }
        self.test_player_coin_inventory.add_coins(add)
        minimum = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 5,
        }

        # Act
        real = self.test_player_coin_inventory.has_minimum(minimum)
        # Assert
        self.assertTrue(real)

    def test_player_coin_inventory_has_minimum_false(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[2]: 7,
            self._mock_coin_type_list[-1]: 9,
        }
        minimum = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[2]: 8,
            self._mock_coin_type_list[-1]: 5,
        }
        # Act
        self.test_player_coin_inventory.add_coins(add)
        real = self.test_player_coin_inventory.has_minimum(minimum)
        # Assert
        self.assertFalse(real)

    def test_player_coin_inventory_has_minimum_type_error_new_coin_type(self):
        # Arrange
        new_mock_coin = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        minimum = {new_mock_coin: 0}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = self.test_player_coin_inventory.has_minimum(minimum)

    def test_player_coin_inventory_add_coins(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 3,
            self._mock_coin_type_list[-1]: 3,
        }
        expected = add
        # Act
        self.test_player_coin_inventory.add_coins(add)
        real = self.test_player_coin_inventory.get_coins()
        # Assert
        self.assertEqual(real, expected)

    def test_player_coin_inventory_add_coins_multiple_times(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 3,
            self._mock_coin_type_list[-1]: 3,
        }
        expected = {
            self._mock_coin_type_list[0]: 6,
            self._mock_coin_type_list[2]: 6,
            self._mock_coin_type_list[-1]: 6,
        }
        # Act
        self.test_player_coin_inventory.add_coins(add)
        self.test_player_coin_inventory.add_coins(add)
        real = self.test_player_coin_inventory.get_coins()
        # Assert
        self.assertEqual(real, expected)

    def test_player_coin_inventory_add_coins_type_error_new_coin_type(self):
        # Arrange
        new_mock_coin = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        add = {new_mock_coin: 0}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_player_coin_inventory.add_coins(add)

    def test_player_coin_inventory_remove_coins(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 8,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 7,
        }
        remove = {
            self._mock_coin_type_list[0]: 7,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 3,
        }
        expected = {self._mock_coin_type_list[0]: 1, self._mock_coin_type_list[-1]: 4}
        # Act
        self.test_player_coin_inventory.add_coins(add)
        self.test_player_coin_inventory.remove_coins(remove)
        real = self.test_player_coin_inventory.get_coins()
        # Assert
        self.assertEqual(real, expected)

    def test_player_coin_inventory_remove_coins_bellow_zero(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 5,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 6,
        }
        remove = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 7,
        }
        self.test_player_coin_inventory.add_coins(add)
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_player_coin_inventory.remove_coins(remove)

    def test_player_coin_inventory_remove_coins_type_error_new_coin_type(self):
        # Arrange
        new_mock_coin = mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True)
        remove = {new_mock_coin: 0}
        # Act
        # Assert
        with self.assertRaises(ValueError):
            self.test_player_coin_inventory.remove_coins(remove)

    def test_player_coin_inventory_get_coins_immutability(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 5,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[-1]: 6,
        }
        self.test_player_coin_inventory.add_coins(add)
        pre_mutation = self.test_player_coin_inventory.get_coins()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertNotEqual(pre_mutation, self.test_player_coin_inventory.get_coins())

    def test_player_coin_inventory_get_number_of_coins(self):
        add = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[-1]: 1,
        }
        self.test_player_coin_inventory.add_coins(add)
        # Act
        real = self.test_player_coin_inventory.get_number_of_coins()
        # Assert
        self.assertEqual(real, 6)

    def test_coin_reserve_to_json_empty(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual({"coin_stocks": []}, self.test_player_coin_inventory.to_json())

    def test_coin_reserve_to_json(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 1,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 3,
        }
        self.test_player_coin_inventory = player_coin_inventory.PlayerCoinInventory(
            self._mock_coin_type_manager, add
        )
        # Act
        # Assert
        self.assertEqual(
            {
                "coin_stocks": [
                    {"coin_name": "A", "count": 1},
                    {"coin_name": "B", "count": 2},
                    {"coin_name": "C", "count": 3},
                ]
            },
            self.test_player_coin_inventory.to_json(),
        )

    def test_coin_reserve_to_json_non_empty_coins_not_transfer(self):
        # Arrange
        add = {
            self._mock_coin_type_list[0]: 1,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 0,
        }
        self.test_player_coin_inventory = player_coin_inventory.PlayerCoinInventory(
            self._mock_coin_type_manager, add
        )
        # Act
        # Assert
        self.assertEqual(
            {
                "coin_stocks": [
                    {"coin_name": "A", "count": 1},
                    {"coin_name": "B", "count": 2},
                ]
            },
            self.test_player_coin_inventory.to_json(),
        )

    def test_coin_reserve_to_json_complies_with_schema(self):
        # Arrange
        test_json_validator = json_validator.JsonValidator(
            json_schemas.JSON_PLAYER_COIN_INVENTORY
        )
        # Act
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(self.test_player_coin_inventory.to_json())
        )
