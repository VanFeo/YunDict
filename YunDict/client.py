"""
用户端
env: python3.6
author: Feo
Model: 多进程TCP发  Viewer
"""
import sys
from getpass import getpass
from socket import *

ADDR = ('127.0.0.1', 8888)
# 创建TCP套接字
sockfd = socket()
try:
    sockfd.connect(ADDR)
except:
    sys.exit()


def query(name):
    while True:
        word = input("单词：")
        if word == '##':
            break
        msg = "Q %s %s" % (name, word)
        sockfd.send(msg.encode())
        data = sockfd.recv(2048).decode()
        print(data)


def history(name):
    msg = "H %s" % name
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == 'OK':
        while True:
            data = sockfd.recv(1024).decode()
            if data == '##':
                break
            else:
                print(data)
    else:
        print("没有查询记录")


def secondary_interface(name):
    while True:
        print("+---------命令选项----------+")
        print("|*****    1.查单词     *****|")
        print("|*****    2.历史记录   *****|")
        print("|*****    3.注销       *****|")
        print("+===========================+")
        cmd = input("命令:")
        if cmd == '1':
            query(name)
        elif cmd == '2':
            history(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确命令！")


def register():
    while True:
        name = input("请输入用户名：")
        passwd = getpass("请输入密码：")
        passwd_ = getpass("再次输入密码：")
        if passwd != passwd_:
            print("两次密码不一致！")
            continue
        if (' ' in name) or (' ' in passwd):
            print("用户名和密码不支持空格")
            continue
        msg = "R %s %s" % (name, passwd)
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()
        if data == 'OK':
            print("注册成功")
        else:
            print("注册失败")
        return


def login():
    while True:
        name = input("请输入用户名：")
        passwd = getpass("请输入密码：")
        msg = "L %s %s" % (name, passwd)
        sockfd.send(msg.encode())
        data = sockfd.recv(128).decode()
        if data == 'OK':
            print("登录成功")
            secondary_interface(name)
        else:
            print("登录失败")
        return


def main():
    # 循环发送消息
    while True:
        print("+---------命令选项----------+")
        print("|*****     1.注册      *****|")
        print("|*****     2.登录      *****|")
        print("|*****     3.退出      *****|")
        print("+===========================+")
        cmd = input("命令:")
        if cmd == '1':
            register()
        elif cmd == '2':
            login()
        elif cmd == '3':
            sockfd.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确命令！")


if __name__ == '__main__':
    main()
