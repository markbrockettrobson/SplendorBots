import abc
import typing


class IJsonValidator(abc.ABC):
    @abc.abstractmethod
    def __init__(self, schema: typing.Dict):
        """

        :param schema: the schema to validate against
                 <typing.Dict>
        """

    @abc.abstractmethod
    def validate_json(self, json: typing.Dict) -> bool:
        """

        :param json: the json dict
                 <typing.Dict>
        :return: bool true if the dict conforms to the schema
                 <bool>
        """
