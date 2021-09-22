import re

import scrapy
import datetime
from tutorial.items import KisssubItem
from bs4 import BeautifulSoup
from re import search, findall


class KisssubSpider(scrapy.Spider):
    name = 'kisssub'
    allowed_domains = ['www.kisssub.org']
    start_urls = ['http://www.kisssub.org/search.php?keyword=%E6%AD%BB%E7%A5%9E%E5%B0%91%E7%88%B7%E4%B8%8E%E9%BB%91%E5%A5%B3%E4%BB%86']

    def parse(self, response):
        content = response.css("#data_list").extract_first()
        td_list = BeautifulSoup(content, "html.parser").select("td")
        for one in range(50):
            kiss = KisssubItem()
            published_date = td_list[0 + one * 8].text
            if '今天' in published_date:
                published_date = str(datetime.date.today()).replace('-', '/')
            elif '昨天' in published_date:
                published_date = str(datetime.date.today() - datetime.timedelta(days=1)).replace('-', '/')
            elif '前天' in published_date:
                published_date = str(datetime.date.today() - datetime.timedelta(days=2)).replace('-', '/')
            kiss['published_time'] = published_date
            kiss['_type'] = td_list[1 + one * 8].text
            kiss['title'] = td_list[2 + one * 8].text
            kiss['href'] = "http://www.kisssub.org/" + search("href=\"(.+?)\"", str(td_list[2 + one * 8]))[1]
            # magnet_request = scrapy.Request(url=kiss['href'], callback=self.parse2)  # 2021/8/14改进, 直接从href中取
            # magnet_request.meta['kiss'] = kiss　　# 同上
            kiss['magnet_link'] = re.search("show-(.+?).html", kiss['href'])[1]  # kiss['magnet_link'] = magnet_request
            kiss['content_length'] = td_list[3 + one * 8].text
            kiss['seed'] = td_list[4 + one * 8].text
            kiss['download_times'] = td_list[5 + one * 8].text
            kiss['complete_times'] = td_list[6 + one * 8].text
            kiss['author'] = td_list[7 + one * 8].text
            yield kiss  # magnet_request
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
