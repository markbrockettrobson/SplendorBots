import abc
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_manager as i_sponsor_manager


class ISponsorReserve(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            sponsor_manager: i_sponsor_manager.ISponsorManager,
            sponsor_set: typing.Set[i_sponsor.ISponsor]
    ):
        """

        :param sponsor_manager: the manager holding all sponsors in the game
               <i_sponsor_manager.ISponsorManager>
        :param sponsor_set: the set of sponsors that can be acquired
               <typing.Set[i_sponsor.ISponsor]>
        """

    @abc.abstractmethod
    def get_sponsor_manager(
            self,
    ) -> i_sponsor_manager.ISponsorManager:
        """

        :return: the sponsor manager
                 <i_sponsor_manager.ISponsorManager>
        """

    @abc.abstractmethod
    def get_remaining_sponsor_set(self) -> typing.Set[i_sponsor.ISponsor]:
        """

        :return: a set of sponsors remaining in the reserve
                 <typing.Set[i_sponsor.ISponsor]>
        """

    @abc.abstractmethod
    def remove_sponsor(self, sponsor: i_sponsor.ISponsor) -> None:
        """

        :param sponsor: the sponsor to remove form the reserve
               <i_sponsor.ISponsor>
        :return: None
        """

    @abc.abstractmethod
    def to_json(self) -> typing.Dict:
        """

        :return: a json dict of the sponsor
                 <typing.Dict>
        """
