import scrapy
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quote_list = response.css(".quote")
        for i in quote_list:
            text = i.css(".text::text").extract_first()
            author = i.css(".author::text").extract_first()
            tags = i.css(".author::text").extract_first()
            obj = QuoteItem()
            obj['text'] = text
            obj['tags'] = tags
            obj['author'] = author
            yield obj
        next = response.css(".pager .next a::attr('href')").extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)


