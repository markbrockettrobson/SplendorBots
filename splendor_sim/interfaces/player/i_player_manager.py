import abc
import typing
import splendor_sim.interfaces.player.i_player as i_player


class IPlayer(abc.ABC):

    @abc.abstractmethod
    def __init__(self, player_list: typing.Set[i_player.IPlayer]):
        """

        :param player_list:
        """

    @abc.abstractmethod
    def get_player_set(self):
        """

        :return:
        """

    @abc.abstractmethod
    def get_current_player(self):
        """

        :return:
        """

    @abc.abstractmethod
    def next_players_turn(self):
        """

        :return:
        """

    @abc.abstractmethod
    def get_turn_number(self):
        """

        :return:
        """