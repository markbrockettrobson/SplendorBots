import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.card.i_card as i_card


class Card(i_card.ICard):
    _DEFAULT_NAME_FORMAT = "T%d_D%s_V%d_C%s"

    def __init__(
            self,
            tier: int,
            victory_points: int,
            discount: i_coin_type.ICoinType,
            cost: typing.Dict[i_coin_type.ICoinType, int],
            name: str = None
    ):
        self._validate_tier(tier)
        self._validate_victory_points(victory_points)
        self._validate_cost(cost)

        self._tier = tier
        self._victory_points = victory_points
        self._discount = discount
        self._cost = copy.copy(cost)
        self._name: str
        if not name:
            self._name = self._create_default_name()
        else:
            self._name = name

    def get_tier(self) -> int:
        return self._tier

    def get_victory_points(self) -> int:
        return self._victory_points

    def get_discount(self) -> i_coin_type.ICoinType:
        return self._discount

    def get_cost(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        return copy.copy(self._cost)

    def get_name(self) -> str:
        return self._name

    @staticmethod
    def _validate_tier(level: int) -> None:
        if level <= 0:
            raise ValueError("level must be greater than 0")

    @staticmethod
    def _validate_victory_points(victory_points: int) -> None:
        if victory_points < 0:
            raise ValueError("victory_points must be greater than or equal to 0")

    @staticmethod
    def _validate_cost(cost: typing.Dict[i_coin_type.ICoinType, int]) -> None:
        for _, value in cost.items():
            if value < 0:
                raise ValueError("costs must be greater than or equal to 0")

    def _create_default_name(self):
        cost_string_builder = []
        for coin, value in self._cost.items():
            cost_string_builder.append("%s%d" % (coin.get_name(), value))

        return Card._DEFAULT_NAME_FORMAT % (
            self._tier,
            self._discount.get_name(),
            self._victory_points,
            "".join(cost_string_builder)
        )
