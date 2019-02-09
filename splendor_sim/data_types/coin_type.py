from splendor_sim.interfaces.data_types.i_coin_type import ICoinType
# todo document this


class CoinType(ICoinType):

    def __init__(self,
                 coin_id: int,
                 long_name: str,
                 short_name: str,
                 color_name: str,
                 is_wildcard: bool):
        self._coin_id = coin_id
        self._long_name = long_name
        self._short_name = short_name
        self._color_name = color_name
        self._is_wildcard = is_wildcard

    def __str__(self) -> str:
        return self.get_long_name()

    def get_coin_id(self) -> int:
        return self._coin_id

    def get_long_name(self) -> str:
        return self._long_name

    def get_short_name(self) -> str:
        return self._short_name

    def get_color_name(self) -> str:
        return self._color_name

    def is_wildcard(self) -> bool:
        return self._is_wildcard
