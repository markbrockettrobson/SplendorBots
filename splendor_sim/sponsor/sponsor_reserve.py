import abc
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve


class SponsorReserve(i_sponsor_reserve.ISponsorReserve):

    def __init__(
            self,
            sponsor_list: typing.List[i_sponsor.ISponsor]
    ):
        self._sponsor_list = set(sponsor_list)

    def get_remaining_sponsor_list(self) -> typing.List[i_sponsor.ISponsor]:
        return list(self._sponsor_list)

    def remove_sponsor(self, sponsor: i_sponsor.ISponsor) -> None:
        if sponsor not in self._sponsor_list:
            raise ValueError("sponsor not available in reserve")
        self._sponsor_list.remove(sponsor)
