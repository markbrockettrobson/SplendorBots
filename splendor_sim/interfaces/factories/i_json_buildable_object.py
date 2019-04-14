import abc
import typing


class IJsonBuildableObject(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def build_from_json(
            cls,
            json: typing.Dict
    ):
        """

        :param json: json dict to build the project from
               <typing.Dict>
        :return: The object built from the json
        """

    @staticmethod
    @abc.abstractmethod
    def get_json_schema() -> typing.Dict:
        """

        :return: the schema used to validate that the json has all needed fields
                 <typing.Dict>
        """
