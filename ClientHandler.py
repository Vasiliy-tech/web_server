# -*- coding: utf-8 -*-
import time, os
from datetime import datetime
EOL = '\r\n'
EOL1 = '\n\n'
EOL2 = '\n\r\n'
STATUS_OK = '200 OK'
STATUS_FORBIDDEN = '403 Forbidden'
STATUS_NOT_FOUND = '404 Not Found'
STATUS_METHOD_NOT_ALLOWED = '405 Method Not Allowed'


class Handler:
    def __init__(self, connection, document_root=os.getcwd()):
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
                #print(data_buffer.decode())
                if not data_buffer:
                    break
                data += data_buffer.decode('utf-8')

            self.request_data = data
            print(data)

            response_data = self.create_response(self.request_data)
            print(response_data)

            if response_data:
                #bytes_sent_total = 0
                #while bytes_sent_total < len(response_data):
                #    data_to_send = response_data[bytes_sent_total:]
                #    bytes_sent_total += self.connection.send(data_to_send)
                self.connection.send(response_data)
                self.connection.close()
                if self.method == 'HEAD':
                    pass


            else:
                self.connection.send(response_data)
                self.connection.close()

            os._exit(0)

    def create_response_string(self):
        response = 'HTTP/1.1' + ' ' + self.status + EOL
        response += self.server + EOL
        response += self.get_content_type() +EOL
        response += self.date + EOL

        if self.status == STATUS_NOT_FOUND or self.status == STATUS_FORBIDDEN:
            response += self.content_lenght + '0' + EOL
        else:
            response += self.content_lenght + EOL


        if self.method == 'GET':
            response += self.connection_type
            response += EOL + EOL
            response += self.content
            response += EOL
        elif self.method == 'HEAD':
           response += self.connection_type + "\n\n"

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

        if self.method != 'HEAD' and self.method != 'GET':
            self.status = STATUS_METHOD_NOT_ALLOWED


        self.document_root += first_line[1]

        if '?' in self.document_root:
            self.document_root = self.document_root.split('?')[0]


        print (self.document_root)

        if self.document_root.endswith('/'):
            self.document_root += 'index.html'
        print(self.document_root)




        if '..' in first_line[1]:
            self.status = STATUS_FORBIDDEN
        else:
            try:
                request_file = open(self.document_root, 'r')
                response_data = request_file.read()
                self.content_lenght += str(len(response_data))
                if self.method == 'GET':
                    self.content = response_data
            except:
                self.status = STATUS_NOT_FOUND

        response_data = self.create_response_string()

        return response_data

