import abc
import typing

import splendor_sim.interfaces.game_state.i_incomplete_game_state as i_incomplete_game_state


class IJsonBuildableObject(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def build_from_json(
        cls,
        json: typing.Dict,
        incomplete_game_state: i_incomplete_game_state.IIncompleteGameState,
    ):
        """

        :param json: json dict to build the project from
               <typing.Dict>
        :param incomplete_game_state: a incomplete game state object
               <i_game_state.IGameState>
        :return: The object built from the json
        """

    @staticmethod
    @abc.abstractmethod
    def get_json_schema() -> typing.Dict:
        """

        :return: the schema used to validate that the json has all needed fields
                 <typing.Dict>
        """

    @abc.abstractmethod
    def to_json(self) -> typing.Dict:
        """

        :return: a json dict of the object
                 <typing.Dict>
        """
