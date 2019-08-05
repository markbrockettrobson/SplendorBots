import abc
import typing

import splendor_sim.interfaces.player.i_player as i_player


class IPlayerManager(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        player_list: typing.List[i_player.IPlayer],
        current_player: i_player.IPlayer,
        turn_number: int,
    ):
        """

        :param player_list: a set of all players to manage
        :param current_player: the current player
        :param turn_number: the number of turns that have passed
        """

    @abc.abstractmethod
    def get_player_list(self) -> typing.List[i_player.IPlayer]:
        """

        :return: a list of all players in the manager in turn order
                 <typing.List[i_player.IPlayer]>
        """

    @abc.abstractmethod
    def get_player_set(self) -> typing.Set[i_player.IPlayer]:
        """

        :return: a set of all players in the manager
                 <typing.Set[i_player.IPlayer]>
        """

    @abc.abstractmethod
    def get_current_player(self) -> i_player.IPlayer:
        """

        :return: the current player
                 <i_player.IPlayer>
        """

    @abc.abstractmethod
    def next_players_turn(self) -> i_player.IPlayer:
        """

        :return: move to the next player and return the new current player
                 <i_player.IPlayer>
        """

    @abc.abstractmethod
    def get_turn_number(self) -> int:
        """

        :return: return the turn number
                 <int>
        """

    @abc.abstractmethod
    def to_json(self) -> typing.Dict:
        """

        :return: a json dict of the player manager object
                 <typing.Dict>
        """
