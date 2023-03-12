from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webvis.spiders.wikipedia import WikipediaSpider


def run_crawler_process(
    start_url='https://en.wikipedia.org/wiki/Functor',
    network_groups=6,
    branching_factor=4
):
    # override project-level settings with params
    settings = get_project_settings()
    settings.set('NETWORK_GROUPS', network_groups)

    process = CrawlerProcess(settings)

    # override spider-level attributes with params
    process.crawl(WikipediaSpider,
                  start_url=start_url,
                  branching_factor=branching_factor)

    process.start()


run_crawler_process()
