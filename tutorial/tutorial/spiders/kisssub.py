import scrapy
from tutorial.items import KisssubItem
from bs4 import BeautifulSoup
from re import search, findall


class KisssubSpider(scrapy.Spider):
    name = 'kisssub'
    allowed_domains = ['www.kisssub.org']
    start_urls = ['http://www.kisssub.org/team-1-1.html']

    def parse(self, response):
        content = response.css("#data_list").extract_first()
        td_list = BeautifulSoup(content, "html.parser").select("td")
        for one in range(50):
            kiss = KisssubItem()
            kiss['published_time'] = td_list[0 + one * 8].text
            kiss['_type'] = td_list[1 + one * 8].text
            kiss['title'] = td_list[2 + one * 8].text
            kiss['href'] = "http://www.kisssub.org/" + search("href=\"(.+?)\"", str(td_list[2 + one * 8]))[1]
            magnet_request = scrapy.Request(url=kiss['href'], callback=self.parse2)
            magnet_request.meta['kiss'] = kiss
            kiss['magnet_link'] = magnet_request
            kiss['content_length'] = td_list[3 + one * 8].text
            kiss['seed'] = td_list[4 + one * 8].text
            kiss['download_times'] = td_list[5 + one * 8].text
            kiss['complete_times'] = td_list[6 + one * 8].text
            kiss['author'] = td_list[7 + one * 8].text
            yield magnet_request
        try:
            next_ = response.css("a.nextprev::attr('href')").extract()
            if len(next_) == 1:
                next_ = next_[0]
            elif len(next_) == 2:
                next_ = next_[1]
            else:
                raise IndexError

        except IndexError:
            self.crawler.engine.close_spider(self, '\n\n\n\n\n')
        url = response.urljoin(next_)
        with open("record.txt", 'w', encoding='utf-8') as file:
            file.write(url)
        yield scrapy.Request(url=url, callback=self.parse)


    def parse2(self, response):
        kiss = response.meta['kiss']
        kiss['magnet_link'] = findall("\w+", response.css("#text_hash_id").extract_first())[4]
        yield kiss
