import unittest
import unittest.mock as mock

import splendor_sim.src.factories.json_validator as json_validator


class TestJsonValidator(unittest.TestCase):
    def setUp(self):
        self._validator_patcher = mock.patch('cerberus.validator', spec=True)
        self._mock_validator = self._validator_patcher.start()
        self.addCleanup(self._validator_patcher.stop)

        self._schema = {
            'name': {
                'type': 'string'
            },
            'age': {
                'type': 'string',
                'min': 10
            }
        }

        self._json = {
            'name': 'mark',
            'age': '10'
        }

    def test_validate_json_schema(self):
        # Arrange
        # Act
        # Assert
        self.assertTrue(
            json_validator.JsonValidator.validate_json_schema(
                self._json,
                self._schema
            )
        )

    def test_validate_json_schema_false(self):
        # Arrange
        self._json = {
            'name': 'mark',
            'age': 10
        }
        # Act
        # Assert
        self.assertFalse(
            json_validator.JsonValidator.validate_json_schema(
                self._json,
                self._schema
            )
        )
