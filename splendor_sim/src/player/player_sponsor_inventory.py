import copy
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory


class PlayerSponsorInventory(i_player_sponsor_inventory.IPlayerSponsorInventory):

    def __init__(self, sponsors: typing.Set[i_sponsor.ISponsor]):
        self._sponsors: typing.Set[i_sponsor.ISponsor] = set()
        self._total_victory_points = 0
        for sponsor in sponsors:
            self.add_sponsor(sponsor)

    def get_sponsor_set(self) -> typing.Set[i_sponsor.ISponsor]:
        return copy.copy(self._sponsors)

    def add_sponsor(self, sponsor: i_sponsor.ISponsor):
        if sponsor in self._sponsors:
            raise ValueError("sponsor already in inventory")
        self._sponsors.add(sponsor)
        self._total_victory_points += sponsor.get_victory_points()

    def get_total_victory_points(self) -> int:
        return self._total_victory_points

    def to_json(self) -> typing.Dict:
        return {
            'sponsors': [sponsor.get_name() for sponsor in self._sponsors]
        }
