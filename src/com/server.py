'''
Created on 2024/12/09

@author: sue-t
'''

from com import HEADER_SIZE

import socket
import socketserver
from struct import pack,unpack

class WasurejiHandler(socketserver.BaseRequestHandler):
    server = None
    sequence = None

    def handle(self) -> None:
        _header = self.request.recv(HEADER_SIZE)
        data_size = unpack('!I', _header)[0]
        print(data_size)
        data_rcv = self.request.recv(data_size)
        # print(data_rcv)
        str_rcv = data_rcv.decode(encoding='utf-8')
        # print(str_rcv)
        str_msg = WasurejiHandler.server.recv(str_rcv)
        data_msg = bytes(str_msg, 'utf-8')
        self.request.sendall(pack('!I', len(data_msg)))
        self.request.sendall(data_msg)

    @classmethod
    def start_server(self, port, wasureji_server):
        WasurejiHandler.server = wasureji_server
        server_ip = socket.gethostbyname(socket.gethostname())
        with socketserver.TCPServer((server_ip, port),
                WasurejiHandler) as s:
            s.serve_forever()


if __name__ == '__main__':
    from main import PORT
    WasurejiHandler.start_server(PORT)