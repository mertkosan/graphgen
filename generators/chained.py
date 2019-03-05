import numpy as np
import networkx as nx
from generators.graphgen import GraphGen


class ChainedDynamicGraph(GraphGen):
    def __init__(self, count):
        super().__init__()

        self._graph_count = count  # Number of graph in dynamic graph

        self._graphs = []  # All graphs
        self._n = 1000  # Initial number of nodes
        self._p = 0.001  # Initial probability of each edge
        self._event_trigger = 0.07  # How much increase in # edges will result in an event.
        self._p_next = self._p / 20 / (1 - self._p)  # Probability of edge creation for the next generation.
        self._p_increase = 0.5  # Max percentage increase of p_next for the next generation.

        # Initialize with the first graph
        first_graph = nx.erdos_renyi_graph(self._n, self._p)
        self._graphs.append(first_graph)

        # Create dynamic graph with events
        self._event_information = [0]
        current_graph = first_graph
        for _ in range(1, count):
            next_graph = self._find_next_graph(current_graph)
            if self._is_event(next_graph, current_graph):
                self._event_information.append(1)
                self._reset_p_next(current_graph_density=nx.density(next_graph))
            else:
                self._event_information.append(0)
                self._next_p_next()
            current_graph = next_graph
            print(self._p_next, nx.density(current_graph))

        super()._write_data(self._graphs, self._labels)

    # reset to p value to approximately %5 increase edge number
    def _reset_p_next(self, current_graph_density):
        self._p_next = current_graph_density / 20 / (1 - current_graph_density)

    # increase the probability of edge creation
    def _next_p_next(self):
        self._p_next += self._p_next * np.random.uniform(0, self._p_increase)

    def _find_next_graph(self, current_graph):
        next_graph = current_graph.copy()
        for edge in nx.non_edges(next_graph):
            if np.random.binomial(1, self._p_next) == 1:
                next_graph.add_edge(edge[0], edge[1])
        self._graphs.append(next_graph)
        return next_graph

    def _get_graphs(self):
        return self._graphs

    def _get_event_info(self):
        return self._event_information

    def _is_event(self, next_graph, current_graph):
        return len(next_graph.edges) / len(current_graph.edges) >= 1 + self._event_trigger
