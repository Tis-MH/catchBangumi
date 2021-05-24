# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = scrapy.Field()
    tag = scrapy.Field()
    author = scrapy.Field()


class ZhihuItem(scrapy.Item):
    author = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()

class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class KisssubItem(scrapy.Item):
    published_time = scrapy.Field()
    _type = scrapy.Field()
    title = scrapy.Field()
    content_length = scrapy.Field()
    seed = scrapy.Field()
    download_times = scrapy.Field()
    complete_times = scrapy.Field()
    author = scrapy.Field()
    magnet_link = scrapy.Field()
    href = scrapy.Field()
