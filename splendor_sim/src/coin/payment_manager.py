import typing

import networkx

import splendor_sim.interfaces.coin.i_coin_type as i_coin_type
import splendor_sim.interfaces.coin.i_coin_type_manager as i_coin_type_manager
import splendor_sim.interfaces.coin.i_payment_manager as i_payment_manager


class PaymentManager(i_payment_manager.IPaymentManager):
    _MAX_WEIGHT = 255

    def __init__(
            self,
            coin_type_manager: i_coin_type_manager.ICoinTypeManager
    ):
        self._coin_type_manager = coin_type_manager

    def validate_payment(
            self,
            cost: typing.Dict[i_coin_type.ICoinType, int],
            payment: typing.Dict[i_coin_type.ICoinType, int],
            discount: typing.Dict[i_coin_type.ICoinType, int]
    ) -> bool:
        self._validate_coin_dictionary(cost)
        self._validate_coin_dictionary(payment)
        self._validate_coin_dictionary(discount)

        discounted_cost = self._make_discounted_cost(cost, discount)

        total_cost = self._get_total(discounted_cost)
        total_payment = self._get_total(payment)

        graph = self._create_cost_graph(discounted_cost, payment)
        self.ford_fulkerson(graph, "source", "sink")
        max_flow = self._total_outbound_flow(graph)

        return total_cost == max_flow and total_payment == max_flow

    def _validate_coin_dictionary(self, coin_dictionary: typing.Dict[i_coin_type.ICoinType, int]):
        coin_set = self._coin_type_manager.get_coin_set()
        for key, value in coin_dictionary.items():
            if key not in coin_set:
                raise ValueError("Unknown coin type")
            if value < 0:
                raise ValueError("Negative costs or payment")

    @staticmethod
    def _make_discounted_cost(
            cost: typing.Dict[i_coin_type.ICoinType, int],
            discount: typing.Dict[i_coin_type.ICoinType, int]
    ):
        discounted_cost = {}
        for key, value in cost.items():
            if key in discount:
                discounted_cost[key] = max(value - discount[key], 0)
            else:
                discounted_cost[key] = value
        return discounted_cost

    @staticmethod
    def _get_total(
            cost: typing.Dict[i_coin_type.ICoinType, int]
    ) -> int:
        total = 0
        for coin in cost.keys():
            total += cost[coin]
        return total

    @staticmethod
    def _create_edge(from_node: str, to_node: str, weight):
        return from_node, to_node, {'capacity': weight, 'flow': 0}

    @staticmethod
    def _make_payment_weights(
            cost: typing.Dict[i_coin_type.ICoinType, int]
    ) -> typing.List[typing.Tuple[str, str, typing.Dict[str, int]]]:
        edges = []
        for coin in cost.keys():
            edges.append(PaymentManager._create_edge("source", coin.__str__() + "_payment", cost[coin]))
        return edges

    @staticmethod
    def _make_cost_weights(
            payment: typing.Dict[i_coin_type.ICoinType, int]
    ) -> typing.List[typing.Tuple[str, str, typing.Dict[str, int]]]:
        edges = []
        for coin in payment.keys():
            edges.append(PaymentManager._create_edge(coin.__str__() + "_cost", "sink", payment[coin]))
        return edges

    def _create_cost_graph(
            self,
            cost: typing.Dict[i_coin_type.ICoinType, int],
            payment: typing.Dict[i_coin_type.ICoinType, int]
    ) -> networkx.DiGraph:

        nodes = ["source",
                 "sink"]
        for coin_type in self._coin_type_manager.get_coin_set():
            nodes.append(coin_type.__str__() + "_payment")
            nodes.append(coin_type.__str__() + "_cost")

        graph = networkx.DiGraph()
        graph.add_nodes_from(nodes)
        edges = []
        edges.extend(self._make_payment_weights(payment))
        edges.extend(self._make_cost_weights(cost))
        for coin in self._coin_type_manager.get_coin_set():
            for equivalent in self._coin_type_manager.get_coin_usage(coin):
                edges.append(
                    self._create_edge(coin.__str__() + "_payment", equivalent.__str__() + "_cost", self._MAX_WEIGHT)
                )
        graph.add_edges_from(edges)
        return graph

    def _total_outbound_flow(self, graph: networkx.DiGraph) -> int:
        total = 0
        for coin in self._coin_type_manager.get_coin_set():
            if "sink" in graph[coin.__str__() + "_cost"]:
                total += graph[coin.__str__() + "_cost"]["sink"]["flow"]
        return total

    # code from https://medium.com/100-days-of-algorithms/day-49-ford-fulkerson-e70045dafd8b
    @staticmethod
    def ford_fulkerson(graph, source, sink):
        flow, path = 0, True

        while path:

            path, reserve = PaymentManager.depth_first_search(graph, source, sink)
            flow += reserve

            for vertex, destination_vertex in zip(path, path[1:]):
                if graph.has_edge(vertex, destination_vertex):
                    graph[vertex][destination_vertex]['flow'] += reserve
                else:
                    graph[destination_vertex][vertex]['flow'] -= reserve

    @staticmethod
    def depth_first_search(graph, source, sink):
        undirected = graph.to_undirected()
        explored = {source}
        stack = [(source, 0, dict(undirected[source]))]

        while stack:
            vertex, _, neighbours = stack[-1]
            if vertex == sink:
                break

            while neighbours:
                destination_vertex, edge = neighbours.popitem()
                if destination_vertex not in explored:
                    break
            else:
                stack.pop()
                continue

            in_direction = graph.has_edge(vertex, destination_vertex)
            capacity = edge['capacity']
            flow = edge['flow']
            neighbours = dict(undirected[destination_vertex])

            if in_direction and flow < capacity:
                stack.append((destination_vertex, capacity - flow, neighbours))
                explored.add(destination_vertex)

            elif not in_direction and flow:
                stack.append((destination_vertex, flow, neighbours))
                explored.add(destination_vertex)

        reserve = min((f for _, f, _ in stack[1:]), default=0)
        path = [vertex for vertex, _, _ in stack]

        return path, reserve
