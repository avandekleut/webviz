from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webvis.spiders.wikipedia import WikipediaSpider


process = CrawlerProcess(get_project_settings())
process.crawl(WikipediaSpider,
              start_url='https://en.wikipedia.org/wiki/Functor',
              children=2)
process.start()
