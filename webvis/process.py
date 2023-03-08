from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webvis.spiders.wikipedia import WikipediaSpider
import sys

for line in sys.path:
    print(line)


process = CrawlerProcess(get_project_settings())

process.crawl(WikipediaSpider)
process.start()
