import copy
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.card.i_card as i_card


class Card(i_card.ICoinType):
    def __init__(self,
                 level: int,
                 victory_points: int,
                 discount: i_coin_type.ICoinType,
                 cost: typing.Dict[i_coin_type.ICoinType, int]):
        self._validate_level(level)
        self._validate_victory_points(victory_points)
        self._validate_cost(cost)

        self._level = level
        self._victory_points = victory_points
        self._discount = discount
        self._cost = cost

    def get_level(self) -> int:
        return self._level

    def get_victory_points(self) -> int:
        return self._victory_points

    def get_discount(self) -> i_coin_type.ICoinType:
        return self._discount

    def get_cost(self) -> typing.Dict[i_coin_type.ICoinType, int]:
        return copy.copy(self._cost)

    @staticmethod
    def _validate_level(level: int) -> None:
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
