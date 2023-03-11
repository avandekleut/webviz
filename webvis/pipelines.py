
from pyvis.network import Network

from webvis.items import WebvisItem


class PyVisPipeline:
    def __init__(self):
        self.net = Network(directed=True)
        self.count = 0
        self.save_frequency = 10

    def open_spider(self, spider):
        print('open_spider')

    def close_spider(self, spider):
        print('close_spider')
        print('count', self.count)
        self.net.save_graph('out.html')

    def process_item(self, item: WebvisItem, spider):
        self.count += 1

        source_url = item['source_url']
        dest_url = item['dest_url']

        self.net.add_node(
            source_url, label=source_url.replace("_", " "))

        self.net.add_node(dest_url, label=dest_url.replace("_", " "))

        self.net.add_edge(source_url, dest_url)

        if self.count % self.save_frequency == 0:
            self.net.save_graph('out.html')

        self.net.directed

        return item
