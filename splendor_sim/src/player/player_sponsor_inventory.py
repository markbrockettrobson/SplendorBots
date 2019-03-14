import copy
import typing

import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory


class PlayerSponsorInventory(i_player_sponsor_inventory.IPlayerSponsorInventory):

    def __init__(self):
        self._sponsors = set()
        self._total_victory_points = 0

    def get_sponsor_set(self) -> typing.Set[i_sponsor.ISponsor]:
        return copy.copy(self._sponsors)

    def add_sponsor(self, sponsor: i_sponsor.ISponsor):
        if sponsor in self._sponsors:
            raise ValueError("sponsor already in inventory")
        self._sponsors.add(sponsor)
        self._total_victory_points += sponsor.get_victory_points()

    def get_total_victory_points(self) -> int:
        return self._total_victory_points
