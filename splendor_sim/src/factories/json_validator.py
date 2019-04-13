import typing
import cerberus.validator as cerberus_validator

import splendor_sim.interfaces.factories.i_json_validator as i_json_validator


class JsonValidator(i_json_validator.IJsonValidator):
    @staticmethod
    def validate_json_schema(
            json: typing.Dict,
            schema: typing.Dict
    ) -> bool:
        validator = cerberus_validator.Validator(schema)
        return validator.validate(json)
