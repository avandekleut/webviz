import re
import scrapy
import urllib

from urllib.parse import urldefrag

from webvis.items import WebvisItem
from webvis.utils.path_filter import PathFilter
from webvis.utils.path_sampler import PathSampler


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

        self.filter = PathFilter(self.allowed_paths, self.ignore_paths)
        self.sampler = PathSampler(branching_factor)

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

    def get_outgoing_urls(self, response):
        return response.xpath('//a/@href').getall()

    def get_next_urls(self, response):

        urls = []

        for url in self.get_outgoing_urls(response):
            url = self.get_full_url(response, url)

            if self.filter.should_ignore(url):
                continue

            urls.append(url)

        return self.sampler.filter(urls)

    def assert_at_most_one(self, *args):
        booled = [bool(x) for x in list(args)]
        truthy = [x for x in booled if x]
        return len(truthy) <= 1

    def get_full_url(self, response, href):
        url = response.urljoin(href)
        unfragmented = urldefrag(url)[0]  # remove anchors, etc
        return unfragmented
