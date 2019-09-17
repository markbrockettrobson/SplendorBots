import copy
import typing

import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.coin.i_payment_manager as i_payment_manager
import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.json_player_manager as json_player_manager
import splendor_sim.src.card.json_card_reserve as json_card_reserve
import splendor_sim.src.coin.json_coin_reserve as json_coin_reserve
import splendor_sim.src.coin.payment_manager as payment_manager
import splendor_sim.src.sponsor.json_sponsor_reserve as json_sponsor_reserve
import splendor_sim.src.game_state.game_state as game_state


class JsonGameState(game_state.GameState, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_GAME_STATE)

    def __init__(
        self,
        player_manager: i_player_manager.IPlayerManager,
        coin_reserve: i_coin_reserve.ICoinReserve,
        card_reserve: i_card_reserve.ICardReserve,
        sponsor_reserve: i_sponsor_reserve.ISponsorReserve,
        coin_payment_manager: i_payment_manager.IPaymentManager,
    ):
        super(JsonGameState, self).__init__(
            player_manager,
            coin_reserve,
            card_reserve,
            sponsor_reserve,
            coin_payment_manager,
        )

    @classmethod
    def build_from_json(
        cls,
        json: typing.Dict,
        incomplete_game_state: i_incomplete_game_state.IIncompleteGameState,
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        coin_reserve = json_coin_reserve.JsonCoinReserve.build_from_json(
            json["coin_reserve"], incomplete_game_state
        )
        incomplete_game_state.set_coin_reserve(coin_reserve)

        card_reserve = json_card_reserve.JsonCardReserve.build_from_json(
            json["card_reserve"], incomplete_game_state
        )
        incomplete_game_state.set_card_reserve(card_reserve)

        sponsor_reserve = json_sponsor_reserve.JsonSponsorReserve.build_from_json(
            json["sponsor_reserve"], incomplete_game_state
        )
        incomplete_game_state.set_sponsor_reserve(sponsor_reserve)

        player_manager = json_player_manager.JsonPlayerManager.build_from_json(
            json["player_manager"], incomplete_game_state
        )
        incomplete_game_state.set_player_manager(player_manager)

        coin_payment_manager = payment_manager.PaymentManager(
            coin_reserve.get_manager()
        )

        json_game_state = cls(
            player_manager,
            coin_reserve,
            card_reserve,
            sponsor_reserve,
            coin_payment_manager,
        )
        return json_game_state

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_GAME_STATE)
