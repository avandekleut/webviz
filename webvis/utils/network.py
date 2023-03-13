import pickle

from pyvis.network import Network

import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman


class NetworkHelper:
    def __init__(self):
        self.nx = nx.Graph()

    def add_edge(self, source, dest):
        self.nx.add_edge(source, dest)

    def pipeline(self, groups=6, name='out'):
        """
        basic steps to run from any base self.nx network
        """
        self.pretty()
        self.cluster(groups)
        self.export_pyvis(name)
        self.export_nx(name)

    def pretty(self):
        """
        adjust visual graph properties like node size,
        labels
        """
        self._update_node_sizes()

    def export_nx(self, name: str):
        filename = self.get_nx_filename(name)
        pickle.dump(self.nx, open(filename, 'wb'))

    def load_nx(self, name: str):
        filename = self.get_nx_filename(name)
        self.nx = pickle.load(open(filename, 'rb'))

    @classmethod
    def from_cache(cls, name: str):
        net = cls()
        net.load_nx(name)
        return net

    @classmethod
    def get_nx_filename(cls, name):
        return name + '.nx'

    def export_pyvis(self, name: str):
        filename = name + '.html'
        net = Network(
            select_menu=True
        )
        net.from_nx(self.nx)
        net.save_graph(filename)

    def cluster(self, num_clusters: int):
        communities = self._get_clusters(num_clusters)
        self._update_node_group_membership_by_community(communities)

    def _update_node_sizes(self):
        for node in self.nx.nodes:
            size = self._get_node_size(node)
            self._update_node(node, {'size': size})

    def _get_node_size(self, node):
        size = self._get_num_neighbours(node)
        return self._normalize_size(size)

    def _get_num_neighbours(self, node):
        neighbors = nx.all_neighbors(self.nx, node)
        num_neighbors = len(list(neighbors))
        return num_neighbors

    def _normalize_size(self, size, base_size=2):
        return base_size + size

    def _get_clusters(self, num_clusters: int):
        cluster_generator = girvan_newman(self.nx)

        # girvan_newman: each iteration produces exactly one
        # more community.
        iters = num_clusters - 1
        for iter in range(iters):
            try:
                clusters = map(list, next(cluster_generator))
            except StopIteration:
                pass

        return clusters

    def _update_node_group_membership_by_community(self, communities):
        for i, community in enumerate(communities):
            for node in community:
                self._update_node(node, {'group': i})

    def _update_node(self, node: str, props: dict):
        for key, value in props.items():
            self.nx.nodes[node][key] = value
