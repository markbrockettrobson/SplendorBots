import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_manager as i_sponsor_manager
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.player.json_player_sponsor_inventory as json_player_sponsor_inventory


class TestJsonPlayerCoinInventory(unittest.TestCase):
    def set_up_validator(self):
        self._validator_patcher = mock.patch(
            "splendor_sim.src.player.json_player_sponsor_inventory.JsonPlayerSponsorInventory._JSON_VALIDATOR",
            autospec=True,
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

    def set_up_sponsors(self):
        self._mock_sponsors = [
            mock.create_autospec(spec=i_sponsor.ISponsor, specset=True)
            for _ in range(6)
        ]
        self._mock_sponsor_set = set(self._mock_sponsors)

        for i, sponsor in enumerate(self._mock_sponsors):
            sponsor.get_name.return_value = "name_%d" % i

        self._sponsor_name_map = {
            sponsor.get_name(): sponsor for sponsor in self._mock_sponsors
        }

    def set_up_player_sponsor_inventory(self):
        self._player_sponsor_inventory_patcher = mock.patch(
            "splendor_sim.src.player.json_player_sponsor_inventory.player_sponsor_inventory.PlayerSponsorInventory"
            ".__init__",
            autospec=True,
        )
        self._mock_player_sponsor_inventory_init = (
            self._player_sponsor_inventory_patcher.start()
        )
        self.addCleanup(self._player_sponsor_inventory_patcher.stop)

    def setUp(self):
        self.set_up_validator()
        self.set_up_sponsors()
        self.set_up_player_sponsor_inventory()

        self._mock_json = {
            "sponsors": {sponsor.get_name() for sponsor in self._mock_sponsors}
        }

        self._mock_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True
        )
        self._mock_sponsor_reserve = mock.create_autospec(
            spec=i_sponsor_reserve.ISponsorReserve, spec_set=True
        )
        self._mock_sponsor_manager = mock.create_autospec(
            spec=i_sponsor_manager.ISponsorManager, spec_set=True
        )

        self._mock_game_state.get_sponsor_reserve.return_value = (
            self._mock_sponsor_reserve
        )
        self._mock_sponsor_reserve.get_sponsor_manager.return_value = (
            self._mock_sponsor_manager
        )

        self._mock_sponsor_manager.get_sponsor_by_name.side_effect = lambda name: self._sponsor_name_map[
            name
        ]
        self._mock_sponsor_manager.is_sponsor_in_manager_by_name.side_effect = (
            lambda name: name in self._sponsor_name_map
        )

    def test_json_player_sponsor_inventory_init(self):
        # Arrange
        # Act
        object_pointer = json_player_sponsor_inventory.JsonPlayerSponsorInventory(
            self._mock_sponsor_set
        )
        # Assert
        self._mock_player_sponsor_inventory_init.assert_called_once_with(
            object_pointer, self._mock_sponsor_set
        )

    def test_json_player_sponsor_inventory_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_player_sponsor_inventory.JsonPlayerSponsorInventory.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_player_sponsor_inventory_init.assert_called_once_with(
            object_pointer, self._mock_sponsor_set
        )

    def test_json_player_sponsor_inventory_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_sponsor_inventory.JsonPlayerSponsorInventory.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_player_sponsor_inventory_build_from_json_invalid_card_name_not_in_manager(
        self
    ):
        # Arrange
        self._mock_json["sponsors"].add("not a name in the manager")
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_player_sponsor_inventory.JsonPlayerSponsorInventory.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_player_sponsor_inventory_get_json_schema(self):
        # Arrange
        object_pointer = json_player_sponsor_inventory.JsonPlayerSponsorInventory.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Act
        # Assert
        self.assertEqual(
            object_pointer.get_json_schema(), json_schemas.JSON_PLAYER_SPONSOR_INVENTORY
        )

    def test_json_player_sponsor_inventory_get_json_schema_immutability(self):
        # Arrange
        object_pointer = json_player_sponsor_inventory.JsonPlayerSponsorInventory.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Act
        object_pointer.get_json_schema().pop(list(object_pointer.get_json_schema())[0])
        # Assert
        self.assertEqual(
            object_pointer.get_json_schema(), json_schemas.JSON_PLAYER_SPONSOR_INVENTORY
        )
