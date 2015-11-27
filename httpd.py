# -*- coding: utf-8 -*-
import os, sys, time
import getopt
from socket import *
from ClientHandler import Handler
myHost = '127.0.0.1'
myPort = 8080

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockobj.bind((myHost, myPort))
sockobj.listen(4096)

def is_it_correct_root(root):
    if not os.access(root, os.R_OK):
        return False
    elif root.endswith('/'):
        root = root[:-1]
        return root
    else:
        return root

def now():
    return time.ctime(time.time())


activeChildren = []


def reapChildren():
    while activeChildren:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid:break
        activeChildren.remove(pid)


def dispatcher(document_root):
    while True:
        try:
            connection, addres = sockobj.accept()
            print('Server connected by', addres, ' ')
            print('at', now())

            reapChildren()
            childPid = os.fork()

            if childPid == 0:
                client_handler = Handler(connection, document_root)
                client_handler.handle_client()
            else:
                activeChildren.append(childPid)
        except KeyboardInterrupt:
            return



cores = 1
document_root = os.getcwd()

try:
    options, remainder = getopt.getopt(sys.argv[1:], "r:c:")
except getopt.GetoptError:
    print('Incorrect options!')
else:
    for opt, arg in options:
        if opt == '-r':
            document_root = arg
        elif opt == '-c':
            cores = int(arg)

print('Root (Default it is your project directory): ' + document_root)
print('Host: localhost:' + str(myPort))
document_root = is_it_correct_root(document_root)
if document_root:
    dispatcher(document_root)
else:
    print("Incorrect root!")