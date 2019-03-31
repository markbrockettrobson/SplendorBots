import abc

import splendor_sim.interfaces.game_state.i_game_state as i_game_state


class IAction(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def validate(self, game_state: i_game_state.IGameState) -> bool:
        pass

    @abc.abstractmethod
    def execute(self, game_state: i_game_state.IGameState) -> None:
        pass

    # todo report_changes
