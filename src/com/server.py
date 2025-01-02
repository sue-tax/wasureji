'''
Created on 2024/12/09

@author: sue-t
'''

from com import HEADER_SIZE

import socket
import socketserver
from struct import pack,unpack

import TkEasyGUI

class WasurejiHandler(socketserver.BaseRequestHandler):
    server = None
    sequence = None

    def handle(self) -> None:
        try:
            _header = self.request.recv(HEADER_SIZE)
            data_size = unpack('!I', _header)[0]
            # print(data_size)
            data_rcv = self.request.recv(data_size)
            # print(data_rcv)
            str_rcv = data_rcv.decode(encoding='utf-8')
            # print(str_rcv)
            str_msg = WasurejiHandler.server.recv(str_rcv)
            # print(str_msg)
            data_msg = bytes(str_msg, 'utf-8')
            # print(data_msg)
            # print(len(data_msg))
            self.request.sendall(pack('!I', len(data_msg)))
            self.request.sendall(data_msg)
        except Exception as e:
            TkEasyGUI.popup(f"error_com:{e}", "ERROR")
            
    @classmethod
    def start_server(self, port, wasureji_server):
        WasurejiHandler.server = wasureji_server
        # print(socket.gethostname())
        # HPENVY
        # if host == None:
        #     host_name = socket.gethostname()
        # else:
        #     host_name = host

        # server_ip = socket.gethostbyname(socket.gethostname())
        server_ip = "0.0.0.0"
        
        # server_ip = socket.gethostbyname(host_name)
        # print(server_ip)
        # 192.168.1.17
        try:
            with socketserver.TCPServer((server_ip, port),
                    WasurejiHandler) as s:
                s.serve_forever()
        except Exception as e:
            TkEasyGUI.popup(f"error_com:{e}", "ERROR")

if __name__ == '__main__':
    from main import PORT
    WasurejiHandler.start_server(PORT)