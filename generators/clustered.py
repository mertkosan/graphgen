import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from features import feature_functions_artificial_data as feature_functions
import utils
from generators.graphgen import GraphGen


class ClusteredDynamicGraph(GraphGen):
    def __init__(self, graph_count, n=100, p=0.1, threshold=0.2, seed=None, is_chain=False, min_cluster_no=10):
        super().__init__()

        self._graphs = []  # graphs
        self._labels = []  # labels (event or not)
        self._features = []  # feature vectors for each graph
        self._features_diff = []  # feature difference between two consecutive graphs
        self._clusters = None  # cluster object after training

        self._n = n  # number of nodes
        self._p = p  # edge probability
        self._threshold = threshold  # threshold value that p will be stable
        self._is_chain = is_chain  # is the dynamic graph chain?
        self._time_difference = True  # will it be looked difference of features?

        self._seed = seed
        self._min_cluster_no = min_cluster_no

        self._construct_graphs(graph_count)
        self._generate_features()
        self._normalize_features()
        if self._time_difference:
            self._calculate_feature_difference()
            self._cluster_features(self._features_diff)
            self._labels.append(0)
        else:
            self._cluster_features(self._features)
        self._determine_labels()
        super()._write_data(self._graphs, self._labels)

    def get_graphs(self):
        return self._graphs

    def _next_parameters(self):
        if not self._is_chain:
            self._n += int(np.round(np.random.exponential(1)))
            if self._p > self._threshold:
                self._p += np.random.normal(0, 0.01)
            else:
                self._p += np.random.normal(0.01, 0.01)
        # TODO : elif self.chain...

    def _construct_graphs(self, graph_count):
        for i in range(graph_count):
            gi = nx.erdos_renyi_graph(n=self._n, p=self._p, seed=self._seed)
            self._graphs.append(gi)
            self._next_parameters()
            print(self._n, self._p)

    def _generate_features(self):
        for subgraph in self._graphs:
            graph_features = []
            for func in feature_functions:
                graph_features.append(func(subgraph))
            self._features.append(graph_features)

    def _normalize_features(self):
        self._features = utils.normalize_min_max(self._features)

    def _calculate_feature_difference(self):
        self._features_diff = []
        for i in range(len(self._features) - 1):
            diff = np.subtract(self._features[i + 1], self._features[i])
            self._features_diff.append(diff)

    def _cluster_features(self, features):
        x = np.array(features)
        good_k = 0
        max_score = -1
        for k in range(self._min_cluster_no, self._min_cluster_no * 2):
            kmeans = KMeans(n_clusters=k, random_state=0).fit(x)
            score = silhouette_score(x, kmeans.labels_)
            if score > max_score:
                max_score = score
                good_k = k
        print(max_score)
        self._clusters = KMeans(n_clusters=good_k, random_state=0).fit(x)

    def _determine_labels(self):
        event_cluster = np.random.randint(0, self._clusters.n_clusters)
        for label in self._clusters.labels_:
            if event_cluster == label:
                self._labels.append(1)
            else:
                self._labels.append(0)
