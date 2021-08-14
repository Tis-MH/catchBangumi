import sqlite3

class SqliteDB:
    def __init__(self, db_path):
        db = sqlite3.connect(db_path)
        self.cursor = db.cursor()

    def select(self, string):
        sql = "select * from Bangumi where Title REGEXP ?"
        print(sql)
        cursor = self.cursor.execute(sql, ['".+魔王.+少女.+"'])
        a = cursor.fetchall()
        for i in a:
            print(i)



if __name__ == '__main__':
    db = SqliteDB("D://coding//java//maven_test//test.db")
    # db.select(".+魔王.+少女.+")