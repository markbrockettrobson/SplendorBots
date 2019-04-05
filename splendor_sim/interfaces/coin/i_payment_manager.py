import abc
import typing

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager


class IPaymentManager(abc.ABC):
    @abc.abstractmethod
    def __init__(
            self,
            coin_type_manager: i_coin_type_manager.ICoinTypeManager
    ):
        """

        :param coin_type_manager: the coin type manager responsible for holding the relationships between coins\
               <i_coin_type_manager.ICoinTypeManager>
        """

    def validate_payment(
            self,
            cost: typing.Dict[i_coin_type.ICoinType, int],
            payment: typing.Dict[i_coin_type.ICoinType, int],
    ) -> bool:
        """

        :param cost:
               <typing.Dict[i_coin_type.ICoinType, int]>
        :param payment:
               <typing.Dict[i_coin_type.ICoinType, int]>
        :return: True if the payment can be used to pay the cost
                 <bool>
        """
