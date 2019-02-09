import copy
import typing

from splendor_sim.interfaces.data_types.i_coin_reserve import ICoinReserve
from splendor_sim.interfaces.collection_rules.i_collection_rule import ICollectionRule
# todo document this


class CoinReserve(ICoinReserve):

    def __init__(self,
                 color_names: typing.List[str],
                 max_number_of_coin: int):

        self._rules = []
        self._number_of_coin_types = len(color_names)
        self._color_names = color_names
        self._longest_name_length = max(len(name) for name in color_names)
        self._max_number_of_coin = max_number_of_coin
        self._current_coin_count = copy.deepcopy(max_number_of_coin)

    def __str__(self,
                format_template=None)-> str:

        output_string = ''
        if not format_template:
            format_template = '{0:' + str(self._longest_name_length) + 's} | {1:3d}/{2:d}\n'
        for i in range(self._number_of_coin_types):
            output_string += format_template.format(self._color_names[i],
                                                    self._current_coin_count[i],
                                                    self._max_number_of_coin[i])
        return output_string

    def print_std_out(self):
        print(str(self))

    def add_rule(self, rule: ICollectionRule):
        self._rules.append(rule)

    def get_rules(self)-> typing.List[ICollectionRule]:
        return self._rules
