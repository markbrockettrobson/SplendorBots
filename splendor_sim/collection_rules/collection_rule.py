import typing

from splendor_sim.interfaces.collection_rules.i_collection_rule import ICollectionRule


class CollectionRule(ICollectionRule):
    _description = 'CollectionRule super class'

    def __init__(self):
        pass

    def __str__(self) -> str:
        return self._description

    def is_valid(self,
                 requested_coins: typing.List[int],
                 current_reserves: typing.List[int]) -> bool:

        return False

    def get_description(self) -> str:
        return self._description
