import re
from threading import Thread

import mariaBb
import kisssub_bgTable
import backGround
import transmission


class Run:

    def __init__(self):
        self.transmission_client = transmission.Transmission()
        self.user_client = backGround.App()
        self.mysql = mariaBb.MariaDB()


    # def follow(self, title: str):
    #     utility_db_search_result = self.user_client.utility_db_search(title)
    #     user_db_search_result = self.user_client.user_db_search(title)
    #     for no, public in enumerate(utility_db_search_result):
    #         if public[1] == utility_db_search_result[0][1] or utility_db_search_result[0][1] - 1:  # 相关读相等或相关度相差小于1
    #             if public[0] not in user_db_search_result:
    #                 print("No: {} {}".format(no, public[0]))
    #     input_list = re.split(' +', input("(split by space ) No:"))
    #     return input_list
    def follow(self, title: str):
        follow_list = self.user_client.follow(title)
        for i in follow_list:
            mapping_i = self.user_client.utility_database.hgetall(i)
            self.download_one(mapping_i[b'magnet_link'].decode())
            self.user_client.user_database.hmset(i, mapping_i)



    def download_one(self, magnet_hash: str):
        from time import sleep
        self.transmission_client.add_torrent(self.transmission_client.magnet_create(magnet_hash))
        sleep(1)

    def download_list(self, download_list: list):
        from time import sleep
        for i in download_list:
            bangumi_objective = self.user_client.user_database.hgetall(i)
            magnet = bangumi_objective['magnet_link']
            self.transmission_client.add_torrent(magnet)
            self.user_client.database_record(i, bangumi_objective)
            sleep(1)


runNow = Run()
while True:
    mode = input("mode 1 follow // 2 bangumi table:")
    if mode == '2':
        bgT_list = kisssub_bgTable.showTable(kisssub_bgTable.getTable("http://www.kisssub.org/addon.php?r=bangumi/table"))
        for uri in bgT_list:
            url = "http://www.kisssub.org/" + uri[1] + '/'
            status_code = runNow.user_client.get_scrapyrt(url)
            print(status_code)
        if input("auto download ? yes/no") == 'yes':
            pass
    elif mode == 'q':
        break

    while True:
        runNow.follow(input("keys: "))
#
# while True:
#     runNow.follow(input("keys: "))