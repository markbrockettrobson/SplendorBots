import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.player.json_player_coin_inventory as json_player_coin_inventory


class TestJsonPlayerCoinInventory(unittest.TestCase):

    def set_up_validator(self):
        self._validator_patcher = mock.patch(
            'splendor_sim.src.player.json_player_coin_inventory.JsonPlayerCoinInventory._JSON_VALIDATOR',
            autospec=True
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

    def set_up_coins(self):
        self._mock_coin_types = [mock.create_autospec(spec=i_coin_type.ICoinType, specset=True) for _ in range(6)]
        self._mock_coin_type_set = set(self._mock_coin_types)

        for i, coin in enumerate(self._mock_coin_types):
            coin.get_name.return_value = "name_%d" % i

        self._coin_name_map = {coin.get_name(): coin for coin in self._mock_coin_types}

    def set_up_player_coin_inventory(self):
        self._player_coin_inventory_patcher = mock.patch(
            'splendor_sim.src.player.json_player_coin_inventory.player_coin_inventory.PlayerCoinInventory.__init__',
            autospec=True
        )
        self._mock_player_coin_inventory_init = self._player_coin_inventory_patcher.start()
        self.addCleanup(self._player_coin_inventory_patcher.stop)

    def setUp(self):
        self.set_up_validator()
        self.set_up_coins()
        self.set_up_player_coin_inventory()

        self._mock_coin_stocks = [
            {
                'coin_name': self._mock_coin_types[0].get_name(),
                'count': 0
            },
            {
                'coin_name': self._mock_coin_types[1].get_name(),
                'count': 1
            },
            {
                'coin_name': self._mock_coin_types[2].get_name(),
                'count': 2
            },
            {
                'coin_name': self._mock_coin_types[3].get_name(),
                'count': 3
            },
            {
                'coin_name': self._mock_coin_types[4].get_name(),
                'count': 4
            },
            {
                'coin_name': self._mock_coin_types[5].get_name(),
                'count': 5
            },
        ]
        self._mock_coin_stocks_by_object_pointer = {
            self._mock_coin_types[0]: 0,
            self._mock_coin_types[1]: 1,
            self._mock_coin_types[2]: 2,
            self._mock_coin_types[3]: 3,
            self._mock_coin_types[4]: 4,
            self._mock_coin_types[5]: 5,
        }

        self._mock_json = {
            'coin_stocks': self._mock_coin_stocks
        }

        self._mock_game_state = mock.create_autospec(spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True)
        self._mock_coin_reserve = mock.create_autospec(spec=i_coin_reserve.ICoinReserve, spec_set=True)
        self._mock_coin_type_manager = mock.create_autospec(spec=i_coin_type_manager.ICoinTypeManager, spec_set=True)

        self._mock_game_state.get_coin_reserve.return_value = self._mock_coin_reserve
        self._mock_coin_reserve.get_manager.return_value = self._mock_coin_type_manager
        self._mock_coin_type_manager.get_coin_by_name.side_effect = lambda name: self._coin_name_map[name]
        self._mock_coin_type_manager.is_coin_in_manager_by_name.side_effect = \
            lambda name: name in self._coin_name_map

    def test_json_player_coin_inventory_init(self):
        # Arrange
        mock_dict = mock.Mock()
        # Act
        object_pointer = json_player_coin_inventory.JsonPlayerCoinInventory(
            self._mock_coin_type_manager,
            mock_dict
        )
        # Assert
        self._mock_player_coin_inventory_init.assert_called_once_with(
            object_pointer,
            self._mock_coin_type_manager,
            mock_dict
        )

    def test_json_player_coin_inventory_init_coin_stocks(self):
        # Arrange
        # Act
        object_pointer = json_player_coin_inventory.JsonPlayerCoinInventory(
            self._mock_coin_type_manager,
            self._mock_coin_stocks_by_object_pointer
        )
        # Assert
        self._mock_player_coin_inventory_init.assert_called_once_with(
            object_pointer,
            self._mock_coin_type_manager,
            self._mock_coin_stocks_by_object_pointer
        )

    def test_json_player_coin_inventory_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_player_coin_inventory.JsonPlayerCoinInventory.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_player_coin_inventory_init.assert_called_once_with(
            object_pointer,
            self._mock_coin_type_manager,
            self._mock_coin_stocks_by_object_pointer
        )

    def test_json_player_coin_inventory_build_from_json_invalid(self):
        # Arrange

        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_coin_inventory.JsonPlayerCoinInventory.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_player_coin_inventory_build_from_json_invalid_coin_name_not_in_manager(self):
        # Arrange
        self._mock_coin_stocks.append(
            {
                'coin_name': "not a name in the manager",
                'count': 0
            }
        )
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_coin_inventory.JsonPlayerCoinInventory.build_from_json(
                self._mock_json,
                self._mock_game_state
            )

    def test_json_player_coin_inventory_get_json_schema(self):
        # Arrange
        object_pointer = json_player_coin_inventory.JsonPlayerCoinInventory.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Act
        # Assert
        self.assertEqual(object_pointer.get_json_schema(), json_schemas.JSON_PLAYER_COIN_INVENTORY)

    def test_json_player_coin_inventory_get_json_schema_immutability(self):
        # Arrange
        object_pointer = json_player_coin_inventory.JsonPlayerCoinInventory.build_from_json(
            self._mock_json,
            self._mock_game_state
        )
        # Act
        object_pointer.get_json_schema().pop(list(object_pointer.get_json_schema())[0])
        # Assert
        self.assertEqual(object_pointer.get_json_schema(), json_schemas.JSON_PLAYER_COIN_INVENTORY)
