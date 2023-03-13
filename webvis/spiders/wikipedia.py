import scrapy
import urllib

from urllib.parse import urldefrag

from webvis.items import WebvisItem
from webvis.utils.path_filter import PathFilter
from webvis.utils.path_sampler import PathSampler
from webvis.utils.wikipedia_parser import WikipediaParser


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
        parsed = WikipediaParser(response)
        print('parsed')

        self.filter.visit(parsed.url)
        print('visited')

        source = parsed.get_title()
        print('source', source)

        all_urls = parsed.get_urls()
        print('all_urls', all_urls)

        urls = self.filter_urls(all_urls)
        print('urls', urls)

        for url in urls:
            print('yield url', url)
            yield scrapy.Request(url, callback=self.parse)

            dest = parsed.get_title(url)
            print('dest', dest)

            item = WebvisItem()
            item['source'] = source
            item['dest'] = dest

            print('item', item)

            yield item

    def filter_urls(self, urls):
        filtered_urls = []
        for url in urls:
            if self.filter.should_ignore(url):
                continue

            filtered_urls.append(url)

        return self.sampler.filter(filtered_urls)
