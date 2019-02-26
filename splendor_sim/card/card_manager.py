import typing
import copy
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manger
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_card_manager as i_card_manager


class CardManager(i_card_manager.ICardManager):
    def __init__(self,
                 card_list: typing.List[i_card.ICard],
                 coin_type_manger: i_coin_type_manger.ICoinTypeManager):
        self._coin_type_manger = coin_type_manger
        self._coin_type_list = self._coin_type_manger.get_coin_list()
        self._validate_card_list(card_list, self._coin_type_list)

        self._card_list = copy.copy(card_list)
        self._cards_by_tier = self._sort_cards_by_tier(self._card_list)

    def get_tiers(self) -> typing.List[int]:
        return list(self._cards_by_tier.keys())

    def get_card_list(self) -> typing.List[i_card.ICard]:
        return copy.copy(self._card_list)

    def get_card_tier(self, tier: int) -> typing.List[i_card.ICard]:
        if tier not in self._cards_by_tier:
            raise ValueError("tier " + str(tier) + " has no cards")
        return copy.copy(self._cards_by_tier[tier])

    @staticmethod
    def _validate_card_list(card_list: typing.List[i_card.ICard],
                            coin_type_list: typing.List[i_coin_type.ICoinType]) -> None:
        for card in card_list:
            if card.get_discount() not in coin_type_list:
                raise ValueError("card " + str(card) + " has a unknown discount")
            for cost in card.get_cost().keys():
                if cost not in coin_type_list:
                    raise ValueError("card " + str(card) + " has a unknown cost")

    @staticmethod
    def _sort_cards_by_tier(card_list: typing.List[i_card.ICard]) -> typing.Dict[int, typing.List[i_card.ICard]]:
        cards_by_tier = {}  # type: typing.Dict[int, typing.List[i_card.ICard]]
        for card in card_list:
            tier = card.get_tier()
            if tier not in cards_by_tier:
                cards_by_tier[tier] = []
            cards_by_tier[tier].append(card)
        return cards_by_tier
