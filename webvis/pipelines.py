import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman

from webvis.items import WebvisItem

from scrapy.crawler import CrawlerProcess

from webvis.spiders.wikipedia import WikipediaSpider
from webvis.utils.network import NetworkHelper


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

    def __init__(self, network_groups: int):
        self.net = NetworkHelper()

        self.count = 0
        self.network_groups = network_groups

        print(self.__dict__)

    def open_spider(self, spider: WikipediaSpider):
        pass

    def close_spider(self, spider: WikipediaSpider):
        self.net.update_network_properties(self.network_groups)
        self.net.save_network()
        print(f'Finished with {self.count} nodes.')

    def process_item(self, item: WebvisItem, spider: WikipediaSpider):
        self.count += 1

        self.net.add_edge(item['source'], item['dest'])

        return item
