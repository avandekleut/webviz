import re
import scrapy
import urllib
import random

from urllib.parse import urldefrag

from webvis.items import WebvisItem


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/Salix_bebbiana"
    ]

    custom_settings = {
        # NOTE: Generally speaking this will generate more than 100 results.
        # In experiments it returned up to 200 results.
        'CLOSESPIDER_ITEMCOUNT': 100
    }

    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        # discussion posts etc
        "https://en.wikipedia.org/wiki/*:*",

        # keep search local, main page links to random
        "https://en.wikipedia.org/wiki/Main_Page"
    ]

    def __init__(self, name=None, start_url=None, children=4, groups=6, random_seed=0, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [start_url] if start_url else self.start_urls
        self.children = int(children)

        # TODO: Pull this out of this class
        self.groups = int(groups)

        random.seed(random_seed)

        self.logger.debug({'self': self.__dict__, })

    def parse(self, response):
        source = self.get_wiki_title_from_url(response.url)

        outgoing_links = self.get_next_urls(response)

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
        return urls[:self.children]

    def get_outgoing_urls(self, response):
        return response.xpath('//a/@href').getall()

    def get_next_urls(self, response):
        wiki_urls = self.get_targeted_urls(response)

        unique_urls = self.get_unique(wiki_urls)

        subset = self.select_subset(unique_urls)

        return subset

    def get_targeted_urls(self, response):
        def should_ignore(url):
            if url == response.url:
                return True

            if self.should_ignore_path(url):
                return True

            if not self.should_allow_path(url):
                return True

        urls = []

        for url in self.get_outgoing_urls(response):
            url = self.get_full_url(response, url)

            if should_ignore(url):
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
