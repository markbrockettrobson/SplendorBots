import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_manager as i_sponsor_manager
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.sponsor.json_sponsor_reserve as json_sponsor_reserve


class TestJsonSponsorReserve(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            "splendor_sim.src.sponsor.json_sponsor_reserve.JsonSponsorReserve._JSON_VALIDATOR",
            autospec=True,
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._sponsor_reserve_patcher = mock.patch(
            "splendor_sim.src.sponsor.sponsor_reserve.SponsorReserve.__init__",
            autospec=True,
        )
        self._mock_sponsor_reserve = self._sponsor_reserve_patcher.start()
        self.addCleanup(self._sponsor_reserve_patcher.stop)

        self._json_sponsor_manager_patcher = mock.patch(
            "splendor_sim.src.sponsor.json_sponsor_manager.JsonSponsorManager",
            autospec=True,
        )
        self._mock_json_sponsor_manager = self._json_sponsor_manager_patcher.start()
        self.addCleanup(self._json_sponsor_manager_patcher.stop)

        self._mock_sponsors = {
            mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True)
            for _ in range(10)
        }

        for i, sponsor in enumerate(self._mock_sponsors):
            sponsor.get_name.return_value = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]

        self._mock_sponsor_name_map = {
            sponsor.get_name(): sponsor for sponsor in self._mock_sponsors
        }
        self._mock_sponsors_manager = mock.create_autospec(
            spec=i_sponsor_manager.ISponsorManager, spec_set=True
        )
        self._mock_sponsors_manager.is_sponsor_in_manager_by_name.side_effect = (
            lambda x: x in self._mock_sponsor_name_map.keys()
        )
        self._mock_sponsors_manager.get_sponsor_by_name.side_effect = lambda x: self._mock_sponsor_name_map[
            x
        ]

        self._mock_json_sponsor_manager.build_from_json.return_value = (
            self._mock_sponsors_manager
        )

        self._mock_json = {
            "sponsor_manager": {"mock": "json"},
            "sponsors": [sponsor.get_name() for sponsor in self._mock_sponsors],
        }

        self._mock_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True
        )

    def test_json_sponsor_reserve_init(self):
        # Arrange
        # Act
        object_pointer = json_sponsor_reserve.JsonSponsorReserve(
            self._mock_sponsors_manager, self._mock_sponsors
        )
        # Assert
        self._mock_sponsor_reserve.assert_called_once_with(
            object_pointer, self._mock_sponsors_manager, self._mock_sponsors
        )

    def test_json_sponsor_reserve_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_sponsor_reserve.JsonSponsorReserve.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Assert
        self._mock_json_sponsor_manager.build_from_json.assert_called_once_with(
            {"mock": "json"}, self._mock_game_state
        )

        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_sponsor_reserve.assert_called_once_with(
            object_pointer, self._mock_sponsors_manager, self._mock_sponsors
        )

    def test_json_sponsor_reserve_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_sponsor_reserve.JsonSponsorReserve.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_sponsor_reserve_build_from_json_unknown_sponsor(self):
        # Arrange
        self._mock_json["sponsors"].append("unknown")
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_sponsor_reserve.JsonSponsorReserve.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_sponsor_reserve_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_SPONSOR_RESERVE_SCHEMA,
            json_sponsor_reserve.JsonSponsorReserve.get_json_schema(),
        )

    def test_json_sponsor_reserve_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_sponsor_reserve.JsonSponsorReserve.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_SPONSOR_RESERVE_SCHEMA,
            json_sponsor_reserve.JsonSponsorReserve.get_json_schema(),
        )
