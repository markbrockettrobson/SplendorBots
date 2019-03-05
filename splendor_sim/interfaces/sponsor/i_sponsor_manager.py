import abc
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor


class ISponsorManager(abc.ABC):
    @abc.abstractmethod
    def __init__(self,
                 seed: int,
                 number_of_sponsors: int,
                 sponsor_list: typing.List[i_sponsor.ISponsor]):
        """

        :param seed: the seed for the RNG
        :param number_of_sponsors: the number of sponsors to select
        :param sponsor_list: the list of sponsors that can be selected
        """

    @abc.abstractmethod
    def get_sponsor_list(self) -> typing.List[i_sponsor.ISponsor]:
        """

        :return: the selected sponsors in a list
        """
