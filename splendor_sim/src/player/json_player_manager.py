import copy
import typing

import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state
import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.player.json_player as json_player
import splendor_sim.src.player.player_manager as player_manager


class JsonPlayerManager(
    player_manager.PlayerManager, i_json_buildable_object.IJsonBuildableObject
):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_PLAYER_MANAGER)

    def __init__(
        self,
        player_list: typing.List[i_player.IPlayer],
        current_player: i_player.IPlayer,
        turn_number: int = 1,
    ):
        super(JsonPlayerManager, self).__init__(
            player_list, current_player, turn_number
        )

    @classmethod
    def build_from_json(
        cls,
        json: typing.Dict,
        incomplete_game_state: i_incomplete_game_state.IIncompleteGameState,
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")

        player_list = [
            json_player.JsonPlayer.build_from_json(player_json, incomplete_game_state)
            for player_json in json["players"]
        ]
        current_players = [
            player
            for player in player_list
            if player.get_name() == json["current_player"]
        ]
        turn_number = json["turn_number"]

        if len(current_players) != 1:
            raise ValueError("current player not in list of players")

        json_player_manager = cls(player_list, current_players[0], turn_number)
        return json_player_manager

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_PLAYER_MANAGER)
