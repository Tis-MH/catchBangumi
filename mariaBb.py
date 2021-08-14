import mariadb

class MariaDB:
    def __init__(self):
        self.client = mariadb.connect(host="120.78.140.25", username="root", passwd="861238abcABCO", port=3306, db="Bangumi")
        self.cursor = self.client.cursor()



def test():
    import time
    a = time.time()
    db = mariadb.connect(host="120.78.140.25", username="root", passwd="861238abcABCO", port=3306, db="Bangumi")
    cursor = db.cursor()
    # cursor.execute("select Title from Bangumi")
    # cursor.execute("select Title, magnet_link from Bangumi where Title regexp ?", [".+魔王.+"])
    # print(cursor.fetchall())
    print("link to db use: " + str(time.time() - a))
    return cursor


def interactTest():
    import time
    cursor = test()
    while True:
        sql = input("select sql: ")
        if sql == "q":
            break
        try:
            start = time.time()
            cursor.execute(sql)

            ret = cursor.fetchones()
            print(ret)
            ret = cursor.fetchones()
            print(ret)
            print("execute sql use: " + str(time.time() - start))
        except Exception as e:
            print(e)


if __name__ == '__main__':

    # db = mariadb.connect(host="120.78.140.25", username="root", passwd="861238abcABCO", port=3306, db="Bangumi")
    # cursor = db.cursor()
    # cursor.execute("select Title from Bangumi")
    # # cursor.execute("select Title, magnet_link from Bangumi where Title regexp ?", [".+魔王.+"])
    # print(cursor.fetchall())
    # test()
    interactTest()