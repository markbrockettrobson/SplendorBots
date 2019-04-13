import abc
import typing


class IJsonValidator(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def validate_json_schema(
            json: typing.Dict,
            schema: typing.Dict
    ) -> bool:
        pass
