import abc
import typing

import splendor_sim.interfaces.card.i_card as i_card
import splendor_sim.interfaces.coin.i_coin_type as i_coin_type


class IPlayerCardInventory(abc.ABC):

    @abc.abstractmethod
    def __init__(
            self,
            max_reserved_cards: int,
            reserved_cards: typing.Set[i_card.ICard],
            cards: typing.Set[i_card.ICard]
    ):
        """

        :param max_reserved_cards: the max number of cards the player can reserve
               <int>
        """

    @abc.abstractmethod
    def get_max_number_of_reserved_cards(self) -> int:
        """

        :return: the number of cards reserved
                 <int>
        """

    @abc.abstractmethod
    def get_number_of_reserved_cards(self) -> int:
        """

        :return: the number of cards reserved
                 <int>
        """

    @abc.abstractmethod
    def add_card(self, card: i_card.ICard) -> None:
        """

        :param card: the card to add to the inventory
               <i_card.ICard>
        :return: None
        """

    @abc.abstractmethod
    def add_card_to_reserved(self, card: i_card.ICard) -> None:
        """

        :param card: the card to reserve
               <i_card.ICard>
        :return: None
        """

    @abc.abstractmethod
    def get_total_discount(self) -> typing.Dict[i_coin_type.ICoinType, int]:

        """

        :return: the total discount from cards
                 <typing.Dict[i_coin_type.ICoinType, int]>
        """

    @abc.abstractmethod
    def get_victory_points(self) -> int:

        """

        :return: the number of victory points in total
                 <int>
        """

    @abc.abstractmethod
    def get_card_set(self) -> typing.Set[i_card.ICard]:

        """

        :return: a set of all cards the player owns
                 <typing.Set[i_card.ICard]>
        """

    @abc.abstractmethod
    def get_reserved_card_set(self) -> typing.Set[i_card.ICard]:

        """

        :return: set of all cards in reserve
                 <typing.Set[i_card.ICard]>
        """

    @abc.abstractmethod
    def remove_from_reserved_card_set(self, card: i_card.ICard) -> None:
        """

        :param card: the card to be removed from the card set
               <i_card.ICard>
        :return: None
        """

    @abc.abstractmethod
    def to_json(self) -> typing.Dict:
        """

        :return: a json dict of the player card inventory object
                 <typing.Dict>
        """
