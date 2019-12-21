"""
服务端
env: python3.6
author: Feo
Model: 多进程TCP并发  Controller
"""
from socket import *
import signal, sys, time
from multiprocessing import Process
from dbmodel import YunDictModel

# 全局变量
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)
# 生成数据库连接对象
db = YunDictModel(user='root', passwd='123456', database='dict')


def register(connfd, name, passwd):
    if db.register(name, passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')


def login(connfd, name, passwd):
    if db.login(name, passwd):
        connfd.send(b'OK')
    else:
        connfd.send(b'FAIL')


def query(connfd, name, word):
    mean = db.query(word)  # 负责查询单词
    # 查不到返回空
    if mean:
        msg = "%s: %s" % (word, mean)
        connfd.send(msg.encode())
        # 插入历史记录
        db.insert_history(name, word)
    else:
        connfd.send("没有查询结果".encode())


# 处理客户端请求
def history(connfd, name):
    r = db.history(name)
    if not r:
        connfd.senf(b'FAIL')
        return
    connfd.send(b'OK')
    for word, tm in r:
        time.sleep(0.1)
        msg = "%s   %-16s    %s" % (name, word, tm)
        connfd.send(msg.encode())
    time.sleep(0.1)
    connfd.send(b'##')


def request(connfd):
    db.create_cursor()
    while True:
        msg = connfd.recv(1024).decode()
        tmp = msg.split(' ')
        if not msg or tmp[0] == 'E':
            return
        # R name passwd
        if tmp[0] == 'R':
            register(connfd, tmp[1], tmp[2])
        # L name passwd
        elif tmp[0] == 'L':
            login(connfd, tmp[1], tmp[2])
        # Q name word
        elif tmp[0] == 'Q':
            query(connfd, tmp[1], tmp[2])
        # H name
        elif tmp[0] == 'H':
            history(connfd, tmp[1])


def main():
    # 创建TCP套接字
    sockfd = socket()
    # 设置端口重用
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(3)
    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    # 循环接受客户端请求连接
    print("Listen the port 8888...")

    while True:
        try:
            connfd, addr = sockfd.accept()
            print("Connect From:", addr)
        except KeyboardInterrupt:
            db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建进程
        p = Process(target=request, args=(connfd,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
