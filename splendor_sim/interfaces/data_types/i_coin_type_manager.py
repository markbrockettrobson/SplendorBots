import abc
import typing

import splendor_sim.interfaces.data_types.i_coin_type as i_coin_type


class ICoinTypeManager(abc.ABC):
    @abc.abstractmethod
    def __init__(self,
                 coin_type_list: typing.List[i_coin_type.ICoinType],
                 coin_equivelances: typing.List[typing.Tuple[i_coin_type.ICoinType, i_coin_type.ICoinType]]):
        pass

    def get_coin_list(self) -> typing.List[i_coin_type.ICoinType]:
        pass

    def get_equivalent_coins(self,
                             coin_type: i_coin_type.ICoinType
                             ) -> typing.List[i_coin_type.ICoinType]:
        pass

    def get_coin_usage(self,
                       coin_type: i_coin_type.ICoinType
                       ) -> typing.List[i_coin_type.ICoinType]:
        pass
