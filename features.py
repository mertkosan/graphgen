import networkx as nx
from networkx.algorithms import approximation as aprx
from networkx.algorithms import community as comm
import utils


# one feature value for series of graphs, last feature value is for the current graph
def weighted_average_based_history_function(feature_arr, decimal_places=4):
    diff_arr = [feature_arr[i + 1] - feature_arr[i] for i in range(len(feature_arr) - 1)]
    history = diff_arr[:-1]
    return round(utils.weighted_average_based_on_index(history) + diff_arr[-1], decimal_places)


def average_degree(graph, decimal_place=4):
    degrees = nx.degree(graph)
    total_degree = 0
    for node in degrees:
        total_degree += node[1]
    return round(total_degree / nx.number_of_nodes(graph), decimal_place)


def max_degree(graph):
    degrees = nx.degree(graph)
    _max = 0
    for node in degrees:
        if node[1] > _max:
            _max = node[1]
    return _max


def max_eigenvector_centrality(graph, decimal_place=4):
    ei = nx.eigenvector_centrality_numpy(graph)
    max_ei = 0
    for node in ei:
        if ei[node] > max_ei:
            max_ei = ei[node]
    return round(max_ei, decimal_place)


def avg_eigenvector_centrality(graph, decimal_place=4):
    ei = nx.eigenvector_centrality_numpy(graph)
    sum_ei = 0
    for node in ei:
        sum_ei += ei[node]
    return round(sum_ei / len(ei), decimal_place)


def number_of_local_bridges(graph):
    return len(list(nx.local_bridges(graph)))


def length_maximal_matching(graph):
    return len(aprx.min_maximal_matching(graph))


def number_of_greedy_modularity_components(graph):
    return len(comm.greedy_modularity_communities(graph))


feature_functions = [
    nx.number_of_edges,
    nx.number_of_nodes,
    average_degree,
    max_degree,
    nx.density,
    nx.is_connected,
    nx.algorithms.shortest_paths.average_shortest_path_length
]

feature_functions_artificial_data = [
    nx.number_of_edges,
    nx.number_of_nodes,
    average_degree,
    max_degree,
    nx.density,
    aprx.node_connectivity,  # Problematic with 1000 nodes
    aprx.large_clique_size,
    aprx.average_clustering,
    length_maximal_matching,
    nx.has_bridges,
    number_of_local_bridges,
    max_eigenvector_centrality,
    avg_eigenvector_centrality,
    number_of_greedy_modularity_components,
    nx.is_connected,
    nx.number_connected_components,
    nx.is_biconnected,
    nx.diameter,  # Problematic with 1000 nodes
    nx.radius
]
