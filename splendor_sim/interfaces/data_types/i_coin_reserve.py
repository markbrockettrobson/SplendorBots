from abc import ABC, abstractmethod
from typing import List

# todo document this


class ICoinReserve(ABC):

    def __init__(self, color_names: List[str], max_number_of_coin: int):
        raise NotImplemented

    def __str__(self)-> str:
        raise NotImplemented

    @abstractmethod
    def print_std_out(self):
        raise NotImplemented
