import typing
import copy
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_deck as i_deck
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.card.i_card_manager as i_card_manager


class CardReserve(i_card_reserve.ICardReserve):
    def __init__(
            self,
            card_manager: i_card_manager.ICardManager,
            cards_on_sale: int,
            decks: typing.Set[i_deck.IDeck]
    ):
        self._card_manager = card_manager

        self._validate_cards_on_sale(cards_on_sale)
        self._validate_decks(decks)

        self._create_decks_by_tier(decks)

        self._cards_on_sale = cards_on_sale
        self._create_cards_on_sale()

    @staticmethod
    def _validate_cards_on_sale(cards_on_sale: int) -> None:
        if cards_on_sale <= 0:
            raise ValueError("Cards on sale must be one or more")

    @staticmethod
    def _validate_decks(decks: typing.Set[i_deck.IDeck]) -> None:
        if not decks:
            raise ValueError("must have one or more deck")

        tiers = set()  # type: typing.Set[int]
        for deck in decks:
            if deck.get_tier() in tiers:
                raise ValueError("more than one deck has the same tier")
            tiers.add(deck.get_tier())

    def _create_decks_by_tier(self, decks: typing.Set[i_deck.IDeck]) -> None:
        self._decks_by_tier = {}  # type: typing.Dict[int,i_deck.IDeck]
        for deck in decks:
            self._decks_by_tier[deck.get_tier()] = deck

    def _create_cards_on_sale(self) -> None:
        self._cards_on_sale_by_tier = {}  # type: typing.Dict[int,typing.Set[i_card.ICard]]
        for tier in self._decks_by_tier:
            self._cards_on_sale_by_tier[tier] = set()
            for _ in range(self._cards_on_sale):
                if self._decks_by_tier[tier].has_next():
                    self._cards_on_sale_by_tier[tier].add(self._decks_by_tier[tier].next())

    def get_card_manager(self):
        return self._card_manager

    def get_cards_for_sale(self) -> typing.Set[i_card.ICard]:
        card_set = set()  # type: typing.Set[i_card.ICard]
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
                    self._cards_on_sale_by_tier[tier].add(self._decks_by_tier[tier].next())
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
        total_cards = set()  # type: typing.Set[i_card.ICard]
        for tier in self._decks_by_tier:
            total_cards = total_cards.union(self._decks_by_tier[tier].get_remaining_cards())
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
        return self._decks_by_tier[tier].number_remaining_cards() + len(self._cards_on_sale_by_tier[tier])

    def to_json(self):
        return {
            "card_manager": self._card_manager.to_json(),
            "number_of_cards_on_sale": self._cards_on_sale,
            "decks": [
                deck.to_json() for deck in self._decks_by_tier.values()
            ],
            "tiers": self._decks_by_tier.keys(),
            "cards_on_sale": [
                {
                    "tier": tier,
                    "cards": [
                        card.get_name() for card in self._cards_on_sale_by_tier[tier]
                    ]
                }
                for tier in self._decks_by_tier
            ]
        }
