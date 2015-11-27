# -*- coding: utf-8 -*-
import time, os, urllib
import socket
from datetime import datetime
EOL = '\r\n'
EOL1 = '\n\n'
EOL2 = '\n\r\n'
STATUS_OK = '200 OK'
STATUS_FORBIDDEN = '404 Forbidden'
STATUS_NOT_FOUND = '403 Not Found'
STATUS_METHOD_NOT_ALLOWED = '405 Method Not Allowed'


class Handler:
    def __init__(self, connection, document_root):
        self.connection = connection
        self.server = 'Server: smokey'
        self.document_root = document_root
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
        data = ''
        while True:
            while EOL1 not in data and EOL2 not in data:
                data_buffer = self.connection.recv(1024)
                if not data_buffer:
                    break
                data += data_buffer.decode('utf-8')

            self.request_data = data
            #print(data)

            response_data = self.create_response(self.request_data)
            #print(response_data)

            if response_data:
                self.connection.send(response_data)
                try:
                    self.connection.shutdown(socket.SHUT_RDWR)
                except socket.error:
                    self.connection.close()
                else:
                    self.connection.close()

            os._exit(0)


    def create_response_string(self):
        response = 'HTTP/1.1' + ' ' + self.status + EOL
        response += self.server + EOL
        response += self.get_content_type() + EOL
        response += self.date + EOL

        if self.status == STATUS_NOT_FOUND or self.status == STATUS_FORBIDDEN or self.status == STATUS_METHOD_NOT_ALLOWED:
            response += self.content_lenght + '0' + EOL
        else:
            response += self.content_lenght + EOL

        if self.method == 'GET':
            response += self.connection_type
            response += EOL + EOL
            response += self.content
            response += EOL
        elif self.method == 'HEAD' or self.status == STATUS_METHOD_NOT_ALLOWED:
           response += self.connection_type + EOL + EOL

        return response


    def get_content_type(self):
        if self.document_root.lower().endswith('/') or self.document_root.lower().endswith('.html') :
            self.content_type += 'text/html'

        elif self.document_root.lower().endswith('.css'):
            self.content_type += 'text/css'

        elif self.document_root.lower().endswith('.jpeg'):
            self.content_type += 'image/jpeg'

        elif self.document_root.lower().endswith('.jpg'):
            self.content_type += 'image/jpeg'

        elif self.document_root.lower().endswith('.js'):
            self.content_type += 'application/javascript'

        elif self.document_root.lower().endswith('.png'):
            self.content_type += 'image/png'

        elif self.document_root.lower().endswith('.gif'):
            self.content_type += 'image/gif'

        elif self.document_root.lower().endswith('.swf'):
            self.content_type += 'application/x-shockwave-flash'

        else:
            self.content_type += 'text/plane'

        return self.content_type


    def create_response(self, request_data):
        response_data = ''
        request_data = request_data.splitlines()
        first_line = request_data[0].split()
        self.method = first_line[0]

        self.document_root += first_line[1]
        self.document_root = urllib.unquote(self.document_root)

        if '?' in self.document_root:
            self.document_root = self.document_root.split('?')[0]


        if self.document_root.endswith('/'):
            self.document_root += 'index.html'


        if '..' in first_line[1]:
            self.status = STATUS_FORBIDDEN
        elif self.method != 'HEAD' and self.method != 'GET':
            self.status = STATUS_METHOD_NOT_ALLOWED
        else:
            try:
                request_file = open(self.document_root, 'r')
                response_data = request_file.read()
                self.content_lenght += str(len(response_data))
                if self.method == 'GET':
                    self.content = response_data
            except:
                if self.document_root.endswith('index.html'):
                    self.status = STATUS_NOT_FOUND
                else: self.status = STATUS_FORBIDDEN

        response_data = self.create_response_string()

        return response_data

