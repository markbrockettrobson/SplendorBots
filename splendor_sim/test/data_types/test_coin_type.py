import unittest
from splendor_sim.data_types.coin_type import CoinType


# todo type checking


class TestCoinReserve(unittest.TestCase):

    def setUp(self):
        self._coin_id = 1
        self._long_name = "red coin"
        self._short_name = "r"
        self._color_name = "red"
        self._is_wildcard = False

    def create_coin_type(self):
        self._coin_type = CoinType(
            self._coin_id,
            self._long_name,
            self._short_name,
            self._color_name,
            self._is_wildcard
        )

    def test_get_coin_id(self):
        # ASSEMBLE
        self.create_coin_type()
        expected = self._coin_id
        # ACT
        real = self._coin_type.get_coin_id()
        # ASSERT
        self.assertEqual(expected, real)

    def test_get_long_name(self):
        # ASSEMBLE
        self.create_coin_type()
        expected = self._long_name
        # ACT
        real = self._coin_type.get_long_name()
        # ASSERT
        self.assertEqual(expected, real)

    def test_get_short_name(self):
        # ASSEMBLE
        self.create_coin_type()
        expected = self._short_name
        # ACT
        real = self._coin_type.get_short_name()
        # ASSERT
        self.assertEqual(expected, real)

    def test_get_color_name(self):
        # ASSEMBLE
        self.create_coin_type()
        expected = self._color_name
        # ACT
        real = self._coin_type.get_color_name()
        # ASSERT
        self.assertEqual(expected, real)

    def test_is_wildcard(self):
        # ASSEMBLE
        self.create_coin_type()
        expected = self._is_wildcard
        # ACT
        real = self._coin_type.is_wildcard()
        # ASSERT
        self.assertEqual(expected, real)
