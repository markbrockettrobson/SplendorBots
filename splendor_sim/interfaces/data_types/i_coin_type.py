import abc


class ICoinType(abc.ABC):
    @abc.abstractmethod
    def __init__(self, name: str, total_number: int):
        """

        :param name: <str>
        :param total_number: <int>
        """

    def get_name(self) -> str:
        """

        :return: <str>
        """

    def get_total_number(self) -> int:
        """

        :return: <int>
        """
