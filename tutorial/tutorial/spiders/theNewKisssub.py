import scrapy
from scrapy import exceptions
import datetime
import re
from re import search, findall
from bs4 import BeautifulSoup
from tutorial.items import KisssubItem

class ThenewkisssubSpider(scrapy.Spider):
    name = 'theNewKisssub'
    allowed_domains = ['kisssub.org']
    start_urls = ['http://kisssub.org/']

    def parse(self, response):
        content = response.css("#data_list").extract_first()
        td_list = BeautifulSoup(content, "html.parser").select("td")
        for one in range(50):  # 一页50条
            kiss = KisssubItem()
            published_date = td_list[0 + one * 8].text
            if '今天' in published_date:
                published_date = str(datetime.date.today()).replace('-', '/')
            elif '昨天' in published_date:
                published_date = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '/')
            else:
                raise exceptions.CloseSpider("crawl Done")
            kiss['published_time'] = published_date
            kiss['_type'] = td_list[1 + one * 8].text
            kiss['title'] = td_list[2 + one * 8].text
            kiss['href'] = "http://www.kisssub.org/" + search("href=\"(.+?)\"", str(td_list[2 + one * 8]))[1]
            # magnet_request = scrapy.Request(url=kiss['href'], callback=self.parse2)  # 2021/8/14改进, 直接从href中取
            # magnet_request.meta['kiss'] = kiss　　# 同上
            kiss['magnet_link'] = re.search("show-(.+?).html", kiss['href'])[1]
            kiss['content_length'] = td_list[3 + one * 8].text
            kiss['seed'] = td_list[4 + one * 8].text
            kiss['download_times'] = td_list[5 + one * 8].text
            kiss['complete_times'] = td_list[6 + one * 8].text
            kiss['author'] = td_list[7 + one * 8].text
            yield kiss  # 改进前为magnet_request
        # try:
        #     next_ = response.css("a.nextprev::attr('href')").extract()[0]
        #
        # except IndexError:
        #     # self.crawler.engine.close_spider(self, '\n\n\n\n\n')
        #     try:
        #         next_ = response.css("a.nextprev::attr('href')").extract()[1]
        #     except IndexError:
        #         self.crawler.engine.close_spider(self, "\n")
        # url = response.urljoin(next_)

        href_list = response.css(".nextprev").getall()
        for href in href_list:
            if "〉" in href:
                try:
                    url = re.search("href=\"(.+?)\"", href)[1]
                    url = url.replace("&amp;", "&")
                    url = response.urljoin(url)
                    # with open("record.txt", 'w', encoding='utf-8') as file:
                    #     file.write(url)
                    yield scrapy.Request(url=url, callback=self.parse)
                except IndexError:
                    self.crawler.engine.close_spier(self, '\n')

    def parse2(self, response):
        kiss = response.meta['kiss']
        kiss['magnet_link'] = findall("\w+", response.css("#text_hash_id").extract_first())[4]
        yield kiss

