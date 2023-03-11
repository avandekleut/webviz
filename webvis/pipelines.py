
from pyvis.network import Network

from webvis.items import WebvisItem


class PyVisPipeline:
    def __init__(self):
        self.net = Network(
            directed=True,
            select_menu=True,
        )
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

        source = item['source']
        dest = item['dest']

        self.net.add_node(source)

        self.net.add_node(dest)

        self.net.add_edge(source, dest)

        if self.count % self.save_frequency == 0:
            self.net.save_graph('out.html')

        return item
