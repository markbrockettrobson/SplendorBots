import unittest
import unittest.mock as mock

import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_payment_manager as i_payment_manager
import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.game_state.game_state as game_state


class TestGameState(unittest.TestCase):
    def setUp(self):
        self._mock_player_manager = mock.create_autospec(
            spec=i_player_manager.IPlayerManager, spec_set=True
        )
        self._mock_player_manager.to_json.return_value = {"mock player manager": "json"}

        self._mock_coin_reserve = mock.create_autospec(
            spec=i_coin_reserve.ICoinReserve, spec_set=True
        )
        self._mock_coin_reserve.to_json.return_value = {"mock coin reserve": "json"}

        self._mock_card_reserve = mock.create_autospec(
            spec=i_card_reserve.ICardReserve, spec_set=True
        )
        self._mock_card_reserve.to_json.return_value = {"mock card reserve": "json"}

        self._mock_sponsor_reserve = mock.create_autospec(
            spec=i_sponsor_reserve.ISponsorReserve, spec_set=True
        )
        self._mock_sponsor_reserve.to_json.return_value = {
            "mock sponsor reserve": "json"
        }

        self._mock_payment_manager = mock.create_autospec(
            spec=i_payment_manager.IPaymentManager, spec_set=True
        )

    def test_game_state_get_player_manager(self):
        # Arrange
        test_game_state = game_state.GameState(
            self._mock_player_manager,
            self._mock_coin_reserve,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_payment_manager,
        )
        # Act
        # Assert
        self.assertEqual(
            test_game_state.get_player_manager(), self._mock_player_manager
        )

    def test_game_state_get_coin_reserve(self):
        # Arrange
        test_game_state = game_state.GameState(
            self._mock_player_manager,
            self._mock_coin_reserve,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_payment_manager,
        )
        # Act
        # Assert
        self.assertEqual(test_game_state.get_coin_reserve(), self._mock_coin_reserve)

    def test_game_state_get_card_reserve(self):
        # Arrange
        test_game_state = game_state.GameState(
            self._mock_player_manager,
            self._mock_coin_reserve,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_payment_manager,
        )
        # Act
        # Assert
        self.assertEqual(test_game_state.get_card_reserve(), self._mock_card_reserve)

    def test_game_state_get_sponsor_reserve(self):
        # Arrange
        test_game_state = game_state.GameState(
            self._mock_player_manager,
            self._mock_coin_reserve,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_payment_manager,
        )
        # Act
        # Assert
        self.assertEqual(
            test_game_state.get_sponsor_reserve(), self._mock_sponsor_reserve
        )

    def test_game_state_get_payment_manager(self):
        # Arrange
        test_game_state = game_state.GameState(
            self._mock_player_manager,
            self._mock_coin_reserve,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_payment_manager,
        )
        # Act
        # Assert
        self.assertEqual(
            test_game_state.get_payment_manager(), self._mock_payment_manager
        )

    def test_game_state_to_json(self):
        # Arrange
        test_game_state = game_state.GameState(
            self._mock_player_manager,
            self._mock_coin_reserve,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_payment_manager,
        )
        # Act
        # Assert
        self.assertEqual(
            test_game_state.to_json(),
            {
                "player_manager": {"mock player manager": "json"},
                "coin_reserve": {"mock coin reserve": "json"},
                "card_reserve": {"mock card reserve": "json"},
                "sponsor_reserve": {"mock sponsor reserve": "json"},
            },
        )

    def test_game_state_to_json_complies_with_schema(self):
        # Arrange
        test_game_state = game_state.GameState(
            self._mock_player_manager,
            self._mock_coin_reserve,
            self._mock_card_reserve,
            self._mock_sponsor_reserve,
            self._mock_payment_manager,
        )
        test_json_validator = json_validator.JsonValidator(json_schemas.JSON_GAME_STATE)
        # Act
        # Assert
        self.assertTrue(test_json_validator.validate_json(test_game_state.to_json()))
