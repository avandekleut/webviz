import urllib
from urllib.parse import urldefrag
from pyvis.network import Network

import networkx as nx
from networkx.algorithms.community.centrality import girvan_newman


class WikipediaParser:
    def __init__(self, response):
        self.response = response
        self.url = response.url

    def get_urls(self):
        print('get_urls')
        hrefs = self.response.xpath('//a/@href').getall()
        urls = []
        for href in hrefs:
            print('href', href)
            url = self.href_to_full_url(href)
            print('url', url)
            urls.append(url)
        return urls

    def href_to_full_url(self, href):
        url = self.response.urljoin(href)
        unfragmented = urldefrag(url)[0]  # remove anchors, etc
        return unfragmented

    def get_title(self, url=None):
        url = url or self.url

        wiki_path = url.split("/wiki/")[-1]

        decoded = urllib.parse.unquote(
            wiki_path, encoding='utf-8', errors='replace')

        pretty = decoded.replace("_", " ")

        return pretty
