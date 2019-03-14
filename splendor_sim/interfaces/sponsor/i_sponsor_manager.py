import abc
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor


class ISponsorManager(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            seed: int,
            number_of_sponsors: int,
            sponsor_set: typing.Set[i_sponsor.ISponsor]
    ):
        """

        :param seed: the seed for the RNG
               <int>
        :param number_of_sponsors: the number of sponsors to select
               <int>
        :param sponsor_set: the set of sponsors that can be selected
               <typing.Set[i_sponsor.ISponsor]>
        """

    @abc.abstractmethod
    def get_sponsor_set(self) -> typing.Set[i_sponsor.ISponsor]:
        """

        :return: the selected sponsors in a set
                 <typing.Set[i_sponsor.ISponsor]>
        """
