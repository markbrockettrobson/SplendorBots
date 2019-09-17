import copy
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.sponsor.i_sponsor_manager as i_sponsor_manager


class SponsorManager(i_sponsor_manager.ISponsorManager):
    def __init__(self, sponsor_set: typing.Set[i_sponsor.ISponsor]):

        self._sponsor_set = copy.copy(sponsor_set)
        self._name_map: typing.Dict[str, i_sponsor.ISponsor] = {}
        for sponsor in sponsor_set:
            if sponsor.get_name() in self._name_map:
                raise ValueError(
                    "manager can not have more then one sponsor with the same name."
                )
            self._name_map[sponsor.get_name()] = sponsor

    def get_sponsor_set(self) -> typing.Set[i_sponsor.ISponsor]:
        return copy.copy(self._sponsor_set)

    def get_sponsor_by_name(self, name: str) -> i_sponsor.ISponsor:
        if name not in self._name_map:
            raise ValueError("no sponsor with that name.")
        return self._name_map[name]

    def is_sponsor_in_manager_by_name(self, name: str) -> bool:
        return name in self._name_map

    def to_json(self) -> typing.Dict:
        return {"sponsors": [sponsor.to_json() for sponsor in self._sponsor_set]}
