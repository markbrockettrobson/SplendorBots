import abc
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor


class ISponsorReserve(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            sponsor_list: typing.List[i_sponsor.ISponsor]
    ):
        """

        :param sponsor_list: the list of sponsors that can be acquired
               <typing.List[i_sponsor.ISponsor]>
        """

    @abc.abstractmethod
    def get_remaining_sponsor_list(self) -> typing.List[i_sponsor.ISponsor]:
        """

        :return: a list of sponsors remaining in the reserve
                 <typing.List[i_sponsor.ISponsor]>
        """

    @abc.abstractmethod
    def remove_sponsor(self, sponsor: i_sponsor.ISponsor) -> None:
        """

        :param sponsor: the sponsor to remove form the reserve
               <i_sponsor.ISponsor>
        :return: None
        """
