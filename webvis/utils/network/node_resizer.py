from networkx import all_neighbors
from networkx import Graph

from webvis.utils.create_missing_folders import create_missing_folders


class NodeResizer:
    def __init__(self, network: Graph):
        self.network = network

    def update_node_sizes(self):
        for node in self.network.nodes:
            size = self.get_node_size(node)
            self.network.nodes[node]['size'] = size

    def get_node_size(self, node):
        size = self.get_num_neighbours(node)
        return self.normalize_size(size)

    def get_num_neighbours(self, node):
        neighbors = all_neighbors(self.network, node)
        num_neighbors = len(list(neighbors))
        return num_neighbors

    def normalize_size(self, size, base_size=2):
        return base_size + size
