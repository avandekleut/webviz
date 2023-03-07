import re
import scrapy

from collections import defaultdict

from urllib.parse import urldefrag

from pyvis.network import Network


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Functor"]

    max_depth = 1

    # TODO: Make these relative
    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        "https://en.wikipedia.org/wiki/*:*",
    ]

    network = Network()

    def parse(self, response, depth=0):
        if depth >= self.max_depth:
            return

        current_url = response.url

        self.network.add_node(current_url)

        for url in self.get_outgoing_links(response):
            if self.should_ignore_path(url):
                yield
                continue

            if not self.should_allow_path(url):
                yield
                continue

            print(f'({depth}) {url}')

            self.network.add_node(url)
            self.network.add_edge(current_url, url)

            yield scrapy.Request(url, lambda response: self.parse(response, depth+1),)

        if depth == 0:
            print('done')
            print(self.network)
            self.network.toggle_physics(True)
            self.network.show('graph.html', notebook=False)

    def get_outgoing_links(self, response):
        urls = []

        for href in response.xpath('//a/@href').getall():
            url = self.get_full_url(response, href)
            urls.append(url)

        unique_urls = list(set(urls))

        return unique_urls

    def get_full_url(self, response, href):
        url = response.urljoin(href)
        unfragmented = urldefrag(url)[0]  # remove anchors, etc
        return unfragmented

    def should_ignore_path(self, path):
        return self.filter_paths_by_pattern(path, self.ignore_paths)

    def should_allow_path(self, path):
        return self.filter_paths_by_pattern(path, self.allowed_paths)

    def filter_paths_by_pattern(self, path, patterns):
        for pattern in patterns:
            regular_expression = self.wildcard_to_regular_expression(pattern)
            if re.match(regular_expression, path):
                return True

        return False

    def wildcard_to_regular_expression(self, path):
        return re.escape(path).replace('\*', '.+')
