import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman

from pyvis.network import Network

from webvis.items import WebvisItem

import scrapy

import time


class PyVisPipeline:
    def __init__(self):
        # self.net = Network(
        #     directed=True,
        #     select_menu=True,
        # )
        self.nx = nx.DiGraph()
        self.count = 0
        self.save_frequency = 10
        self.start_time = time.time()
        self.end_time = None

    def open_spider(self, spider: scrapy.Spider):
        print('open spider')
        self.save_frequency = spider.custom_settings['SAVE_FREQUENCY'] or self.save_frequency

    def close_spider(self, spider):
        print('close_spider')
        print('count', self.count)
        self.update_and_save_network()
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        print(f'elapsed time: {elapsed_time} s')

    def update_and_save_network(self):
        self.update_nodes_and_edges()
        self.save_network()

    def process_item(self, item: WebvisItem, spider: scrapy.Spider):
        save_frequency = spider.settings.get('WANTED_SETTING')
        spider.settings

        self.count += 1

        self.nx.add_edge(item['source'], item['dest'])

        if self.count % self.save_frequency == 0:
            self.update_and_save_network()

        return item

    def update_nodes_and_edges(self, iters=7, desired_elements_per_community=None):
        if iters and desired_elements_per_community:
            raise Exception(
                f'expected one of: iters, desired_elements_per_community. got: {iters}, {desired_elements_per_community}')

        if desired_elements_per_community is not None:
            communities = self.get_communities_by_number_of_desired_elements_per_community(
                5)
        else:
            communities = self.get_communities(iters)
        self.update_node_groups(communities)
        # self.update_edge_weights_by_community_membership(communities)

        self.update_node_sizes()

    def get_communities_by_number_of_desired_elements_per_community(self, desired=5):
        """
        if after i iterations there are i + 1 communities and we want each community
        to hold d desired items, then the expected number of iterations is c = len(V) // d
        where len(V) is the number of nodes in the graph.

        This would yield c communities, each containing d elements, so that d * c = d * len(V) // d ~= len(V)
        """
        iters = len(self.nx.nodes) // desired
        return self.get_communities(iters)

    def get_communities(self, iters=5):
        assert iters > 0, f'expected: {iters} > 0'

        community_generator = girvan_newman(self.nx)

        # run the algorithm for iters - 1 iterations
        # girvan_newman: each iteration produces exactly one
        # more community.
        for iter in range(iters - 1):
            next(community_generator)

        communities = []
        for community in next(community_generator):
            community = list(community)
            communities.append(community)

        return communities

    def update_node_groups(self, communities):
        for i, community in enumerate(communities):
            for node in community:
                self.nx.nodes[node]['group'] = i

    def update_edge_weights_by_community_membership(self, communities):
        """
        update all edge weights to be 1 between members of a community and 0 
        between non-members
        """
        pass
        # for node in self.nx.nodes:
        # for
        # self.nx.nodes[node]['weight'] = 100

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

    def save_network(self, filename='out.html'):
        net = Network(
            # directed=True, # interesting but distracting
            select_menu=True
        )
        net.from_nx(self.nx)
        net.save_graph(filename)
