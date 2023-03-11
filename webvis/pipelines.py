import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman

from pyvis.network import Network

from webvis.items import WebvisItem


class PyVisPipeline:
    def __init__(self):
        # self.net = Network(
        #     directed=True,
        #     select_menu=True,
        # )
        self.nx = nx.DiGraph()
        self.count = 0
        self.save_frequency = 10

    def open_spider(self, spider):
        print('open_spider')

    def close_spider(self, spider):
        print('close_spider')
        print('count', self.count)
        self.compute_communities()
        self.compute_sizes()
        self.save_network()

    def process_item(self, item: WebvisItem, spider):
        self.count += 1

        self.nx.add_edge(item['source'], item['dest'])

        return item

    def compute_communities(self, iters=5):
        assert iters > 0, f'expected: {iters} > 0'

        community_generator = girvan_newman(self.nx)

        # run the algorithm for iters - 1 iterations
        for iter in range(iters - 1):
            next(community_generator)

        communities = []
        for i, community in enumerate(next(community_generator)):
            community = list(community)
            communities.append(community)

            for node in community:
                self.nx.nodes[node]['group'] = i

        print(f'found {len(communities)} communities in {iters} iterations')
        print(communities)

    def compute_sizes(self, base_size=2):
        for node in self.nx.nodes:
            neighbors = nx.all_neighbors(self.nx, node)
            num_neighbors = len(list(neighbors))
            node_size = base_size + num_neighbors
            self.nx.nodes[node]['size'] = node_size

    def save_network(self, filename='out.html'):
        net = Network(
            # directed=True,
            select_menu=True
        )
        net.from_nx(self.nx)
        net.save_graph(filename)
