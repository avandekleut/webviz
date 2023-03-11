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
        'CLOSESPIDER_PAGECOUNT': 25,
        'CHILDREN': 4,
        'STRATEGY': 'first',  # 'any'
        'SAVE_FREQUENCY': 10,
        'RANDOM_SEED': 0
    }

    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        "https://en.wikipedia.org/wiki/*:*",
        "https://en.wikipedia.org/wiki/Main_Page"
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        random.seed(self.custom_settings['RANDOM_SEED'])
        self.children = self.custom_settings['CHILDREN']
        self.strategy = self.custom_settings['STRATEGY']
        self.save_frequency = self.custom_settings['SAVE_FREQUENCY']

    def parse(self, response):
        source = self.get_wiki_title_from_url(response.url)

        outgoing_links = self.get_next_urls(response)

        print(outgoing_links)

        for url in outgoing_links:
            yield scrapy.Request(url, callback=self.parse)

            dest = self.get_wiki_title_from_url(url)

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

    def select_subset(self, urls: list):
        if self.strategy == 'first':
            return urls[:self.children]
        elif self.strategy == 'any':
            return random.sample(urls, self.children)

    def get_outgoing_urls(self, response):
        return response.xpath('//a/@href').getall()

    def get_next_urls(self, response):
        wiki_urls = self.get_wiki_urls(response)

        unique_urls = self.get_unique(wiki_urls)

        subset = self.select_subset(unique_urls)

        print(f"""
              wiki_urls: ({len(wiki_urls)}) {wiki_urls}
              unique_urls: ({len(unique_urls)}) {unique_urls}
              subset: ({len(subset)}) {subset}
              """)

        return subset

    def get_wiki_urls(self, response):
        current_url = response.url

        urls = []

        for url in self.get_outgoing_urls(response):
            url = self.get_full_url(response, url)
            if url == current_url:
                continue

            if self.should_ignore_path(url):
                continue

            if not self.should_allow_path(url):
                continue

            urls.append(url)

        return urls

    def assert_at_most_one(self, *args):
        booled = [bool(x) for x in list(args)]
        truthy = [x for x in booled if x]
        return len(truthy) <= 1

    def get_unique(self, arr):
        return list(dict.fromkeys(arr))

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
