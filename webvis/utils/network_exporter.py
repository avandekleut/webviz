import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman

from pyvis.network import Network


class Network:
    def __init__(self):
        self.nx = nx.Graph()

    def add_edge(self, source, dest):
        self.nx.add_edge(source, dest)

    def get_communities(self, groups: int):
        community_generator = girvan_newman(self.nx)

        # girvan_newman: each iteration produces exactly one
        # more community.
        iters = groups - 1
        for iter in range(iters):
            try:
                communities = map(list, next(community_generator))
            except StopIteration:
                pass

        return communities

    def update_node_sizes(self):
        for node in self.nx.nodes:
            size = self.get_node_size(node)
            self.nx.nodes[node]['size'] = size

    def get_node_size(self, node):
        size = self.get_num_neighbours(node)
        return self.normalize_size(size)

    def get_num_neighbours(self, node):
        neighbors = nx.all_neighbors(self.nx, node)
        num_neighbors = len(list(neighbors))
        return num_neighbors

    def normalize_size(self, size, base_size=2):
        return base_size + size
