import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.sponsor.json_sponsor_manager as json_sponsor_manager


class TestJsonSponsorManager(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch(
            "splendor_sim.src.sponsor.json_sponsor_manager.JsonSponsorManager._JSON_VALIDATOR",
            autospec=True,
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

        self._sponsor_manager_patcher = mock.patch(
            "splendor_sim.src.sponsor.sponsor_manager.SponsorManager.__init__",
            autospec=True,
        )
        self._mock_sponsor_manager = self._sponsor_manager_patcher.start()
        self.addCleanup(self._sponsor_manager_patcher.stop)

        self._json_sponsor_patcher = mock.patch(
            "splendor_sim.src.sponsor.json_sponsor.JsonSponsor", autospec=True
        )
        self._mock_json_sponsor = self._json_sponsor_patcher.start()
        self.addCleanup(self._json_sponsor_patcher.stop)

        self._mock_sponsors = {
            mock.create_autospec(spec=i_sponsor.ISponsor, spec_set=True)
            for _ in range(10)
        }
        self._mock_json_sponsor.build_from_json.side_effect = self._mock_sponsors

        self._mock_json = {"sponsors": [{"mock": "json %d" % i} for i in range(10)]}

        self._mock_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True
        )

    def test_json_sponsor_manager_init(self):
        # Arrange
        # Act
        object_pointer = json_sponsor_manager.JsonSponsorManager(self._mock_sponsors)
        # Assert
        self._mock_sponsor_manager.assert_called_once_with(
            object_pointer, self._mock_sponsors
        )

    def test_json_sponsor_manager_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_sponsor_manager.JsonSponsorManager.build_from_json(
            self._mock_json, self._mock_game_state
        )
        # Assert
        self._mock_json_sponsor.build_from_json.assert_has_calls(
            [
                mock.call({"mock": "json %d" % i}, self._mock_game_state)
                for i in range(10)
            ]
        )

        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_sponsor_manager.assert_called_once_with(
            object_pointer, self._mock_sponsors
        )

    def test_json_sponsor_manager_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_sponsor_manager.JsonSponsorManager.build_from_json(
                self._mock_json, self._mock_game_state
            )

    def test_json_sponsor_manager_get_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertEqual(
            json_schemas.JSON_SPONSOR_MANAGER_SCHEMA,
            json_sponsor_manager.JsonSponsorManager.get_json_schema(),
        )

    def test_json_sponsor_manager_get_json_schema_immutability(self):
        # Arrange
        pre_mutation = json_sponsor_manager.JsonSponsorManager.get_json_schema()
        # Act
        pre_mutation.pop(list(pre_mutation.keys())[0])
        # Assert
        self.assertEqual(
            json_schemas.JSON_SPONSOR_MANAGER_SCHEMA,
            json_sponsor_manager.JsonSponsorManager.get_json_schema(),
        )
