import abc
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor


class ISponsorReserve(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            sponsor_set: typing.Set[i_sponsor.ISponsor]
    ):
        """

        :param sponsor_set: the set of sponsors that can be acquired
               <typing.Set[i_sponsor.ISponsor]>
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
