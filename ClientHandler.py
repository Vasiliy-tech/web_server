# -*- coding: utf-8 -*-
import time, os
EOL1 = '\n'
EOL2 = '\n\r\n'

class Handler:
    def __init__(self, connection):
        self.connection = connection


    def now(self):
        return time.ctime(time.time())


    def handleClient(self):
        time.sleep(1)
        data = ''
        while True:
            while EOL1 not in data and EOL2 not in data:
                data_buffer = self.connection.recv(1)
                if not data_buffer:
                    break
                data += data_buffer.decode()
            #data = self.connection.recv()
            print(data)
            #if not data: break
            reply = 'Echo => %s at %s' %(data, self.now())
            self.connection.send(reply.encode())
            self.connection.close()
            os._exit(0)