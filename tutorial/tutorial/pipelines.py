# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from re import findall
import redis
import mariadb


class TutorialPipeline:
    def process_item(self, item, spider):
        item['published_time'] = "".join(findall("\S+", item['published_time']))
        item['title'] = "".join(findall("\S+", item['title']))
        item['seed'] = "".join(findall("\S+", item['seed']))
        item['download_times'] = "".join((findall("\S+", item['download_times'])))
        item['complete_times'] = "".join(findall("\S+", item['complete_times']))
        return item

class MariaDb:
    def __init__(self, maria_url, maria_user, maria_passwd, maria_port, maria_db):
        self.maria_url = maria_url
        self.maria_user = maria_user
        self.maria_passwd = maria_passwd
        self.maria_port = maria_port
        self.maria_db = maria_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            maria_url=crawler.settings.get("maria_url"),
            maria_db=crawler.settings.get("maria_db"),
            maria_port=crawler.settings.get("maria_port"),
            maria_user=crawler.settings.get("maria_user"),
            maria_passwd=crawler.settings.get("maria_passwd")
        )

    def open_spider(self, spider):
        client = mariadb.connect(host=self.maria_url, username=self.maria_user, passwd=self.maria_passwd,
                                      port=self.maria_port, db=self.maria_db)
        self.client = client
        self.cursor = client.cursor()

    def process_item(self, item, spider):
        self.cursor.execute("insert ignore into Bangumi values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            [
                                item['title'], item['complete_times'], item['download_times'], item['_type'],
                                item['author'], item['href'], item['seed'], item['content_length'],
                                item['magnet_link'], item['published_time'], item['title']
                            ])

    def close_spider(self, spider):
        self.client.close()



class RedisSave:
    def __init__(self, redis_url, redis_port, redis_db, redis_passwd):
        self.redis_url = redis_url
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_passwd = redis_passwd

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_url=crawler.settings.get("REDIS_URI"),
            redis_port=crawler.settings.get("REDIS_PORT"),
            redis_db=crawler.settings.get("REDIS_DB"),
            redis_passwd=crawler.settings.get("REDIS_PASSWD"),
        )

    def open_spider(self, spider):
        self.client = redis.Redis(host=self.redis_url, port=self.redis_port, db=self.redis_db, password=self.redis_passwd)

    def process_item(self, item, spider):
        self.client.hsetnx(item['title'], 'published_time', item['published_time'])
        self.client.hsetnx(item['title'], 'seed', item['seed'])
        self.client.hsetnx(item['title'], 'download_times', item['download_times'])
        self.client.hsetnx(item['title'], 'complete_times', item['complete_times'])
        self.client.hsetnx(item['title'], '_type', item['_type'])
        self.client.hsetnx(item['title'], 'href', item['href'])
        self.client.hsetnx(item['title'], 'magnet_link', item['magnet_link'])
        self.client.hsetnx(item['title'], 'content_length', item['content_length'])
        self.client.hsetnx(item['title'], 'author', item['author'])
        return item

    def close_spider(self, spider):
        self.client.close()
