from abc import ABC, abstractmethod


class ICollectionRule(ABC):

    def __init__(self):
        pass

    def __str__(self) -> str:
        pass

    @abstractmethod
    def is_valid(self, requested_coins, current_reserves) -> bool:
        pass

    def get_description(self) -> str:
        pass
