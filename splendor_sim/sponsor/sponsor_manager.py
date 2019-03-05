import typing
import random
import copy
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_manager as i_sponsor_manager


class SponsorManager(i_sponsor_manager.ISponsorManager):

    def __init__(self,
                 seed: int,
                 number_of_sponsors: int,
                 sponsor_list: typing.List[i_sponsor.ISponsor]):
        random.seed(seed)

        if len(sponsor_list) < number_of_sponsors:
            raise ValueError("has less sponsors then number_of_sponsors")

        self._number_of_sponsors = number_of_sponsors
        self._sponsor_list = random.sample(sponsor_list, self._number_of_sponsors)

    def get_sponsor_list(self) -> typing.List[i_sponsor.ISponsor]:
        return copy.copy(self._sponsor_list)
