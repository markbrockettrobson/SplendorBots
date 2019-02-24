import abc


class ICoinType(abc.ABC):
    @abc.abstractmethod
    def __init__(self, name: str, total_number: int):
        """

        :param name: a string name used for printing
               <str>
        :param total_number: the total number of coins of this type
               <int>
        """

    @abc.abstractmethod
    def get_name(self) -> str:
        """

        :return: the str name of this coin type
                 <str>
        """

    @abc.abstractmethod
    def get_total_number(self) -> int:
        """

        :return: the total number of coins of this type
                 <int>
        """
