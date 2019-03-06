import abc
import typing
import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.card.i_deck as i_deck


class ICardReserve(abc.ABC):
    @abc.abstractmethod
    def __init__(self, cards_on_sale: int, decks: typing.List[i_deck.IDeck]):
        """

        :param cards_on_sale:  the number of card of each tier to be sold
               <int>
        :param decks: the list of decks to sell cards from
               <typing.List[i_deck.IDeck]>
        """

    @abc.abstractmethod
    def get_cards_for_sale(self) -> typing.List[i_card.ICard]:
        """

        :return: the list of cards for sale in all tiers
                 <typing.List[i_card.ICard]>
        """

    @abc.abstractmethod
    def get_cards_for_sale_by_tier(self, tier: int) -> typing.List[i_card.ICard]:
        """

        :param tier: the tier of cards to consider
               <int>
        :return: the list of cards for sale in tiers
                 <typing.List[i_card.ICard]>
        """

    @abc.abstractmethod
    def remove_card(self, card: i_card.ICard) -> None:
        """

        :param card: the card to remove from sale
               <i_card.ICard>
        :return: None
        """

    @abc.abstractmethod
    def remove_top_of_deck(self, tier: int) -> i_card.ICard:
        """

        :param tier: the tier of cards to consider
               <int>
        :return: the card to removed from the deck
                 <i_card.ICard>
        """

    @abc.abstractmethod
    def get_remaining_cards(self) -> typing.Set[i_card.ICard]:
        """

        :return: a set of all cards remaining in the decks and on sale
                 <typing.Set[i_card.ICard]>
        """

    @abc.abstractmethod
    def get_remaining_cards_by_tier(self, tier: int) -> typing.Set[i_card.ICard]:
        """

        :param tier: tier: the tier of cards to consider
               <int>
        :return: a set of all cards remaining in the deck and on sale
                 <typing.Set[i_card.ICard]>
        """

    @abc.abstractmethod
    def get_number_of_remaining_cards(self) -> int:
        """

        :return: the number of cards remaining in any tier
                 <int>
        """

    @abc.abstractmethod
    def get_number_of_remaining_cards_by_tier(self, tier: int) -> int:
        """

        :param tier: tier: tier: the tier of cards to consider
               <int>
        :return: the number of cards remaining in tier
                 <int>
        """
