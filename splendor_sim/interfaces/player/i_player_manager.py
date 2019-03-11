import abc
import typing
import splendor_sim.interfaces.player.i_player as i_player


class IPlayerManager(abc.ABC):

    @abc.abstractmethod
    def __init__(self, player_set: typing.Set[i_player.IPlayer]):
        """

        :param player_set: a set of all players to manage
        """

    @abc.abstractmethod
    def get_player_set(self) -> typing.Set[i_player.IPlayer]:
        """

        :return: a set of all players in the manager
        """

    @abc.abstractmethod
    def get_current_player(self) -> i_player.IPlayer:
        """

        :return: the current player
        """

    @abc.abstractmethod
    def next_players_turn(self) -> i_player.IPlayer:
        """

        :return: move to the next player and return the new current player
        """

    @abc.abstractmethod
    def get_turn_number(self) -> int:
        """

        :return: return the turn number
        """
