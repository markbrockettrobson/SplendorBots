import splendor_sim.interfaces.data_types.i_coin_type as i_coin_type


class CoinType(i_coin_type.ICoinType):

    def __init__(self, name: str, total_number: int):
        assert total_number > 0

        self._name = name
        self._total_number = total_number

    def get_name(self) -> str:
        return self._name

    def get_total_number(self) -> int:
        return self._total_number
