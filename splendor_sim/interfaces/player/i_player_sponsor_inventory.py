import abc
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor


class IPlayerSponsorInventory(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_sponsor_list(self) -> typing.List[i_sponsor.ISponsor]:
        """

        :return: a list of all sponsors in the inventory
                 <typing.List[i_sponsor.ISponsor]>
        """

    @abc.abstractmethod
    def add_sponsor(self, sponsor: i_sponsor.ISponsor):
        """

        :param sponsor: the sponsor to add
               <i_sponsor.ISponsor>
        :return: None
        """

    @abc.abstractmethod
    def get_total_victory_points(self) -> int:
        """

        :return: the total number of victory_points that the payer would have from the sponsors in this inventory
                 <int>
        """
