import re
import scrapy

from collections import defaultdict


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Functor"]

    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        "https://en.wikipedia.org/wiki/*:*",
    ]

    adjacency_matrix = defaultdict(set)

    def parse(self, response, depth=0):
        if self.should_ignore_path(response.url):
            return None

        if not self.should_allow_path(response.url):
            return None

        print(f'{depth} - {response.url}')

        for href in response.xpath('//a/@href').getall():
            self.adjacency_matrix[href].add(href)

            yield scrapy.Request(response.urljoin(href), lambda response: self.parse(response, depth+1),)

    def should_ignore_path(self, path):
        return self.filter_paths_by_pattern(path, self.ignore_paths)

    def should_allow_path(self, path):
        return self.filter_paths_by_pattern(path, self.allowed_paths)

    def filter_paths_by_pattern(self, path, patterns):
        for pattern in patterns:
            regular_expression = re.escape(pattern)
            if re.match(regular_expression, path):
                return True

        return False

    def wildcard_to_regular_expression(self, path):
        return re.escape(path).replace('\*', '.+')


def test_wildcard_to_regular_expression():
    spider = WikipediaSpider('wikipedia')
    assert spider.wildcard_to_regular_expression('abc*') == 'abc.+'
