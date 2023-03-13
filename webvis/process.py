from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webvis.spiders.wikipedia import WikipediaSpider
from webvis.utils.name_generator import NameGenerator
from webvis.utils.network import NetworkHelper


def run_crawler_process(
    start_url='https://en.wikipedia.org/wiki/Functor',
    network_groups=4,
    branching_factor=4
):
    name = NameGenerator.from_params(
        start_url=start_url,
        branching_factor=branching_factor
    )

    try:
        print(f'cache hit: {name}')
        net = NetworkHelper.from_cache(name)
        net.pipeline(groups=network_groups, name='test-cache')
        return

    except Exception:
        print(f'cache miss: {name}')
        pass

    # override project-level settings with params
    settings = get_project_settings()
    settings.set('NETWORK_GROUPS', network_groups)

    process = CrawlerProcess(settings)

    # override spider-level attributes with params
    process.crawl(WikipediaSpider,
                  start_url=start_url,
                  branching_factor=branching_factor,
                  filepath=name
                  )

    process.start()


run_crawler_process()
