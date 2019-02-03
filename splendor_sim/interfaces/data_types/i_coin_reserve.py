from abc import ABC, abstractmethod
from typing import List


class ICoinReserve(ABC):

    def __init__(self, color_names: List[str], max_number_of_coin: int):
        super(ICoinReserve, self).__init__()

    def __str__(self) -> str:
        pass

    @abstractmethod
    def print_std_out(self):
        pass
