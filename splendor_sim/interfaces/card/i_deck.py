import abc
import typing

import splendor_sim.interfaces.card.i_card as i_card


class IDeck(abc.ABC):
    @abc.abstractmethod
    def __init__(self, card_list: typing.List[i_card.ICard]):
        """

        :param card_list: the list of cards in the deck
        """

    @abc.abstractmethod
    def has_next(self) -> bool:
        """

        :return: true if the deck has one or more cards
        """

    @abc.abstractmethod
    def next(self) -> i_card.ICard:
        """
        side effect the card is removed from the deck
        :return: the top most card from the deck
        """

    @abc.abstractmethod
    def number_remaining_cards(self) -> int:
        """

        :return: the number of remaining cards in the deck
        """
