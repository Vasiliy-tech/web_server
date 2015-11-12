# -*- coding: utf-8 -*-
import time, os
from datetime import datetime
EOL = '\r\n'
EOL1 = '\n'
EOL2 = '\n\r\n'
STATUS_OK = '200 OK'
STATUS_FORBIDDEN = '403 Forbidden'
STATUS_NOT_FOUND = '404 Not Found'
STATUS_METHOD_NOT_ALLOWED = '405 Method Not Allowed'


class Handler:
    def __init__(self, connection, document_root=''):
        self.connection = connection
        self.server = 'Server: smokey'
        self.document_root = ''
        self.request_data = ''
        self.method = ''
        self.date = datetime.now().strftime('Date: %a, %d %b %Y %H:%M:%S GMT +3')
        self.content_lenght = 'Content-Length: '
        self.content_type = 'Content-Type: '
        self.status = '200 OK'
        self.content = ''
        self.connection_type = 'Connection: close'

    def now(self):
        return time.ctime(time.time())


    def handle_client(self):
        time.sleep(1)
        data = ''
        while True:
            while EOL1 not in data and EOL2 not in data:
                data_buffer = self.connection.recv(1024)
                if not data_buffer:
                    break
                data += data_buffer.decode()

            self.request_data = data
            print(data)

            response_data = self.create_response(self.request_data)
            print('\n', response_data)

            if response_data:
                #reply = 'Echo => %s at %s' %(response_data, self.now())
                self.connection.send(response_data.encode())
                self.connection.close()
            else:
                self.connection.close()

            os._exit(0)

    def create_response_string(self):
        response = 'HTTP/1.1' + ' ' + self.status + EOL
        response += self.server + EOL
        response += self.content_type + self.get_content_type() +EOL
        response += self.date + EOL
        response += self.content_lenght + EOL
        response += self.connection_type + EOL + EOL
        if self.method == 'GET':
            response += self.content
            response += EOL
        return response

    def get_content_type(self):
        return 'text/html'

    def create_response(self, request_data):
        response_data = ''
        request_data = request_data.splitlines()
        first_line = request_data[0].split()
        self.method = first_line[0]
        #TODO: проверка что это get or HEAD


        self.document_root += first_line[1]
        if self.document_root.endswith('/'):
            self.document_root = 'index.html'
        #print('\n%s\n', self.document_root)


        try:
            request_file = open(self.document_root, 'r')
            response_data = request_file.read()
            self.content = response_data
            self.content_lenght += str(len(response_data))

        except:
            self.status = STATUS_NOT_FOUND

        response_data = self.create_response_string()

        return response_data

