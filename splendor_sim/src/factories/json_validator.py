import typing

import cerberus.validator as validator

import splendor_sim.interfaces.factories.i_json_validator as i_json_validator


class JsonValidator(i_json_validator.IJsonValidator):
    def __init__(self, schema: typing.Dict):
        self._schema = schema
        self._validator = validator.Validator(schema)

    def validate_json(
            self,
            json: typing.Dict
    ) -> bool:
        return self._validator.validate(json)
