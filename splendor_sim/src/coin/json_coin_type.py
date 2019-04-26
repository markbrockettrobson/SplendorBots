import copy
import typing

import splendor_sim.interfaces.factories.i_json_buildable_object as i_json_buildable_object
import splendor_sim.src.factories.json_validator as json_validator
import splendor_sim.src.factories.json_schemas as json_schemas
import splendor_sim.src.coin.coin_type as coin_type


class JsonCoinType(coin_type.CoinType, i_json_buildable_object.IJsonBuildableObject):

    _JSON_VALIDATOR = json_validator.JsonValidator(json_schemas.JSON_COIN_TYPE_SCHEMA)

    def __init__(self, name: str, total_number: int):
        super(JsonCoinType, self).__init__(name, total_number)

    @classmethod
    def build_from_json(
            cls,
            json: typing.Dict
    ):
        if not cls._JSON_VALIDATOR.validate_json(json):
            raise ValueError("Json does not meet schema")
        return cls(
            json['name'],
            json['total_number']
        )

    @staticmethod
    def get_json_schema() -> typing.Dict:
        return copy.deepcopy(json_schemas.JSON_COIN_TYPE_SCHEMA)
