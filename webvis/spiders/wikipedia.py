import re
import scrapy

from collections import defaultdict

from urllib.parse import urldefrag


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Functor"]

    # TODO: Make these relative
    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        "https://en.wikipedia.org/wiki/*:*",
    ]

    adjacency_matrix = defaultdict(dict)

    def parse(self, response, depth=0):
        current_url = response.url

        for url in self.get_outgoing_links(response):
            if self.should_ignore_path(url):
                yield
                continue

            if not self.should_allow_path(url):
                yield
                continue

            print(f'({depth}) {url}')

            self.adjacency_matrix[current_url][url] = True

            yield scrapy.Request(url, lambda response: self.parse(response, depth+1),)

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
