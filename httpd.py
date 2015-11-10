# -*- coding: utf-8 -*-
import os, sys, time
from socket import *
myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)


def now():
    return time.ctime(time.time())


activeChildren = []


def reapChildren():
    while activeChildren:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid:break
        activeChildren.remove(pid)


def handleClient(connection):
    time.sleep(1)
    while True:

        data = connection.recv(40960)
        print(data.decode())
        if not data: break
        reply = 'Echo => %s at %s' %(data, now())
        connection.send(reply.encode())
        connection.close()
        os._exit(0)


def dispatcher():
    while True:
        connection, addres = sockobj.accept()
        print('Server connected by', addres, end=' ')
        print('at', now())
        #connection.send(b'yes!')
        reapChildren()
        childPid = os.fork()
        if childPid == 0:
            handleClient(connection)
        else:
            activeChildren.append(childPid)


dispatcher()