"""
数据库模型
env: python3.6
author Feo
function: 为服务端提供数据交互
"""
import hashlib
import pymysql


# 密码加密
def change_passwd(passwd):
    # hash对象
    hash = hashlib.md5('*#06#'.encode())  # 加盐生产对象
    # 对密码进行加密
    hash.update(passwd.encode())
    return hash.hexdigest()


class YunDictModel:
    def __init__(self, host='localhost',
                 port=3306,
                 user=None,
                 passwd=None,
                 database=None,
                 charset='utf8'
                 ):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()

    def connect_db(self):
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.passwd,
            database=self.database,
            charset=self.charset
        )

    # 创建游标
    def create_cursor(self):
        self.cur = self.db.cursor()

    # 关闭数据库
    def close(self):
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'db'):
            self.db.close()

    def register(self, name, passwd):
        # 判断名字是否重复
        sql = "select name from user where name = %s"
        self.cur.execute(sql, [name])
        result = self.cur.fetchone()  # 查不到返回None
        if result:
            return False
        try:
            passwd = change_passwd(passwd)
            sql = "insert into user (name, password) values(%s, %s)"
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def login(self, name, passwd):
        passwd = change_passwd(passwd)
        sql = "SELECT name FROM user WHERE name = %s AND password = %s"
        self.cur.execute(sql, [name, passwd])
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    def query(self, word):
        sql = "select mean from words where word = '%s'" % word
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return result[0]

    def insert_history(self, name, word):
        sql = "select id from user where name = %s"
        self.cur.execute(sql, [name])
        uid = self.cur.fetchone()
        sql = "select id from words where word = %s"
        self.cur.execute(sql, [word])
        wid = self.cur.fetchone()
        sql = "insert into user_words (uid, wid) values(%s, %s)"
        try:
            self.cur.execute(sql, [uid, wid])
            self.db.commit()
        except:
            self.db.rollback()

    # 查询历史记录
    def history(self, name):
        sql = "select word, h.time from words inner join " \
              "(select wid, time from user_words where uid = (" \
              "select id from user where name = %s) order by time desc limit 10) as h " \
              "on words.id = h.wid"
        self.cur.execute(sql, [name])
        return self.cur.fetchall()


if __name__ == '__main__':
    db = YunDictModel(user='root', passwd='123456', database='dict')
    name = input("name>>")
    passwd = input("passwd>>")
    db.register(name, passwd)
