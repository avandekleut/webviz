from networkx import Graph

from webvis.items import WebvisItem

from webvis.spiders.wikipedia import WikipediaSpider
from webvis.utils.network.pipeline import Pipeline

import logging


class PyVisPipeline:
    def __init__(self):
        self.network = Graph()
        self.logger = logging.getLogger('PyVisPipeline')

    def open_spider(self, spider: WikipediaSpider):
        self.logger.debug('open_spider')
        pass

    def close_spider(self, spider: WikipediaSpider):
        self.logger.debug('close_spider')
        self.logger.debug(f'total nodes: {len(self.network.nodes)}')

        for num_clusters in range(1, 10):
            self.logger.debug(f'Running pipeline {num_clusters}')
            Pipeline(self.network).run(
                num_clusters, name=f'out_{num_clusters}')

    def process_item(self, item: WebvisItem, spider: WikipediaSpider):
        self.network.add_edge(item['source'], item['dest'])

        return item
