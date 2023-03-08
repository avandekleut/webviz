import re
import scrapy
import urllib
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
from bs4 import BeautifulSoup

from urllib.parse import urldefrag

import graphviz
from pyvis.network import Network


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Functor"]

    max_children = 3  # set to 3 for fun

    # TODO: Make these relative
    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        "https://en.wikipedia.org/wiki/*:*",
    ]

    dot = graphviz.Digraph()
    net = Network()

    total_visited = 0
    max_total_visited = 16

    def parse(self, response, meta={}):

        soup = BeautifulSoup(response.text, 'lxml')
        title_class = "mw-page-title-main"
        title = soup.find_all("span", {"class": title_class})[0].getText()
        # print(f'title: {title}')

        parent_title = meta.get('parent_title')
        parent_title = parent_title or None
        # print(f'parent_title: {parent_title}')

        current_url = response.url

        current_path = current_url.split("/wiki/")[-1]
        source_node = urllib.parse.unquote(
            current_path, encoding='utf-8', errors='replace')
        self.net.add_node(source_node)

        outgoing_links = self.get_outgoing_links(response)
        max_visit_count = self.max_children if self.max_children is not None else len(
            outgoing_links)

        print(f'max_visit_count: {max_visit_count}')

        visited_count = 0
        for url in outgoing_links:
            if visited_count >= max_visit_count:
                print(f'cutoff at {visited_count} >= {max_visit_count}')
                # yield
                break

            if self.total_visited >= self.max_total_visited:
                print(
                    f'hard cutoff at {self.total_visited} >= {self.max_total_visited}')
                # print(self.dot.source)
                # self.dot.render('dot.gv', view=True)

                self.net.show('name.html')

                return

            if url == current_url:
                print('same url')
                continue

            if self.should_ignore_path(url):
                # print(f'ignored url: {url}')
                # yield
                continue

            if not self.should_allow_path(url):
                # print(f'url not allowed: {url}')
                # yield
                continue

            visited_count += 1
            self.total_visited += 1
            print(
                f'[{visited_count}/{max_visit_count}] ({self.total_visited}) {title} -> {url}')

            dest_path = url.split("/wiki/")[-1]
            dest_node = urllib.parse.unquote(
                dest_path, encoding='utf-8', errors='replace')
            # self.dot.edge(source_node, dest_node)
            self.net.add_node(dest_node)
            self.net.add_edge(source_node, dest_node)

            yield scrapy.Request(url, callback=self.parse, meta={"parent_title": title})

    def get_outgoing_links(self, response):
        urls = []

        for href in response.xpath('//a/@href').getall():
            url = self.get_full_url(response, href)
            urls.append(url)

        unique_urls = list(set(urls))
        sorted_urls = sorted(unique_urls)

        return sorted_urls

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
