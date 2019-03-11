import copy
import typing
import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.player.i_player_manager as i_player_manager


class PlayerManager(i_player_manager.IPlayerManager):

    def __init__(self, player_set: typing.Set[i_player.IPlayer]):
        self._player_list = list(player_set)
        self._player_set = copy.copy(player_set)
        self._number_of_players = len(self._player_set)
        self._turn_number = 1
        self._current_player = 0

    def get_player_set(self) -> typing.Set[i_player.IPlayer]:
        return copy.copy(self._player_set)

    def get_current_player(self) -> i_player.IPlayer:
        return self._player_list[self._current_player]

    def next_players_turn(self) -> i_player.IPlayer:
        if self._current_player % (self._number_of_players-1) == 0 and not self._current_player == 0:
            self._turn_number += 1
            self._current_player = 0
        else:
            self._current_player += 1
        return self.get_current_player()

    def get_turn_number(self) -> int:
        return self._turn_number
