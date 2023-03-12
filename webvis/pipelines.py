import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman

from pyvis.network import Network

from webvis.items import WebvisItem

from scrapy.crawler import CrawlerProcess

from webvis.spiders.wikipedia import WikipediaSpider


class PyVisPipeline:
    @classmethod
    def from_crawler(cls, crawler: CrawlerProcess):
        """
        instantiate this pipeline given a crawler reference. The crawler has
        access to the current settings which can be used to configure this
        pipeline.
        """
        # Get settings e.g. from command line like -S NETWORK_GROUPS=8
        settings = crawler.settings
        network_groups = settings.getint('NETWORK_GROUPS')

        return cls(network_groups)

    def __init__(self,  network_groups: int):
        self.nx = nx.Graph()

        self.count = 0
        self.network_groups = network_groups

        print(self.__dict__)

    def open_spider(self, spider: WikipediaSpider):
        pass

    def close_spider(self, spider: WikipediaSpider):
        self.update_and_save_network()
        print(f'Finished with {self.count} nodes.')

    def process_item(self, item: WebvisItem, spider: WikipediaSpider):
        self.count += 1

        self.nx.add_edge(item['source'], item['dest'])

        return item

    def update_and_save_network(self):
        self.update_network_properties()
        self.save_network()

    def update_network_properties(self, ):
        communities = self.get_communities()
        self.update_node_group_membership_by_community(communities)

        self.update_node_sizes()

    def save_network(self, filename='out.html'):
        net = Network(
            # directed=True, # interesting but distracting
            select_menu=True
        )
        net.from_nx(self.nx)
        net.save_graph(filename)

    def get_communities(self):
        community_generator = girvan_newman(self.nx)

        # girvan_newman: each iteration produces exactly one
        # more community.
        iters = self.network_groups - 1
        for iter in range(iters):
            try:
                communities = map(list, next(community_generator))
            except StopIteration:
                pass
                # print(
                #     f'terminated get_communities early: ({iter}) StopIteration')

        return communities

    def update_node_group_membership_by_community(self, communities):
        for i, community in enumerate(communities):
            for node in community:
                self.nx.nodes[node]['group'] = i

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
