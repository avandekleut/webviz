import re
import scrapy

from collections import defaultdict

from bs4 import BeautifulSoup

from urllib.parse import urldefrag

from pyvis.network import Network
import graphviz


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Functor"]

    max_depth = 1
    max_children = 1

    # TODO: Make these relative
    allowed_paths = [
        "https://en.wikipedia.org/wiki/*",
    ]

    ignore_paths = [
        "https://en.wikipedia.org/wiki/*:*",
    ]

    network = Network()

    dot = graphviz.Digraph()

    total_visited = 0

    def parse(self, response, meta={}):

        soup = BeautifulSoup(response.text, 'lxml')
        title_class = "mw-page-title-main"
        title = soup.find_all("span", {"class": title_class})[0].getText()
        # print(f'title: {title}')

        depth = meta.get('depth')
        depth = depth or 0
        # print(f'depth: {depth}')

        parent_title = meta.get('parent_title')
        parent_title = parent_title or None
        # print(f'parent_title: {parent_title}')

        if depth >= self.max_depth:
            # print(f'reached max depth of {depth}')
            return

        current_url = response.url

        self.network.add_node(current_url)
        # self.dot.node(current_url)

        outgoing_links = self.get_outgoing_links(response)
        max_visit_count = self.max_children if self.max_children is not None else len(
            outgoing_links)

        print(f'num_outgoing_links: {max_visit_count}')

        # print(f'found {len(outgoing_links)} outgoing links')

        visited_count = 0
        for url in outgoing_links:
            if visited_count >= max_visit_count:
                print(f'cutoff at {visited_count} >= {max_visit_count}')
                # yield
                break

            if self.should_ignore_path(url):
                # print(f'ignored url: {url}')
                # yield
                continue

            if not self.should_allow_path(url):
                # print(f'url not allowed: {url}')
                # yield
                continue

            visited_count += 1
            print(
                f'({depth}) [{visited_count}/{max_visit_count}] {title} -> {url}')
            # print(f'creating edge {current_url}, {url}')

            self.network.add_node(url)
            # self.dot.node(url)

            self.network.add_edge(current_url, url)
            self.dot.edge(current_url, url)
            # print(f'creating edge {current_url}, {url}')

            yield scrapy.Request(url, callback=self.parse, meta={'depth': depth+1, "parent_title": title})

        if depth == 0:
            print('done')
            print(self.dot.source)
            # self.dot.render('dot.gv', view=True)
            return
            # print(self.network)
            # self.network.toggle_physics(True)
            # self.network.show('graph.html', notebook=False)
            # print(self.network.get_adj_list())
            # print(self.network.dot_lang)

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
