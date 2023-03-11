
from pyvis.network import Network

from webvis.items import WebvisItem

from collections import defaultdict


class PyVisPipeline:
    def __init__(self):
        self.edges = defaultdict(list)

        self.url_to_title_mapping = {}

    def open_spider(self, spider):
        print('open_spider')

    def close_spider(self, spider):
        print('close_spider')
        self.save_graph()

    def save_graph(self, filename='out.html'):
        net = Network()

        for source_url in self.edges:
            source_title = self.url_to_title_mapping[source_url
                                                     ]
            net.add_node(
                source_url, label=source_title)

            for dest_url in self.edges[source_url]:
                if not dest_url in self.url_to_title_mapping:
                    print(f'no title saved for {dest_url}')
                    dest_title = dest_url.replace("_", " ")
                else:
                    dest_title = self.url_to_title_mapping[dest_url]

                net.add_node(dest_url, label=dest_title)

                net.add_edge(source_url, dest_url)

        print(f'saving graph')
        net.save_graph(filename)

    def process_item(self, item: WebvisItem, spider):
        source_url = item['source_url']
        source_title = item['source_title']
        dest_url = item['dest_url']

        # we don't know dest_title yet since we haven't scraped it.
        # we'll come back later with the label when we've finished scraping.
        self.url_to_title_mapping[source_url] = source_title

        self.edges[source_url].append(dest_url)

        return item
