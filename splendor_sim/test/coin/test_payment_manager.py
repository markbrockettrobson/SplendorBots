import unittest
import unittest.mock as mock

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.src.coin.payment_manager as payment_manager


class TestPaymentManager(unittest.TestCase):

    def setUp(self):
        self._mock_coin_type_set = {mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True) for _ in range(5)}
        self._mock_coin_type_list = list(self._mock_coin_type_set)
        self._mock_cost = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 3
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 3
        }
        self._mock_discount = {}
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]: {self._mock_coin_type_list[0]},
            self._mock_coin_type_list[1]: {self._mock_coin_type_list[1]},
            self._mock_coin_type_list[2]: {self._mock_coin_type_list[2]},
            self._mock_coin_type_list[3]: {self._mock_coin_type_list[3]},
            self._mock_coin_type_list[4]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3],
                    self._mock_coin_type_list[4]
                }
        }
        self._mock_coin_type_manager = mock.create_autospec(spec=i_coin_type_manager.ICoinTypeManager, spec_set=True)
        self._mock_coin_type_manager.get_coin_usage.side_effect = lambda coin: self._mock_coin_usage[coin]
        self._mock_coin_type_manager.get_coin_set.return_value = self._mock_coin_type_set
        self._test_payment_manager = payment_manager.PaymentManager(self._mock_coin_type_manager)

    def test_payment_manager_validate_valid_payment_single_coin_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 1
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 1
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_multiple_coins_of_one_type_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 3
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 3
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_multiple_coins_true(self):
        # Arrange
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_wildcard_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 3
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[4]: 1
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_multiple_wildcard_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 1,
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[2]: 1,
            self._mock_coin_type_list[3]: 1,
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
        }
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3]

                },
            self._mock_coin_type_list[1]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1]
                },
            self._mock_coin_type_list[2]: {self._mock_coin_type_list[2]},
            self._mock_coin_type_list[3]: {self._mock_coin_type_list[3]},
            self._mock_coin_type_list[4]: {self._mock_coin_type_list[4]}
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_cycle_wildcard_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 4,
            self._mock_coin_type_list[1]: 4,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[3]: 2,
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[3]: 7,
        }
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1],
                    self._mock_coin_type_list[2]
                },
            self._mock_coin_type_list[1]: {self._mock_coin_type_list[1]},
            self._mock_coin_type_list[2]:
                {
                    self._mock_coin_type_list[1],
                    self._mock_coin_type_list[2]
                },
            self._mock_coin_type_list[3]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3]
                },
            self._mock_coin_type_list[4]: {self._mock_coin_type_list[4]}
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_single_coin_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 1
        }
        self._mock_payment = {
            self._mock_coin_type_list[1]: 1
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_multiple_coins_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[2]: 3,
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_wildcard_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 3
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[4]: 1
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_multiple_wildcard_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 1,
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[2]: 1,
            self._mock_coin_type_list[3]: 1,
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
        }
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3]

                },
            self._mock_coin_type_list[1]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1]
                },
            self._mock_coin_type_list[2]: {self._mock_coin_type_list[2]},
            self._mock_coin_type_list[3]: {self._mock_coin_type_list[3]},
            self._mock_coin_type_list[4]: {self._mock_coin_type_list[4]}
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_cycle_wildcard_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 4,
            self._mock_coin_type_list[1]: 4,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[3]: 2,
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[3]: 7,
        }
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[2]
                },
            self._mock_coin_type_list[1]: {self._mock_coin_type_list[1]},
            self._mock_coin_type_list[2]: {self._mock_coin_type_list[2]},
            self._mock_coin_type_list[3]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3]
                },
            self._mock_coin_type_list[4]: {self._mock_coin_type_list[4]}
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_over_pay_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 1
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_under_pay_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 3
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_multiple_coins_of_one_type_discount_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 3
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 1
        }
        self._mock_discount = {
            self._mock_coin_type_list[0]: 2
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_multiple_coins_discount_true(self):
        # Arrange
        self._mock_payment = {
            self._mock_coin_type_list[0]: 1,
            self._mock_coin_type_list[2]: 3
        }
        self._mock_discount = {
            self._mock_coin_type_list[0]: 1,
            self._mock_coin_type_list[1]: 2
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_wildcard_discount_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 3,
            self._mock_coin_type_list[2]: 5
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[4]: 1
        }
        self._mock_discount = {
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[2]: 2
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_multiple_wildcard_discount_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 1,
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[3]: 1,
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
        }
        self._mock_discount = {
            self._mock_coin_type_list[2]: 1
        }
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3]

                },
            self._mock_coin_type_list[1]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1]
                },
            self._mock_coin_type_list[2]: {self._mock_coin_type_list[2]},
            self._mock_coin_type_list[3]: {self._mock_coin_type_list[3]},
            self._mock_coin_type_list[4]: {self._mock_coin_type_list[4]}
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_cycle_wildcard_discount_true(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 15,
            self._mock_coin_type_list[1]: 5,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[3]: 3,
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[3]: 7,
        }
        self._mock_discount = {
            self._mock_coin_type_list[0]: 11,
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[3]: 1
        }
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1],
                    self._mock_coin_type_list[2]
                },
            self._mock_coin_type_list[1]: {self._mock_coin_type_list[1]},
            self._mock_coin_type_list[2]:
                {
                    self._mock_coin_type_list[1],
                    self._mock_coin_type_list[2]
                },
            self._mock_coin_type_list[3]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3]
                },
            self._mock_coin_type_list[4]: {self._mock_coin_type_list[4]}
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_single_coin_discount_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 1
        }
        self._mock_payment = {
            self._mock_coin_type_list[1]: 1
        }
        self._mock_discount = {
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[3]: 1
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_multiple_coins_discount_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[2]: 3,
        }
        self._mock_discount = {
            self._mock_coin_type_list[0]: 1
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_wildcard_discount_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[1]: 3,
            self._mock_coin_type_list[2]: 3
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[4]: 1
        }
        self._mock_discount = {
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[3]: 10
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_multiple_wildcard_discount_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 1,
            self._mock_coin_type_list[1]: 1,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[3]: 2,
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2,
            self._mock_coin_type_list[1]: 2,
        }
        self._mock_discount = {
            self._mock_coin_type_list[2]: 1,
            self._mock_coin_type_list[3]: 1
        }
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3]

                },
            self._mock_coin_type_list[1]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[1]
                },
            self._mock_coin_type_list[2]: {self._mock_coin_type_list[2]},
            self._mock_coin_type_list[3]: {self._mock_coin_type_list[3]},
            self._mock_coin_type_list[4]: {self._mock_coin_type_list[4]}
        }
        # Act
        # Assert
        self.assertTrue(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_payment_cycle_wildcard_discount_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 4,
            self._mock_coin_type_list[1]: 9,
            self._mock_coin_type_list[2]: 4,
            self._mock_coin_type_list[3]: 2,
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 3,
            self._mock_coin_type_list[1]: 2,
            self._mock_coin_type_list[2]: 2,
            self._mock_coin_type_list[3]: 7,
        }
        self._mock_discount = {
            self._mock_coin_type_list[1]: 5,
            self._mock_coin_type_list[3]: 1
        }
        self._mock_coin_usage = {
            self._mock_coin_type_list[0]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[2]
                },
            self._mock_coin_type_list[1]: {self._mock_coin_type_list[1]},
            self._mock_coin_type_list[2]: {self._mock_coin_type_list[2]},
            self._mock_coin_type_list[3]:
                {
                    self._mock_coin_type_list[0],
                    self._mock_coin_type_list[2],
                    self._mock_coin_type_list[3]
                },
            self._mock_coin_type_list[4]: {self._mock_coin_type_list[4]}
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_over_pay_discount_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 2
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2
        }
        self._mock_discount = {
            self._mock_coin_type_list[0]: 1,
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_valid_under_pay_discount_false(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: 6
        }
        self._mock_payment = {
            self._mock_coin_type_list[0]: 2
        }
        self._mock_discount = {
            self._mock_coin_type_list[0]: 3
        }
        # Act
        # Assert
        self.assertFalse(
            self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
        )

    def test_payment_manager_validate_invalid_payment_negative(self):
        # Arrange
        self._mock_payment = {
            self._mock_coin_type_list[0]: -1
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )

    def test_payment_manager_validate_invalid_payment_unknown_coin(self):
        # Arrange
        self._mock_payment = {
            mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True): 2
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )

    def test_payment_manager_validate_invalid_cost(self):
        # Arrange
        self._mock_cost = {
            self._mock_coin_type_list[0]: -1
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )

    def test_payment_manager_validate_invalid_coin_unknown_coin(self):
        # Arrange
        self._mock_cost = {
            mock.create_autospec(spec=i_coin_type.ICoinType, spec_set=True): 2
        }
        # Act
        # Assert
        with self.assertRaises(ValueError):
            _ = self._test_payment_manager.validate_payment(
                self._mock_cost,
                self._mock_payment,
                self._mock_discount
            )
