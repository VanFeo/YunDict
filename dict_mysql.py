"""
env: python3.6
author: Feo
function: 将dict.txt中的单词插入到数据库
"""
import re
import pymysql


def get_list_dict(file):
    list_ = []
    with open(file) as f:
        for line in f:
            # word = line.split(' ', 1)[0]
            # mean = (line.split(' ', 1)[1]).strip(' ')
            # list_.append((word, mean))
            result = re.findall(r'(\S+)\s+(.*)', line)
            list_.extend(result)
    return list_


def main(file):
    db = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='123456',
        database='dict',
        charset='utf8'
    )
    cur = db.cursor()
    list_ = get_list_dict(file)
    sql = "INSERT INTO words (word, mean) VALUES(%s, %s)"
    try:
        cur.executemany(sql, list_)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    cur.close()
    db.close()


if __name__ == '__main__':
    file = 'dict.txt'
    main(file)
