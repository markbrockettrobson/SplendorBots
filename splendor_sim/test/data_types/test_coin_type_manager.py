import unittest
import unittest.mock as mock
import splendor_sim.data_types.coin_type as coin_type


class TestCoinTypeManager(unittest.TestCase):

    def setUp(self):
        self._mock_coin_type_list = [mock.create_autospec(spec=coin_type.CoinType, spec_set=True) for _ in range(6)]
