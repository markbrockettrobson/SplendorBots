import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.sponsor.i_sponsor as i_sponsor


class Sponsor(i_sponsor.ISponsor):
    def __init__(
        self,
        name: str,
        victory_points: int,
        cost: typing.Dict[i_coin_type.ICoinType, int],
    ):
        self._name = name
        self._validate_victory_points(victory_points)
        self._validate_cost(cost)
        self._victory_points = victory_points
        self._cost = copy.copy(cost)

    @staticmethod
    def _validate_victory_points(victory_points: int):
        if victory_points < 1:
            raise ValueError("victory_points must be one or greater")

    @staticmethod
    def _validate_cost(cost: typing.Dict):
        seen_cards: typing.Set[i_coin_type.ICoinType] = set()
        for coin, amount in cost.items():
            if amount < 0:
                raise ValueError("coin type amount must be zero or greater")
            seen_cards.add(coin)
        if not seen_cards:
            raise ValueError("must have one or more coin types")

    def get_name(self) -> str:
        return self._name

    def get_victory_points(self) -> int:
        return self._victory_points

    def get_cost(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        return copy.copy(self._cost)

    def to_json(self) -> typing.Dict:
        return {
            "name": self._name,
            "victory_points": self._victory_points,
            "cost": [
                {"coin_name": coin.get_name(), "count": number}
                for coin, number in self._cost.items()
            ],
        }
