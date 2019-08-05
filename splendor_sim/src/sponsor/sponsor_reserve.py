import copy
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_manager as i_sponsor_manager
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve


class SponsorReserve(i_sponsor_reserve.ISponsorReserve):
    def __init__(
        self,
        sponsor_manager: i_sponsor_manager.ISponsorManager,
        sponsor_set: typing.Set[i_sponsor.ISponsor],
    ):
        self._sponsor_manager = sponsor_manager
        manager_set = self._sponsor_manager.get_sponsor_set()
        for sponsor in sponsor_set:
            if sponsor not in manager_set:
                raise ValueError("sponsor not in manager")

        self._sponsor_set = copy.copy(sponsor_set)

    def get_sponsor_manager(self) -> i_sponsor_manager.ISponsorManager:
        return self._sponsor_manager

    def get_remaining_sponsor_set(self) -> typing.Set[i_sponsor.ISponsor]:
        return copy.copy(self._sponsor_set)

    def remove_sponsor(self, sponsor: i_sponsor.ISponsor) -> None:
        if sponsor not in self._sponsor_set:
            raise ValueError("sponsor not available in reserve")
        self._sponsor_set.remove(sponsor)

    def to_json(self):
        return {
            "sponsor_manager": self._sponsor_manager.to_json(),
            "sponsors": [sponsor.get_name() for sponsor in self._sponsor_set],
        }
