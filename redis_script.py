import redis
from re import findall
import re
import time
from threading import Thread

client = redis.Redis("120.78.140.25", 6379, 0, password="861238abcABCO")
user_client = redis.Redis("192.168.1.104", 6379, 0, password="861238abcABCO")

def func(start, end, match="*悠哈璃羽字幕社*"):
    a = client.scan(start, match, end)
    for_scan(a)

def for_scan(a):
    for i in a[1]:
        print(i.decode())


class getIndex(Thread):
    def __init__(self, no):
        super().__init__()
        self.no = no

    def func(self, no):
        self.result = client.smembers("length_3000_index_" + str(no))
        print(type(self.result))


    def run(self) -> None:
        self.func(self.no)

    def get_result(self):
        return self.result

def delIndex():
    key_list = client.keys()
    for i in key_list:
        if "length_300_index_" in i.decode():
            client.delete(i)

def getHlist():
    id = 'id'.encode()
    dbsize = client.dbsize()
    length = dbsize/15000
    if length < 1:
        length = 1
    elif length > dbsize//15000:
        length = int(length) + 1
    else:
        length = int(length)
    for i in range(0, length):

        yield client.get("length_15000_index_" + str(i))
        print(1)

def search():
    start = time.time()
    lt = []
    for i in getHlist():

        lt = lt + i.decode().splitlines()

    return lt

def user_db_search(self, search_text):
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
    result_list = list(map(count, search()))
    get = lambda x: x[1]
    result_list.sort(key=get, reverse=True)
    return result_list

def scan():
    ret_list = []
    cursor = 0
    while True:
        ret = client.scan(cursor, count=1000)
        ret_list = ret_list + ret[1]
        cursor = ret[0]
        if ret[0] == 0:
            break
    return ret_list






    # print("use: ", time.time() - start)

# getHlist()
scan()
# a = client.keys()
# for i in a:
#     print(client.ttl(i))
# print(a)