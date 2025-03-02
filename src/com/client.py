'''
Created on 2024/12/09

@author: sue-t
'''

from main import KILL

import socket
from struct import pack, unpack
from com import HEADER_SIZE


class client(object):
    
    # def __init__(self):
    #     self.server_ip = socket.gethostbyname(socket.gethostname())

    def __init__(self, host, port):
        if host == None:
            host_name = socket.gethostname()
            self.server_ip = socket.gethostbyname(host_name)
        else:
            # host_name = host
            self.server_ip = host
        # self.server_ip = socket.gethostbyname(host_name)
        self.port = port

    # @classmethod
    # def send(self, port, str_msg):
    def send(self, str_msg):
        with socket.socket(socket.AF_INET,
                socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.server_ip, self.port))
                # print(str_msg)
                data_msg = bytes(str_msg, 'utf-8')
                sock.sendall(pack('!I', len(data_msg)))
                sock.sendall(data_msg)
                if str_msg == KILL:
                    return None
                received_header = sock.recv(HEADER_SIZE)
                data_size = unpack('!I', received_header)[0]
                # print(data_size)
                received = sock.recv(data_size)
            except Exception as e:
                return f"error_socket:{e}"
            finally:
                sock.close()
        str_rcv = received.decode(encoding='utf-8')
        # print(str_rcv)
        return str_rcv

if __name__ == '__main__':
    pass