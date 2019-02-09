import abc


class ICoinType(abc.ABC):
    @abc.abstractmethod
    def __init__(self,
                 coin_id: int,
                 long_name: str,
                 short_name: str,
                 color_name: str,
                 is_wildcard: bool):
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def get_coin_id(self) -> int:
        pass

    @abc.abstractmethod
    def get_long_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_short_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_color_name(self) -> str:
        pass

    @abc.abstractmethod
    def is_wildcard(self) -> bool:
        pass
