import abc
import typing
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_deck as i_deck


class ICardReserve(abc.ABC):
    @abc.abstractmethod
    def __init__(self, cards_on_sale: int ,decks: typing.List[i_deck.IDeck]):
        pass

    @abc.abstractmethod
    def get_cards_for_sale(self) -> typing.List[i_card.ICard]:
        pass

    @abc.abstractmethod
    def get_cards_for_sale_by_tier(self, tier: int) -> typing.List[i_card.ICard]:
        pass

    @abc.abstractmethod
    def remove_card(self, card: i_card.ICard):
        pass

    @abc.abstractmethod
    def remove_top_of_deck(self, tier: int) -> i_card.ICard:
        pass

    @abc.abstractmethod
    def get_remaining_cards(self) -> typing.Set[i_card.ICard]:
        pass

    @abc.abstractmethod
    def get_remaining_cards_by_tier(self, tier: int) -> typing.Set[i_card.ICard]:
        pass

    @abc.abstractmethod
    def get_number_of_remaining_cards(self) -> int:
        pass

    @abc.abstractmethod
    def get_number_of_remaining_cards_by_tier(self, tier: int) -> int:
        pass
