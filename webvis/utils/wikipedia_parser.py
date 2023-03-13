import urllib
from urllib.parse import urldefrag


class WikipediaParser:
    def __init__(self, response):
        self.response = response
        self.url = response.url

    def get_urls(self):
        hrefs = self.response.xpath('//a/@href').getall()
        full_urls = map(self.href_to_full_url, hrefs)
        return full_urls

    def href_to_full_url(self, href):
        url = self.response.urljoin(href)
        unfragmented = urldefrag(url)[0]  # remove anchors, etc
        return unfragmented

    def get_title_from_url(self, url=None):
        url = url or self.url

        wiki_path = url.split("/wiki/")[-1]

        decoded = urllib.parse.unquote(
            wiki_path, encoding='utf-8', errors='replace')

        pretty = decoded.replace("_", " ")

        return pretty
