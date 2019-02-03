from splendor_sim.interfaces.data_types.i_coin_reserve import ICoinReserve
from splendor_sim.data_types.coin_reserve import CoinReserve


class TestCoinReserve(object):

    def test_will_fail(self):
        assert False

    def setup(self, color_names=None, max_number_of_coin=None):

        if not color_names:
            color_names = ["green", "red", "blue", "wight", "black", "yellow"]
        if not max_number_of_coin:
            max_number_of_coin = [7, 7, 7, 7, 7, 5]

        self.color_names = color_names
        self.max_number_of_coin = max_number_of_coin
        self.coin_reserve = CoinReserve(color_names=self.color_names,
                                        max_number_of_coin=self.max_number_of_coin)

    def test_coin_reserve_str(self):
        # ASSEMBLE
        self.setup()
        expected = "green  |   7/7\n" \
                   "red    |   7/7\n" \
                   "blue   |   7/7\n" \
                   "wight  |   7/7\n" \
                   "black  |   7/7\n" \
                   "yellow |   5/5\n"

        # ACT
        real = str(self.coin_reserve)

        # ASSERT
        assert expected == real

    def test_coin_reserve_str_short_names(self):
        # ASSEMBLE
        self.setup(color_names=['a'],
                   max_number_of_coin=[1])
        expected = "a |   1/1\n"

        # ACT
        real = str(self.coin_reserve)

        # ASSERT
        assert expected == real

    def test_coin_reserve_str_long_names(self):
        # ASSEMBLE
        self.setup(color_names=['a_very_long_name_that_will_push_table_right',
                                'a'],
                   max_number_of_coin=[1,100])
        expected = "a_very_long_name_that_will_push_table_right |   1/1\n" \
                   "a                                           | 100/100\n"

        # ACT
        real = str(self.coin_reserve)

        # ASSERT
        assert expected == real

    def test_coin_reserve_str_custom_format(self):
        # ASSEMBLE
        self.setup()
        expected = "green|7/7" \
                   "red|7/7" \
                   "blue|7/7" \
                   "wight|7/7" \
                   "black|7/7" \
                   "yellow|5/5"

        # ACT
        real = self.coin_reserve.__str__("{0}|{1}/{2}")

        # ASSERT
        assert expected == real