'''
Created on 2024/12/09

@author: sue-t
'''

from main import KILL

import socket
from struct import pack, unpack
from com import HEADER_SIZE


class client(object):
    
    def __init__(self):
        self.server_ip = socket.gethostbyname(socket.gethostname())

    # @classmethod
    def send(self, port, str_msg):
        with socket.socket(socket.AF_INET,
                socket.SOCK_STREAM) as sock:
            sock.connect((self.server_ip, port))

            data_msg = bytes(str_msg, 'utf-8')
            sock.sendall(pack('!I', len(data_msg)))
            sock.sendall(data_msg)
            if str_msg == KILL:
                return None
            received_header = sock.recv(HEADER_SIZE)
            data_size = unpack('!I', received_header)[0]
            # print(data_size)
            received = sock.recv(data_size)
        # print("Sent:     {}".format(str_msg))
        # print("Received: {}".format(received.decode()))
        return received.decode(encoding='utf-8')
       



if __name__ == '__main__':
    pass