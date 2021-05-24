import redis
import re
import transmission
from Config import AppConfig


class Title:
    title = ''
    author = ''
    name = ''
    episode = ''
    coding_type = ''
    resolution = ''
    lang = ''

    def __init__(self, title) -> None:
        self.title = title

    def compose(self):
        return_text = '*'
        for i in self.__dict__.values():
            if i != '':
                return_text = return_text + i + "*"
        return return_text


class Bangumi(Title):
    title: str
    complete_times: str
    href: str
    magnet_link: str
    download_times: str
    seed: str
    published_time: str
    content_length: str
    author: str
    _type: str

    def __init__(self, title: str, bangumi: dict) -> None:
        super().__init__(title)
        self.title = title
        self.complete_times = bangumi['complete_times']
        self.href = bangumi['href']
        self.magnet_link = bangumi['magnet_link']
        self.download_times = bangumi['download_times']
        self.seed = bangumi['seed']
        self.published_time = bangumi['published_time']
        self.content_length = bangumi['content_length']
        self.author = bangumi['author']
        self._type = bangumi['_type']


class App:

    def __init__(self):
        self.config = AppConfig()
        self.utility_database = redis.Redis(host=self.config.utility_database_uri,
                                            port=self.config.utility_database_port,
                                            db=self.config.utility_database_no, password="861238abcABCO")

        self.user_database = redis.Redis(host=self.config.user_database_uri, port=self.config.user_database_port,
                                         db=self.config.user_database_no, password="861238abcABCO")

    def search(self, title: Title) -> list:
        search_title = title.compose()
        print(search_title)  #############
        return self.utility_database.keys(search_title)

    def database_record(self, title: Title, mapping: dict):
        self.user_database.hset(title, mapping)

    def follow(self, title: str):
        utility_db_search_result = self.utility_db_search(title)
        user_db_search_result = self.user_db_search(title)
        for no, public in enumerate(utility_db_search_result):
            if public[1] == utility_db_search_result[0][1]:  # 相关读相等或相关度相差小于1
                if public[0] not in user_db_search_result:
                    print("\nNo: {} {}".format(no, public[0]))
        input_list = set(re.split(' +', input("(split by space ) No:")))
        ret_list = []
        for i in input_list:
            ret_list.append(utility_db_search_result[int(i)][0])
        return ret_list

    def utility_db_search(self, search_text):
        result_list = []
        split_list = re.split('[,|.|\||\[|\]|【|】| +|_]', search_text)
        for item in self.utility_database.keys():
            times = 0
            for i in split_list:
                if i == '':
                    continue
                if i not in item.decode():
                    continue
                else:
                    times = times + 1
            result_list.append((item.decode(), times))
            get = lambda x: x[1]
            result_list.sort(key=get, reverse=True)
        return result_list

    def user_db_search(self, search_text):
        result_list = []
        split_list = re.split('[,|.|\||\[|\]|【|】| |_]', search_text)
        for item in self.user_database.keys():
            times = 0
            for i in split_list:
                if i == '':
                    continue
                if i not in item.decode():
                    continue
                else:
                    times = times + 1
            result_list.append((item.decode(), times))
            get = lambda x: x[1]
            result_list.sort(key=get, reverse=True)
        return result_list


class AdminApp(App):

    def database_remove(self, title: Title):
        pass

    def database_change(self, title: Title):
        pass
