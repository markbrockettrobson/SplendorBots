import abc
import typing


class ICollectionRule(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def is_valid(self,
                 requested_coins: typing.List[int],
                 current_reserves: typing.List[int]) -> bool:
        pass

    @abc.abstractmethod
    def get_description(self) -> str:
        pass
