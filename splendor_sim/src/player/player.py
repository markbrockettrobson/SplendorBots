import splendor_sim.interfaces.player.i_player as i_player
import splendor_sim.interfaces.player.i_player_coin_inventory as i_player_coin_inventory
import splendor_sim.interfaces.player.i_player_card_inventory as i_player_card_inventory
import splendor_sim.interfaces.player.i_player_sponsor_inventory as i_player_sponsor_inventory


class Player(i_player.IPlayer):

    def __init__(self,
                 coin_inventory: i_player_coin_inventory.IPlayerCoinInventory,
                 card_inventory: i_player_card_inventory.IPlayerCardInventory,
                 sponsor_inventory: i_player_sponsor_inventory.IPlayerSponsorInventory):
        self._coin_inventory = coin_inventory
        self._card_inventory = card_inventory
        self._sponsor_inventory = sponsor_inventory

    def get_coin_inventory(self) -> i_player_coin_inventory.IPlayerCoinInventory:
        return self._coin_inventory

    def get_card_inventory(self) -> i_player_card_inventory.IPlayerCardInventory:
        return self._card_inventory

    def get_sponsor_inventory(self) -> i_player_sponsor_inventory.IPlayerSponsorInventory:
        return self._sponsor_inventory
