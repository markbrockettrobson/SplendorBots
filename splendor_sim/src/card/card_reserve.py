import copy
import typing

import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_card_manager as i_card_manager
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.card.i_deck as i_deck


class CardReserve(i_card_reserve.ICardReserve):
    def __init__(
        self,
        card_manager: i_card_manager.ICardManager,
        number_of_cards_on_sale: int,
        decks: typing.Set[i_deck.IDeck],
        cards_on_sale: typing.Set[i_card.ICard],
    ):
        self._card_manager = card_manager

        self._validate_cards_on_sale(number_of_cards_on_sale)
        self._validate_decks(decks)

        self._create_decks_by_tier(decks)

        self.number_of_cards_on_sale = number_of_cards_on_sale
        self._create_cards_on_sale(cards_on_sale)

    @staticmethod
    def _validate_cards_on_sale(number_of_cards_on_sale: int) -> None:
        if number_of_cards_on_sale <= 0:
            raise ValueError("Cards on sale must be one or more")

    @staticmethod
    def _validate_decks(decks: typing.Set[i_deck.IDeck]) -> None:
        if not decks:
            raise ValueError("must have one or more deck")

        tiers: typing.Set[int] = set()
        for deck in decks:
            if deck.get_tier() in tiers:
                raise ValueError("more than one deck has the same tier")
            tiers.add(deck.get_tier())

    def _create_decks_by_tier(self, decks: typing.Set[i_deck.IDeck]) -> None:
        self._decks_by_tier: typing.Dict[int,i_deck.IDeck] = {}
        for deck in decks:
            self._decks_by_tier[deck.get_tier()] = deck

    def _create_cards_on_sale(self, cards_on_sale: typing.Set[i_card.ICard]) -> None:
        self._cards_on_sale_by_tier: typing.Dict[int,typing.Set[i_card.ICard]] = (
            {}
        )

        for card in cards_on_sale:
            tier = card.get_tier()
            if tier not in self._cards_on_sale_by_tier:
                self._cards_on_sale_by_tier[tier] = set()
            self._cards_on_sale_by_tier[tier].add(card)

        for tier in self._cards_on_sale_by_tier:
            if len(self._cards_on_sale_by_tier[tier]) > self.number_of_cards_on_sale:
                raise ValueError("too many cards on sale")

        for tier in self._decks_by_tier:
            if tier not in self._cards_on_sale_by_tier:
                self._cards_on_sale_by_tier[tier] = set()
            while len(self._cards_on_sale_by_tier[tier]) < self.number_of_cards_on_sale:
                if self._decks_by_tier[tier].has_next():
                    self._cards_on_sale_by_tier[tier].add(
                        self._decks_by_tier[tier].next()
                    )
                else:
                    break

    def get_card_manager(self):
        return self._card_manager

    def get_cards_for_sale(self) -> typing.Set[i_card.ICard]:
        card_set: typing.Set[i_card.ICard] = set()
        for tier in self._cards_on_sale_by_tier:
            card_set = card_set.union(self._cards_on_sale_by_tier[tier])
        return card_set

    def get_cards_for_sale_by_tier(self, tier: int) -> typing.Set[i_card.ICard]:
        if tier not in self._cards_on_sale_by_tier:
            raise ValueError("unknown tier")
        return copy.copy(self._cards_on_sale_by_tier[tier])

    def remove_card(self, card: i_card.ICard):
        for tier in self._cards_on_sale_by_tier:
            if card in self._cards_on_sale_by_tier[tier]:
                self._cards_on_sale_by_tier[tier].remove(card)
                if self._decks_by_tier[tier].has_next():
                    self._cards_on_sale_by_tier[tier].add(
                        self._decks_by_tier[tier].next()
                    )
                return
        raise ValueError("card not for sale")

    def remove_top_of_deck(self, tier: int) -> i_card.ICard:
        if tier not in self._decks_by_tier:
            raise ValueError("unknown tier")
        deck = self._decks_by_tier[tier]
        if deck.has_next():
            return deck.next()
        raise ValueError("deck is empty")

    def get_remaining_cards(self) -> typing.Set[i_card.ICard]:
        total_cards: typing.Set[i_card.ICard] = set()
        for tier in self._decks_by_tier:
            total_cards = total_cards.union(
                self._decks_by_tier[tier].get_remaining_cards()
            )
        return total_cards

    def get_remaining_cards_by_tier(self, tier: int) -> typing.Set[i_card.ICard]:
        if tier not in self._decks_by_tier:
            raise ValueError("unknown tier")
        return copy.copy(self._decks_by_tier[tier].get_remaining_cards())

    def get_number_of_remaining_cards(self) -> int:
        total_cards = 0
        for tier in self._decks_by_tier:
            total_cards += self._decks_by_tier[tier].number_remaining_cards()
            total_cards += len(self._cards_on_sale_by_tier[tier])

        return total_cards

    def get_number_of_remaining_cards_by_tier(self, tier: int) -> int:
        if tier not in self._decks_by_tier:
            raise ValueError("unknown tier")
        return self._decks_by_tier[tier].number_remaining_cards() + len(
            self._cards_on_sale_by_tier[tier]
        )

    def to_json(self):
        return {
            "card_manager": self._card_manager.to_json(),
            "number_of_cards_on_sale": self.number_of_cards_on_sale,
            "decks": [deck.to_json() for deck in self._decks_by_tier.values()],
            "tiers": list(self._decks_by_tier.keys()),
            "cards_on_sale": [card.get_name() for card in self.get_cards_for_sale()],
        }
