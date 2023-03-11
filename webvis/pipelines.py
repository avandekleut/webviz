
from pyvis.network import Network

from webvis.items import WebvisItem

from collections import defaultdict


class PyVisPipeline:
    def __init__(self):
        self.total = 0
        self.net = Network()
        self.url_to_title_mapping = {}
        self.edges = defaultdict(list)

    def open_spider(self, spider):
        print('open_spider')

    def close_spider(self, spider):
        print('close_spider')
        for source_url in self.edges:
            source_title = self.url_to_title_mapping[source_url
                                                     ]
            self.net.add_node(
                source_url, label=source_title)

            for dest_url in self.edges[source_url]:
                if not dest_url in self.url_to_title_mapping:
                    dest_title = dest_url
                else:
                    dest_title = self.url_to_title_mapping[dest_url]

                print(f'{source_title} -> {dest_title}')

                self.net.add_node(dest_url, label=dest_title)

                self.net.add_edge(source_url, dest_url)

        print(f'saving graph')
        self.net.save_graph('out.html')

    def process_item(self, item: WebvisItem, spider):
        print(f'--- item: {item}')
        self.total += 1

        source_url = item['source_url']
        source_title = item['source_title']
        dest_url = item['dest_url']

        # we don't know dest_title yet since we haven't scraped it.
        # we'll come back later with the label when we've finished scraping.
        self.url_to_title_mapping[source_url] = source_title

        print(source_url, '->', dest_url)

        self.edges[source_url].append(dest_url)

        # if not self.net.get_node(parent_url):
        #     self.net.add_node(parent_url, label=parent_title)

        # self.net.add_node(item.url, label=item.title)

        # self.net.add_edge(item.url, item.parent_title)

        # if self.total % self.save_frequency == 0:
        #     print(f'{self.total} % {self.save_frequency} == 0')
        #     self.net.save_graph('out.html')

        return item
