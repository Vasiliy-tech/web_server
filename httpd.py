# -*- coding: utf-8 -*-
import os, sys, time
import getopt
from socket import *
from ClientHandler import Handler
myHost = '127.0.0.1'
myPort = 8082

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


def is_it_correct_cores(cores):
    if cores >= 1 and cores <= 10:
        return cores
    else:
        return False


def now():
    return time.ctime(time.time())


activeChildren = []


def reapChildren():
    while activeChildren:
        pid, stat = os.waitpid(0, os.WNOHANG)
        if not pid:break
        activeChildren.remove(pid)


def dispatcher(document_root, cores):
    for i in range(cores):
        childPid = os.fork()

        if childPid == 0:
            while True:
                try:
                    connection, addres = sockobj.accept()
                    # print('Server connected by', addres, ' ')
                    # print('at', now())
                    client_handler = Handler(connection, document_root)
                    client_handler.handle_client()
                except KeyboardInterrupt:
                    os._exit(0)
                except:
                    pass

    try:
        os.waitpid(-1, 0)
    except KeyboardInterrupt:
        os._exit(0)


cores = 5
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
            try:
                cores = int(arg)
            except:
                cores = False

print('Root (Default it is your project directory): ' + document_root)
print('Host: localhost:' + str(myPort))
document_root = is_it_correct_root(document_root)
cores = is_it_correct_cores(cores)
if document_root and cores:
    dispatcher(document_root, cores)
else:
    print("Incorrect root or cores!")
