import scrapy


class WikipediaSpider(scrapy.Spider):
    """Wikipedia Spider

    Args:
        scrapy (_type_): _description_
    """
    name = 'wikipedia'
    start_urls = ['https://en.wikipedia.org/wiki/Functor']
    allowed_domains = ['en.wikipedia.org']

    def parse(self, response, depth=0):

        for next_page in response.css('a.next'):
            next_response = response.follow(next_page, self.parse)
            self.parse(next_response, depth + 1)
