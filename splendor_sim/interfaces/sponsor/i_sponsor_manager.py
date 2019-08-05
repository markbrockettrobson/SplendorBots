import abc
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor


class ISponsorManager(abc.ABC):
    @abc.abstractmethod
    def __init__(self, sponsor_set: typing.Set[i_sponsor.ISponsor]):
        """

        :param sponsor_set: the set of sponsors that can be selected
               <typing.Set[i_sponsor.ISponsor]>
        """

    @abc.abstractmethod
    def get_sponsor_set(self) -> typing.Set[i_sponsor.ISponsor]:
        """

        :return: the selected sponsors in a set
                 <typing.Set[i_sponsor.ISponsor]>
        """

    @abc.abstractmethod
    def get_sponsor_by_name(self, name: str) -> i_sponsor.ISponsor:
        """

        :param name: the nam,e to select
        :return: the sponsor with that name
        """

    @abc.abstractmethod
    def is_sponsor_in_manager_by_name(self, name: str) -> bool:
        """

        :param name: the nam,e to select
        :return: true if the sponsor has a name
        """

    @abc.abstractmethod
    def to_json(self) -> typing.Dict:
        """

        :return: a json dict of the sponsor
                 <typing.Dict>
        """
