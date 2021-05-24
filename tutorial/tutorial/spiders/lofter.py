import scrapy
from tutorial.items import TutorialItem


class LofterSpider(scrapy.Spider):
    name = 'lofter'
    allowed_domains = ['www.lofter.com']
    start_urls = ['http://www.lofter.com/']

    def parse(self, response):
        m_list = response.css('.m-mlist')
        for m in m_list:
            content = m.css(".m-mlist::img").extract_first()
            author = m.css(".m-mlist::.publishernick ")
        a = QuoteItem()
        yield author