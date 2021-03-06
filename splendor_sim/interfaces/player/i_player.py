import abc
import typing

import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory


class IPlayer(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        name: str,
        coin_inventory: i_player_coin_inventory.IPlayerCoinInventory,
        card_inventory: i_player_card_inventory.IPlayerCardInventory,
        sponsor_inventory: i_player_sponsor_inventory.IPlayerSponsorInventory,
    ):
        """

        :param name: the name of the player
               <i_player_coin_inventory.IPlayerCoinInventory>
        :param coin_inventory: the coin inventory of the player
               <i_player_coin_inventory.IPlayerCoinInventory>
        :param card_inventory: the card inventory of the player
               <i_player_card_inventory.IPlayerCardInventory>
        :param sponsor_inventory: the sponsor inventory of the player
               <i_player_sponsor_inventory.IPlayerSponsorInventory>

        """

    @abc.abstractmethod
    def get_name(self) -> str:
        """

        :return: the name of a player
                 <str>
        """

    @abc.abstractmethod
    def get_coin_inventory(self) -> i_player_coin_inventory.IPlayerCoinInventory:
        """

        :return: the coin inventory of a player
                 <i_player_coin_inventory.IPlayerCoinInventory>
        """

    @abc.abstractmethod
    def get_card_inventory(self) -> i_player_card_inventory.IPlayerCardInventory:
        """

        :return: the card inventory of a player
                 <i_player_card_inventory.IPlayerCardInventory>
        """

    @abc.abstractmethod
    def get_sponsor_inventory(
        self
    ) -> i_player_sponsor_inventory.IPlayerSponsorInventory:
        """

        :return: the sponsor inventory of a player
                 <i_player_sponsor_inventory.IPlayerSponsorInventory>
        """

    @abc.abstractmethod
    def to_json(self) -> typing.Dict:
        """

        :return: a json dict of the player object
                 <typing.Dict>
        """
