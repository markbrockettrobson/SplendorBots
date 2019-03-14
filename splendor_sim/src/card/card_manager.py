import typing
import copy
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_card_manager as i_card_manager


class CardManager(i_card_manager.ICardManager):
    def __init__(
            self,
            card_set: typing.Set[i_card.ICard]
    ):

        self._card_set = copy.copy(card_set)
        self._cards_by_tier = self._sort_cards_by_tier(self._card_set)

    def get_tiers(self) -> typing.Set[int]:
        return set(self._cards_by_tier.keys())

    def get_card_set(self) -> typing.Set[i_card.ICard]:
        return copy.copy(self._card_set)

    def get_card_tier(self, tier: int) -> typing.Set[i_card.ICard]:
        if tier not in self._cards_by_tier:
            raise ValueError("tier " + str(tier) + " has no cards")
        return copy.copy(self._cards_by_tier[tier])

    @staticmethod
    def _sort_cards_by_tier(card_set: typing.Set[i_card.ICard]) -> typing.Dict[int, typing.Set[i_card.ICard]]:
        cards_by_tier = {}  # type: typing.Dict[int, typing.Set[i_card.ICard]]
        for card in card_set:
            tier = card.get_tier()
            if tier not in cards_by_tier:
                cards_by_tier[tier] = set()
            cards_by_tier[tier].add(card)
        return cards_by_tier
