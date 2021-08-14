import requests
import re
# import time
import Config
from bs4 import BeautifulSoup


def getTable(table_url: str):
    html = requests.get(table_url, headers={"User-Agent": Config.RequestConfig.UA},
                        proxies=Config.RequestConfig.proxy)
    if html.status_code != 200:
        raise requests.HTTPError
    html_decode = BeautifulSoup(html.text, "html.parser")
    table = html_decode.select_one("#bgm-table").select("dl")
    content = {}
    for block in table:
        weekday = "".join(re.findall("\S+", block.select_one("dt").text))
        bangumi_list = []
        for item in block.select("dd"):
            href = re.search("href=\"(.+?)\"", str(item))[1]
            atom = ("".join(re.findall("\S+", item.text)), href)
            bangumi_list.append(atom)
        content.setdefault(weekday, bangumi_list)
    return content


def showTable(bangumi_list: dict):
    temp = []
    ret_list = []
    x = 0
    for week, week_content in zip(bangumi_list.keys(), bangumi_list.values()):
        print(week)
        for name in week_content:
            print("no: {}\t{}".format(str(x), name[0]))
            x += 1
            temp.append((x, name))

        print()
    inp = input("no:")
    inp_list = set(re.split(' +', inp))
    for i in inp_list:
        ret_list.append(temp[int(i)][1])
    return ret_list



if __name__ == '__main__':
    # print(getTable("http://www.kisssub.org/addon.php?r=bangumi/table"))
    ret = showTable(getTable("http://www.kisssub.org/addon.php?r=bangumi/table"))
    print(ret)
