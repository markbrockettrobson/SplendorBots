import unittest

import splendor_sim.src.factories.json_validator as json_validator


class TestJsonValidator(unittest.TestCase):
    def setUp(self):
        self._schema = {
            'name': {
                'type': 'string'
            },
            'age': {
                'type': 'integer',
                'min': 10,
                'required': True,
            }
        }

        self._json = {
            'name': 'mark',
            'age': 10
        }

    def test_validate_json(self):
        # Arrange
        test_json_validator = json_validator.JsonValidator(self._schema)
        # Act
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(self._json)
        )

    def test_validate_json_true_missing_non_required_field(self):
        # Arrange
        self._json = {
            'age': 10
        }
        test_json_validator = json_validator.JsonValidator(self._schema)
        # Act
        # Assert
        self.assertTrue(
            test_json_validator.validate_json(self._json)
        )

    def test_validate_json_false_incorrect_type(self):
        # Arrange
        self._json = {
            'name': 'mark',
            'age': '10'
        }
        test_json_validator = json_validator.JsonValidator(self._schema)
        # Act
        # Assert
        self.assertFalse(
            test_json_validator.validate_json(self._json)
        )

    def test_validate_json_false_missing_required_field(self):
        # Arrange
        self._json = {
            'name': 'mark'
        }
        test_json_validator = json_validator.JsonValidator(self._schema)
        # Act
        # Assert
        self.assertFalse(
            test_json_validator.validate_json(self._json)
        )
