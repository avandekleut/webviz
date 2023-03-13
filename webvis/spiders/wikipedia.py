import re
import scrapy
import urllib

from urllib.parse import urldefrag

from webvis.items import WebvisItem
from webvis.utils.path_filter import PathFilter


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

    def __init__(self, name=None, start_url=None, branching_factor=4, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [start_url] if start_url else self.start_urls
        self.branching_factor = int(branching_factor)

        self.filter = PathFilter(self.allowed_paths, self.ignore_paths)

    def parse(self, response):
        current_url = response.url
        self.filter.visit(current_url)
        source = self.get_wiki_title_from_url(current_url)

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
        return urls[:self.branching_factor]

    def get_outgoing_urls(self, response):
        return response.xpath('//a/@href').getall()

    def get_next_urls(self, response):
        wiki_urls = self.get_targeted_urls(response)

        unique_urls = self.get_unique(wiki_urls)

        subset = self.select_subset(unique_urls)

        return subset

    def get_targeted_urls(self, response):

        urls = []

        for url in self.get_outgoing_urls(response):
            url = self.get_full_url(response, url)

            if self.filter.should_ignore(url):
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
