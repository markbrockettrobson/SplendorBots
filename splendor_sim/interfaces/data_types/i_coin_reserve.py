import abc
import typing

from splendor_sim.interfaces.collection_rules.i_collection_rule import ICollectionRule


class ICoinReserve(abc.ABC):
    @abc.abstractmethod
    def __init__(self,
                 color_names: typing.List[str],
                 max_number_of_coin: int):
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def print_std_out(self):
        pass

    @abc.abstractmethod
    def add_rule(self,
                 rule: ICollectionRule):
        pass

    @abc.abstractmethod
    def get_rules(self) -> typing.List[ICollectionRule]:
        pass
