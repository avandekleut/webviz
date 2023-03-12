from pyvis.network import Network

import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman


class NetworkHelper:
    def __init__(self):
        self.nx = nx.Graph()

    def add_edge(self, source, dest):
        self.nx.add_edge(source, dest)

    def save_network(self, filename='out.html'):
        net = Network(
            # directed=True, # interesting but distracting
            select_menu=True
        )
        net.from_nx(self.nx)
        net.save_graph(filename)

    def update_network_properties(self, groups: int):
        communities = self.get_communities(groups)
        self.update_node_group_membership_by_community(communities)
        self.update_node_sizes()

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

    def update_node_group_membership_by_community(self, communities):
        for i, community in enumerate(communities):
            for node in community:
                self.update_node(node, {'group': i})

    # def rename_all_nodes_foo(self):
    #     for node in self.nx.nodes:
    #         self.update_node(node, {'label': "foo"})

    def update_node(self, node: str, props: dict):
        for key, value in props.items():
            self.nx.nodes[node][key] = value

    def update_node_sizes(self):
        for node in self.nx.nodes:
            size = self.get_node_size(node)
            self.update_node(node, {'size': size})

    def get_node_size(self, node):
        size = self.get_num_neighbours(node)
        return self.normalize_size(size)

    def get_num_neighbours(self, node):
        neighbors = nx.all_neighbors(self.nx, node)
        num_neighbors = len(list(neighbors))
        return num_neighbors

    def normalize_size(self, size, base_size=2):
        return base_size + size
