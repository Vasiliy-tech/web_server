# -*- coding: utf-8 -*-
import os, sys, time
from socket import *
from ClientHandler import Handler
myHost = '127.0.0.1'
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockobj.bind((myHost, myPort))
sockobj.listen(4096)


def now():
    return time.ctime(time.time())


activeChildren = []


def reapChildren():
    while activeChildren:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid:break
        activeChildren.remove(pid)


def dispatcher():
    while True:
        connection, addres = sockobj.accept()
        print('Server connected by', addres, end=' ')
        print('at', now())
        #connection.send(b'yes!')
        reapChildren()
        childPid = os.fork()
        if childPid == 0:
            client_handler = Handler(connection)
            client_handler.handle_client()
        else:
            activeChildren.append(childPid)


dispatcher()