import abc
import typing

import splendor_sim.interfaces.card.i_card as i_card


class IDeck(abc.ABC):
    @abc.abstractmethod
    def __init__(self, tier: int, card_set: typing.Set[i_card.ICard]):
        """

        :param tier: the tier of the deck
               <int>
        :param card_set: the list of cards in the deck
               <typing.Set[i_card.ICard]>
        """

    @abc.abstractmethod
    def get_tier(self) -> int:
        """

        :return: tier
                 <int>
        """

    @abc.abstractmethod
    def has_next(self) -> bool:
        """

        :return: true if the deck has one or more cards
                 <bool>
        """

    @abc.abstractmethod
    def next(self) -> i_card.ICard:
        """
        side effect the card is removed from the deck
        :return: the top most card from the deck
                 <i_card.ICard>
        """

    @abc.abstractmethod
    def number_remaining_cards(self) -> int:
        """

        :return: the number of remaining cards in the deck
                 <int>
        """

    @abc.abstractmethod
    def get_remaining_cards(self) -> typing.Set[i_card.ICard]:
        """

        :return: a list of all cards left in the deck
                 <typing.set[i_card.ICard]>
        """
