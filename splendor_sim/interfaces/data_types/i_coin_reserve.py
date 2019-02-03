from abc import ABC, abstractmethod
from typing import List

from splendor_sim.interfaces.collection_rules.i_collection_rule import ICollectionRule


class ICoinReserve(ABC):

    def __init__(self, color_names: List[str], max_number_of_coin: int):
        pass

    def __str__(self) -> str:
        pass

    @abstractmethod
    def print_std_out(self):
        pass

    @abstractmethod
    def add_rule(self, rule: ICollectionRule):
        pass

    @abstractmethod
    def get_rules(self) -> List[ICollectionRule]:
        pass
