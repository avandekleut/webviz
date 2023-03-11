import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman

from pyvis.network import Network
from pyvis.options import Layout

from webvis.items import WebvisItem


class PyVisPipeline:
    def __init__(self):
        self.net = Network(
            directed=True,
            select_menu=True,
            # layout=Layout(randomSeed=0)  # reproducibility
        )
        self.nx = nx.DiGraph()
        self.count = 0
        self.save_frequency = 10

    def open_spider(self, spider):
        print('open_spider')

    def close_spider(self, spider):
        print('close_spider')
        print('count', self.count)
        self.compute_communities()
        # self.net.show_buttons()
        self.net.save_graph('out.html')

    def process_item(self, item: WebvisItem, spider):
        self.count += 1

        source = item['source']
        dest = item['dest']

        # self.net.add_node(source)

        # self.net.add_node(dest)

        # self.net.add_edge(source, dest)

        self.nx.add_edge(source, dest)

        if self.count % self.save_frequency == 0:
            self.net.save_graph('out.html')

        return item

    def compute_communities(self, iters=4):
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
                # self.net.add_node(node, group=i)
                self.nx.nodes[node]['group'] = i

        print(f'found {len(communities)} communities in {iters} iterations')
        print(communities)

        self.net.from_nx(self.nx)
