import numpy as np
import networkx as nx
from generators.graphgen import GraphGen


class RandomDynamicGraph(GraphGen):
    def __init__(self, count):
        super().__init__()

        self._graph_count = count  # Number of graph in dynamic graph

        self._graphs = []  # All graphs.
        self._n = 1000  # Initial number of nodes.
        self._p = 0.01  # Initial probability of each edge.
        self._p_next = 0.01  # Probability of an edge for next time.
        self._event_trigger = 0.5  # How much increase density will be enough for an event.
        self._p_change = 1  # Max percentage change of p_next for the next generation.

        increase = True
        self._event_information = []
        for _ in range(0, count):
            graph = nx.erdos_renyi_graph(self._n, self._p_next)
            self._graphs.append(graph)
            if self._is_event(graph):
                self._event_information.append(1)
                increase = False
            else:
                self._event_information.append(0)
                if self._p_next <= self._p:
                    increase = True
            self._next_p_next(increase)

        super()._write_data(self._graphs, self._labels)

    # reset p to default
    def _reset_p_next(self):
        self._p_next = self._p

    # increase the probability of edge creation
    def _next_p_next(self, increase=True):
        if increase:
            self._p_next += self._p_next * np.random.uniform(0, self._p_change)
        else:
            self._p_next -= self._p_next * np.random.uniform(0, self._p_change)

    def _get_graphs(self):
        return self._graphs

    def _get_event_info(self):
        return self._event_information

    def _is_event(self, graph):
        return nx.density(graph) >= self._event_trigger
