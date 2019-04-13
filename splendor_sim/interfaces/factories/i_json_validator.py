import abc
import typing


class IJsonValidator(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def validate_json_schema(
            json: typing.Dict,
            schema: typing.Dict
    ) -> bool:
        """

        :param json: the json dict
                 <typing.Dict>
        :param schema: the schema
                 <typing.Dict>
        :return: bool true if the dict conforms to the schema
                 <bool>
        """
