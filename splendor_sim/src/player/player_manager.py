import copy
import typing

import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.player.i_player_manager as i_player_manager


class PlayerManager(i_player_manager.IPlayerManager):
    def __init__(
        self,
        player_list: typing.List[i_player.IPlayer],
        current_player: i_player.IPlayer,
        turn_number: int = 1,
    ):
        name_set: typing.Set[str] = set()
        for player in player_list:
            if player.get_name() in name_set:
                raise ValueError("Two players can not have the same name.")
            name_set.add(player.get_name())

        if current_player not in player_list:
            raise ValueError("Current player not in player_list.")
        if turn_number < 1:
            raise ValueError("Turn number must be greater than zero.")

        self._player_list = copy.copy(player_list)
        self._player_set = set(player_list)
        self._number_of_players = len(self._player_set)
        self._turn_number = turn_number
        self._current_player = self._player_list.index(current_player)

    def get_player_list(self) -> typing.List[i_player.IPlayer]:
        return copy.copy(self._player_list)

    def get_player_set(self) -> typing.Set[i_player.IPlayer]:
        return copy.copy(self._player_set)

    def get_current_player(self) -> i_player.IPlayer:
        return self._player_list[self._current_player]

    def next_players_turn(self) -> i_player.IPlayer:
        if (
            self._current_player % (self._number_of_players - 1) == 0
            and self._current_player != 0
        ):
            self._turn_number += 1
            self._current_player = 0
        else:
            self._current_player += 1
        return self.get_current_player()

    def get_turn_number(self) -> int:
        return self._turn_number

    def to_json(self) -> typing.Dict:
        return {
            "players": [player.to_json() for player in self._player_list],
            "current_player": self._player_list[self._current_player].get_name(),
            "turn_number": self._turn_number,
        }
