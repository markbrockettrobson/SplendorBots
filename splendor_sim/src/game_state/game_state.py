import abc

import splendor_sim.interfaces.player.i_player_manager as i_player_manager
import splendor_sim.interfaces.coin.i_coin_reserve as i_coin_reserve
import splendor_sim.interfaces.card.i_card_reserve as i_card_reserve
import splendor_sim.interfaces.sponsor.i_sponsor_reserve as i_sponsor_reserve


class GameState(abc.ABC):
    pass