import numpy as np
import networkx as nx
import csv
from time import asctime


class GraphGen:
    def __init__(self):
        pass

    def _write_data(self, graphs, labels):
        if len(graphs) != len(labels):
            raise Exception("The number of graphs should be equal to the number of labels!")

        if len(graphs) <= 0 or len(labels) <= 0:
            raise Exception("The size of the graph/labels should be bigger than 0!")

        _dump_time = asctime()
        with open("data/%s_edges.csv" % str(_dump_time), "w") as _csv_file:
            _field_names = ['timestamp', 'source', 'destination']
            _writer = csv.DictWriter(_csv_file, fieldnames=_field_names)
            _writer.writeheader()

            for timestamp, graph in enumerate(graphs):
                for edges in graph.edges:
                    _writer.writerow({'timestamp': timestamp, 'source': edges[0], 'destination': edges[1]})

        with open("data/%s_labels.csv" % str(_dump_time), "w") as _csv_file:
            _field_names = ['timestamp', 'is_event']
            _writer = csv.DictWriter(_csv_file, fieldnames=_field_names)
            _writer.writeheader()

            for timestamp, label in enumerate(labels):
                _writer.writerow({'timestamp': timestamp, 'is_event': label})
