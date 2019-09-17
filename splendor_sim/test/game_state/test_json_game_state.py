import unittest
import unittest.mock as mock

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.src.factories.json_schemas as json_schemas

import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve
import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.coin.i_payment_manager as i_payment_manager
import splendor_sim.src.game_state.json_game_state as json_game_state


class TestJsonGameState(unittest.TestCase):
    def set_up_validator(self):
        self._validator_patcher = mock.patch(
            "splendor_sim.src.game_state.json_game_state.JsonGameState._JSON_VALIDATOR",
            autospec=True,
        )
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)
        self._mock_validator.validate_json.return_value = True

    def set_up_coin_reserve(self):
        self._json_coin_reserve_patcher = mock.patch(
            "splendor_sim.src.game_state.json_game_state.json_coin_reserve.JsonCoinReserve",
            autospec=True,
        )
        self._mock_coin_reserve_init = self._json_coin_reserve_patcher.start()
        self.addCleanup(self._json_coin_reserve_patcher.stop)
        self._mock_coin_reserve = mock.create_autospec(
            spec=i_coin_reserve.ICoinReserve, spec_set=True
        )
        self._mock_coin_reserve_init.build_from_json.return_value = (
            self._mock_coin_reserve
        )
        self._mock_coin_type_manager = mock.create_autospec(
            spec=i_coin_type_manager.ICoinTypeManager, spec_set=True
        )
        self._mock_coin_reserve.get_manager.return_value = self._mock_coin_type_manager

    def set_up_card_reserve(self):
        self._json_card_reserve_patcher = mock.patch(
            "splendor_sim.src.game_state.json_game_state.json_card_reserve.JsonCardReserve",
            autospec=True,
        )
        self._mock_card_reserve_init = self._json_card_reserve_patcher.start()
        self.addCleanup(self._json_card_reserve_patcher.stop)
        self._mock_card_reserve = mock.create_autospec(
            spec=i_card_reserve.ICardReserve, spec_set=True
        )
        self._mock_card_reserve_init.build_from_json.return_value = (
            self._mock_card_reserve
        )

    def set_up_sponsor_reserve(self):
        self._json_sponsor_reserve_patcher = mock.patch(
            "splendor_sim.src.game_state.json_game_state.json_sponsor_reserve.JsonSponsorReserve",
            autospec=True,
        )
        self._mock_sponsor_reserve_init = self._json_sponsor_reserve_patcher.start()
        self.addCleanup(self._json_sponsor_reserve_patcher.stop)
        self._mock_sponsor_reserve = mock.create_autospec(
            spec=i_sponsor_reserve.ISponsorReserve, spec_set=True
        )
        self._mock_sponsor_reserve_init.build_from_json.return_value = (
            self._mock_sponsor_reserve
        )

    def set_up_player_manager(self):
        self._json_player_manager_patcher = mock.patch(
            "splendor_sim.src.game_state.json_game_state.json_player_manager.JsonPlayerManager",
            autospec=True,
        )
        self._mock_player_manager_init = self._json_player_manager_patcher.start()
        self.addCleanup(self._json_player_manager_patcher.stop)
        self._mock_player_manager = mock.create_autospec(
            spec=i_player_manager.IPlayerManager, spec_set=True
        )
        self._mock_player_manager_init.build_from_json.return_value = (
            self._mock_player_manager
        )

    def set_up_payment_manager(self):
        self._json_payment_manager_patcher = mock.patch(
            "splendor_sim.src.game_state.json_game_state.payment_manager.PaymentManager",
            autospec=True,
        )
        self._mock_payment_manager_init = self._json_payment_manager_patcher.start()
        self.addCleanup(self._json_payment_manager_patcher.stop)
        self._mock_payment_manager = mock.create_autospec(
            spec=i_payment_manager.IPaymentManager, spec_set=True
        )
        self._mock_payment_manager_init.return_value = self._mock_payment_manager

    def setUp(self):

        self._game_state_patcher = mock.patch(
            "splendor_sim.src.game_state.json_game_state.game_state.GameState.__init__",
            autospec=True,
        )
        self._mock_game_state = self._game_state_patcher.start()
        self.addCleanup(self._game_state_patcher.stop)

        self.set_up_validator()
        self.set_up_coin_reserve()
        self.set_up_card_reserve()
        self.set_up_sponsor_reserve()
        self.set_up_player_manager()
        self.set_up_payment_manager()

        self._mock_json = {
            "player_manager": {"mock player manager": "json"},
            "coin_reserve": {"mock coin reserve": "json"},
            "card_reserve": {"mock card reserve": "json"},
            "sponsor_reserve": {"mock sponsor reserve": "json"},
        }

        self._mock_incomplete_game_state = mock.create_autospec(
            spec=i_incomplete_game_state.IIncompleteGameState, spec_set=True
        )

    def test_json_game_state_init(self):
        # Arrange
        # Act
        object_pointer = json_game_state.JsonGameState(
            self._mock_player_manager,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_player_manager,
            self._mock_payment_manager,
        )
        # Assert
        self._mock_game_state.assert_called_once_with(
            object_pointer,
            self._mock_player_manager,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_player_manager,
            self._mock_payment_manager,
        )

    def test_json_game_state_build_from_json_valid(self):
        # Arrange
        # Act
        object_pointer = json_game_state.JsonGameState.build_from_json(
            self._mock_json, self._mock_incomplete_game_state
        )
        # Assert
        self._mock_validator.validate_json.assert_called_once_with(self._mock_json)
        self._mock_game_state.assert_called_once_with(
            object_pointer,
            self._mock_player_manager,
            self._mock_coin_reserve,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_payment_manager,
        )

        self._mock_player_manager_init.build_from_json.assert_called_once_with(
            {"mock player manager": "json"}, self._mock_incomplete_game_state
        )
        self._mock_coin_reserve_init.build_from_json.assert_called_once_with(
            {"mock coin reserve": "json"}, self._mock_incomplete_game_state
        )
        self._mock_card_reserve_init.build_from_json.assert_called_once_with(
            {"mock card reserve": "json"}, self._mock_incomplete_game_state
        )
        self._mock_sponsor_reserve_init.build_from_json.assert_called_once_with(
            {"mock sponsor reserve": "json"}, self._mock_incomplete_game_state
        )

        self._mock_payment_manager_init.assert_called_once_with(
            self._mock_coin_type_manager
        )

    def test_json_game_state_build_from_json_invalid(self):
        # Arrange
        self._mock_validator.validate_json.return_value = False
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = json_game_state.JsonGameState.build_from_json(
                self._mock_json, self._mock_incomplete_game_state
            )

    def test_json_game_state_get_json_schema(self):
        # Arrange
        object_pointer = json_game_state.JsonGameState(
            self._mock_player_manager,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_player_manager,
            self._mock_payment_manager,
        )
        # Act
        # Assert
        self.assertEqual(object_pointer.get_json_schema(), json_schemas.JSON_GAME_STATE)

    def test_json_player_sponsor_inventory_get_json_schema_immutability(self):
        # Arrange
        object_pointer = json_game_state.JsonGameState(
            self._mock_player_manager,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_player_manager,
            self._mock_payment_manager,
        )
        # Act
        object_pointer.get_json_schema().pop(list(object_pointer.get_json_schema())[0])
        # Assert
        self.assertEqual(object_pointer.get_json_schema(), json_schemas.JSON_GAME_STATE)
