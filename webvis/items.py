# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebvisItem(scrapy.Item):
    source_title = scrapy.Field()
    source_url = scrapy.Field()
    dest_url = scrapy.Field()
