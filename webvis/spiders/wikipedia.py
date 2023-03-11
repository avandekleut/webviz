import re
import scrapy
import urllib
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
from bs4 import BeautifulSoup
import random

from urllib.parse import urldefrag

from pyvis.network import Network

from webvis.items import WebvisItem


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/Salix_bebbiana"
    ]

    custom_settings = {
        # 'CONCURRENT_REQUESTS': 1,
        'CLOSESPIDER_PAGECOUNT': 25,
    }

    # TODO: Make these relative
    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        "https://en.wikipedia.org/wiki/*:*",
        "https://en.wikipedia.org/wiki/Main_Page"
    ]

    # TODO: Proper config
    first_n = 4
    first_p = None
    any_n = None
    any_p = None

    save_frequency = 10

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

    def parse(self, response):
        source = self.get_wiki_title_from_url(response.url)

        outgoing_links = self.get_outgoing_links(response,
                                                 first_n=self.first_n,
                                                 first_p=self.first_p,
                                                 any_n=self.any_n,
                                                 any_p=self.any_p)

        for url in outgoing_links:
            dest = self.get_wiki_title_from_url(url)

            yield scrapy.Request(url, callback=self.parse)

            item = WebvisItem()
            item['source'] = source
            item['dest'] = dest
            yield item

    def get_wiki_title_from_url(self, url):
        wiki_path = url.split("/wiki/")[-1]

        decoded = urllib.parse.unquote(
            wiki_path, encoding='utf-8', errors='replace')

        pretty = decoded.replace("_", " ")

        return pretty

    def get_outgoing_links(self, response, first_n=None, first_p=None, any_n=None, any_p=None):
        if not self.assert_at_most_one(first_n, first_p, any_n, any_p):
            raise Exception(
                f'must only pass one of: first_n, first_p, any_n, any_p')

        current_url = response.url
        self.logger.debug('current_url', current_url)
        urls = []

        for href in response.xpath('//a/@href').getall():
            url = self.get_full_url(response, href)
            if url == current_url:
                continue

            if self.should_ignore_path(url):
                continue

            if not self.should_allow_path(url):
                continue

            urls.append(url)

        unique_urls = self.get_unique(urls)

        if first_n:
            subset = self.get_first_n(unique_urls, first_n)
        elif first_p:
            subset = self.get_first_p(unique_urls, first_p)
        elif any_n:
            subset = self.get_any_n(unique_urls, any_n)
        elif any_p:
            subset = self.get_any_p(unique_urls, any_p)
        else:
            subset = unique_urls

        return subset

    def assert_at_most_one(self, *args):
        booled = [bool(x) for x in list(args)]
        truthy = [x for x in booled if x]
        return len(truthy) <= 1

    def get_unique(self, arr):
        return list(dict.fromkeys(arr))

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
