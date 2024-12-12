'''
忘れじサーバー
Created on 2024/12/10

@author: sue-t
'''

# from main import *
from main import PORT
from main import DATABASE
from main import KILL
from main.sequence import Sequence

from database.wasureji_db import WasurejiDB
from com.server import WasurejiHandler

import signal
import sys

server = None

# TODO ファイル監視

def sig_handler(signum, frame) -> None:
    server.term
    sys.exit(1)

class wasureji_server(object):
    '''
    classdocs
    '''


    def __init__(self, database_name, port):
        self.database_name = database_name
        self.port = port

    def start(self):
        # print(self.database_name)
        # self.database = database.WasurejiDB(self.database_name)
        self.database = WasurejiDB(self.database_name)
        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)
        self.database.create_table()
        WasurejiHandler.sequence = Sequence(self.port)
        WasurejiHandler.start_server(self.port, self)
    
    def term(self):
        self.database.term()
        
    def recv(self, str_msg):
        if str_msg.startswith(KILL):
            self.term()
            exit(0)
        ret_msg = WasurejiHandler.sequence.listen(
                str_msg, self.database)
        return ret_msg
            
            

if __name__ == '__main__':
    server = wasureji_server(DATABASE, PORT)
    server.start()
    