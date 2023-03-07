import scrapy


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Functor"]

    def parse(self, response,):
        self.logger.warn('A response from %s just arrived!', response.url)
        for href in response.xpath('//a/@href').getall():
            yield scrapy.Request(response.urljoin(href), self.parse,)
