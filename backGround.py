import redis
import re
import time
import yaml
import requests
import Config
import transmission
from Config import AppConfig
from threading import Thread

yaml_config = yaml.safe_load(open('Config.yaml', encoding='utf-8').read())


def log_to_mission_json(key: str, content: list):
    mission_json = json.loads(open(yaml_config['AppConfig']['mission_json_path'], encoding='utf-8').read())  # todo 过度依赖文件
    mission_json['mission'][key] = content
    with open(yaml_config['AppConfig']['mission_json_path'], 'w', encoding='utf-8') as file:
        file.write(json.dumps(mission_json, ensure_ascii=False))  # 同上


class Title:
    title = ''
    author = ''
    name = ''
    episode = ''
    coding_type = ''
    resolution = ''
    lang = ''

    def __init__(self, title):
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
    utility_database_sort_result: list

    def __init__(self):
        self.config = AppConfig()
        self.utility_database = redis.Redis(host=self.config.utility_database_uri,
                                            port=self.config.utility_database_port,
                                            db=self.config.utility_database_no, password="861238abcABCO")

        self.user_database = redis.Redis(host=self.config.user_database_uri, port=self.config.user_database_port,
                                         db=self.config.user_database_no, password="861238abcABCO")

        utility_database_sort_result = Thread(target=self.redis_keys_list, args=(self.utility_database,))
        self.thread1 = utility_database_sort_result
        utility_database_sort_result.start()

    def get_sort_result(self):
        utility_database_sort_result = Thread(target=self.redis_keys_list, args=(self.utility_database,))
        self.thread1 = utility_database_sort_result
        utility_database_sort_result.start()

    def redis_keys_list(self, redis_db: redis.Redis):
        # 提前将redis 中 key list 存入类变量 utility_database_sort_result 中
        # 防止搜索时占用太多时间
        ret_list = []
        cursor = 0
        while True:
            ret = redis_db.scan(cursor, count=1000)
            ret_list = ret_list + ret[1]
            cursor = ret[0]
            if ret[0] == 0:
                break
        self.utility_database_sort_result = ret_list

    def sortDBsearch(self, search_text: str, title_list: list):  # 对搜索关联度排序
        split_list = re.split('[,|.|\||\[|\]|【|】| +|_]', search_text)

        def count(x):
            temp = x.decode()
            times = 0
            for i in split_list:
                if i == '':
                    continue
                if i in temp:
                    times += 1
            return temp, times

        result_list = list(map(count, title_list))
        get = lambda x: x[1]
        result_list.sort(key=get, reverse=True)
        return result_list

    def search(self, title: Title) -> list:  # 组合字段并搜索
        search_title = title.compose()
        print(search_title)
        return self.utility_database.keys(search_title)

    def database_record(self, title: Title, mapping: dict):  # 记录哈希对 值为dict
        self.user_database.hset(title, mapping)

    def follow(self, title: str):
        utility_db_search_result = self.utility_db_search(title)
        user_db_search_result = self.user_db_search(title)
        for no, public in enumerate(utility_db_search_result):
            if public[1] == utility_db_search_result[0][1]:  # 相关度相等或相关度相差小于1
                if public[0] not in user_db_search_result:
                    print("\nNo: {} {}".format(no, public[0]))
        inp = input("(split by space ) No:")
        if inp == "q":
            return []
        input_list = set(re.split(' +', inp))
        ret_list = []
        for i in input_list:
            ret_list.append(utility_db_search_result[int(i)][0])
        return ret_list

    def subscribe_one(self, key: str, mission: list) -> str:
        mission_length = len(mission)
        compare_mission_list = []  # 具有匹配符用于匹配的list
        for index in range(len(mission)):
            res = re.search("@#0(\d+)#@", mission[index])
            if res:
                compare_mission_list.append(re.sub("@#0\d+#@", "@#0{}#@".format(int(res[1]) + 1), mission[index]))
                mission[index] = re.sub("@#0\d+#@", "0{}".format(int(res[1]) + 1), mission[index])

            res = re.search("@#(\d+)#@", mission[index])
            if res:
                compare_mission_list.append(re.sub("@#\d+#@", "@#{}#@".format(int(res[1]) + 1), mission[index]))
                mission[index] = re.sub("@#\d+#@", "{}".format(int(res[1]) + 1), mission[index])
            # mission[index] = re.sub("@#0\d+#@", "0{}".format(int(re.search("@#0(\d+)#@", mission[index])[1]) + 1), mission[index])
            # mission[index] = re.sub("@#\d+#@", "{}".format(int(re.search("@#(\d+)#@", mission[index])[1]) + 1), mission[index])
        index = 0
        while True:  # 找标题相等的
            res = self.utility_database.hget(mission[index], 'magnet_link')
            if res:
                log_to_mission_json(key, mission)
                print(mission[index])
                return res

            else:
                index = index + 1
            if index == mission_length:
                index = 0
                break
        while True:  # 找标题包含的
            search_result = list(map(lambda x: x[0], self.utility_db_search(mission[index])))
            if len(search_result) == 1:
                if mission[index] in search_result:
                    log_to_mission_json(key, compare_mission_list)
                    print(mission[index])
                    return str(self.utility_database.hget(mission[index], 'magnet_link'))
            elif len(search_result) == 0:
                break
            else:
                index = index + 1
            if index == mission_length:
                break
        # todo 没有任何匹配项, 通知用户

    def subscribe_all(self) -> list:  # todo 优化出现完结情况
        ret_list = []
        mission = json.loads(open(yaml_config['mission_json_path'], encoding='utf-8').read())
        mission_mission = mission['mission']
        for key in mission_mission.keys():
            ret_list.append(self.subscribe_one(key, mission_mission[key]))
        return ret_list


    def utility_db_search(self, search_text):  # [(name, asociation), ()...]
        split_list = re.split('[,|.|\||\[|\]|【|】| +|_]', search_text)

        def count(x):
            temp = x.decode()
            times = 0
            for i in split_list:
                if i == '':
                    continue
                if i in temp:
                    times += 1
            return temp, times

        print("wait thread")
        start = time.time()
        self.thread1.join()
        print("done use: " + str(time.time() - start))
        result_list = list(map(count, self.utility_database_sort_result))
        get = lambda x: x[1]
        result_list.sort(key=get, reverse=True)
        return result_list

    def user_db_search(self, search_text: str):
        split_list = re.split('[,|.|\||\[|\]|【|】| +|_]', search_text)

        def count(x):
            temp = x.decode()
            times = 0
            for i in split_list:
                if i == '':
                    continue
                if i in temp:
                    times += 1
            return temp, times

        result_list = list(map(count, self.user_database.keys()))
        get = lambda x: x[1]
        result_list.sort(key=get, reverse=True)
        return result_list

    def create_redis_index(self):  # 创建 redis 索引
        key_list = self.utility_database.keys()
        index = 0
        no = 0
        string = ""
        for i in key_list:
            if "length_15000_index_" in i.decode():
                continue
            string = "{}{}{}".format(string, "\n", i.decode())

            print(no, index)
            if no == 15000:
                self.utility_database.set("length_15000_index_" + str(index), string)
                string = ""
                no = 0
                index = index + 1
            no = no + 1
        if len(key_list) < 15000:
            self.utility_database.set("length_15000_index_" + str(index), string)

    def get_scrapyrt(self, href_list):
        if type(href_list) == list:
            for url in href_list:
                response = requests.get(
                    "http://{}:9080/crawl.json?spider_name=kisssub&url={}".format(Config.AppConfig.scrapyrt_ip, url))
        else:
            response = requests.get(
                "http://{}:9080/crawl.json?spider_name=kisssub&url={}".format(Config.AppConfig.scrapyrt_ip, href_list))
        return response  # 原为response.status_code


class AdminApp(App):

    def database_remove(self, title: Title):
        pass

    def database_change(self, title: Title):
        pass


if __name__ == '__main__':
    app = App()
    import json

    print(app.subscribe_one('青梅竹马绝对不会输的恋爱喜剧',
                            json.loads(open("etc/mission.json", encoding='utf-8').read())['mission']['青梅竹马绝对不会输的恋爱喜剧']))
    # print(app.follow("86 不存在的战区 01"))
    # app.create_redis_index()
