from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webvis.spiders.wikipedia import WikipediaSpider
from webvis.utils.filepath_utils import FilepathUtils
from webvis.utils.network import NetworkHelper


def run_crawler_process(
    start_url='https://en.wikipedia.org/wiki/Functor',
    network_groups=2,
    branching_factor=4
):
    cache_filepath = FilepathUtils.generate_filepath(
        start_url=start_url,
        branching_factor=branching_factor
    ) + '.nx'

    try:
        net = NetworkHelper.from_cache(cache_filepath)
        net.pipeline(groups=network_groups, filepath='test-cache')
        print(f'cache hit: {cache_filepath}')
        return

    except Exception:
        print(f'cache miss: {cache_filepath}')
        pass

    # override project-level settings with params
    settings = get_project_settings()
    settings.set('NETWORK_GROUPS', network_groups)

    process = CrawlerProcess(settings)

    # override spider-level attributes with params
    process.crawl(WikipediaSpider,
                  start_url=start_url,
                  branching_factor=branching_factor,
                  filepath=cache_filepath
                  )

    process.start()


run_crawler_process()
