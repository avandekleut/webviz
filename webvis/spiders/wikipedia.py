import re
import scrapy
import urllib
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
from bs4 import BeautifulSoup
import random

from urllib.parse import urldefrag

from pyvis.network import Network


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Salix_bebbiana"]

    # TODO: Make these relative
    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        "https://en.wikipedia.org/wiki/*:*",
    ]

    net = Network()

    max_children = 3
    limit = 100

    # subset selection
    first_n = 1

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

    def parse(self, response, meta={}):

        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find_all("h1", {"id": "firstHeading"})[0].getText()

        parent_title = meta.get('parent_title')
        parent_title = parent_title or None

        current_url = response.url

        current_path = current_url.split("/wiki/")[-1]
        source_node = urllib.parse.unquote(
            current_path, encoding='utf-8', errors='replace')
        self.net.add_node(source_node)

        outgoing_links = self.get_outgoing_links(
            response, first_n=self.first_n)
        max_visit_count = self.max_children if self.max_children is not None else len(
            outgoing_links)

        visited_count = 0
        for url in outgoing_links:
            if visited_count >= max_visit_count:
                break

            if url == current_url:
                continue

            if self.should_ignore_path(url):
                continue

            if not self.should_allow_path(url):
                continue

            visited_count += 1
            self.limit -= 1

            dest_path = url.split("/wiki/")[-1]
            dest_node = urllib.parse.unquote(
                dest_path, encoding='utf-8', errors='replace')
            self.net.add_node(dest_node)
            self.net.add_edge(source_node, dest_node)

            if self.limit > 0:
                print(
                    f'yielding with limit {self.limit} queue size {len(self.crawler.engine.slot.scheduler)}')
                yield scrapy.Request(url, callback=self.parse, meta={"parent_title": title})
            else:
                print('done')
                self.net.show('out.html')

    def get_outgoing_links(self, response, first_n=None, first_p=None, any_n=None, any_p=None):
        if not self.assert_one_of_many(first_n, first_p, any_n, any_p):
            raise Exception(
                f'must only pass one of: first_n, first_p, any_n, any_p')

        urls = []

        for href in response.xpath('//a/@href').getall():
            url = self.get_full_url(response, href)
            urls.append(url)

        unique_urls = list(set(urls))
        sorted_urls = sorted(unique_urls)

        subset = sorted_urls
        if first_n:
            print('first_n', first_n)
            subset = self.get_first_n(sorted_urls, first_n)
        elif first_p:
            print('first_p', first_p)
            subset = self.get_first_p(sorted_urls, first_p)
        elif any_n:
            subset = self.get_any_n(sorted_urls, any_n)
        elif any_p:
            subset = self.get_any_p(sorted_urls, any_p)

        return subset

    def assert_one_of_many(self, *args):
        booled = [bool(x) for x in list(args)]
        truthy = [x for x in booled if x]
        return len(truthy) == 1

    def get_first_n(self, arr, n=1):
        return arr[:n]

    def get_any_n(self, arr, n=1, seed=0):
        random.seed(seed)
        return random.sample(arr, n)

    def get_first_p(self, arr, p=0.1):
        equivalent_n = int(len(arr)*p)
        return self.get_first_n(arr, equivalent_n)

    def get_any_p(self, arr, p=0.1, seed=0):
        equivalent_n = int(len(arr)*p)
        return self.get_any_n(arr, equivalent_n, seed=seed)

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
