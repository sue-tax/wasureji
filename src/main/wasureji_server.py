'''
忘れじサーバー
Created on 2024/12/10

@author: sue-t
'''

from main import KILL
from main.sequence import Sequence

from database.wasureji_db import WasurejiDB
from com.server import WasurejiHandler

import signal
import sys
import TkEasyGUI as eg
import json
import os
import win32com.client

server = None


# TODO ファイル監視

def sig_handler(signum, frame) -> None:
    server.term
    sys.exit(1)

class wasureji_server(object):
    def __init__(self, directory_name, database_name, port):
        self.directory_name = directory_name
        self.database_name = database_name
        self.port = port

    def start(self):
        database_name_ = os.path.join(self.directory_name,
                self.database_name)
        self.database = WasurejiDB(database_name_)
        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)
        self.database.create_table()
        WasurejiHandler.sequence = Sequence(
                None, self.port)
        eg.popup_auto_close(
                "wasureji_server 起動しました",
                "Information")
        WasurejiHandler.start_server(
                self.port, self)
    
    def term(self):
        self.database.term()
        
    def recv(self, str_msg):
        if str_msg.startswith(KILL):
            self.term()
            sys.exit(0)
        ret_msg = WasurejiHandler.sequence.listen(
                str_msg, self.database)
        return ret_msg

if __name__ == '__main__':
    try:
        objShell = win32com.client.Dispatch("WScript.Shell")
        dir_name = objShell.SpecialFolders("SENDTO")
        file_name = os.path.join(dir_name, 'wasureji.json')
        json_file = open(file_name, 'r')
        json_dict = json.load(json_file)    
    except Exception as e:
        eg.popup_error(
                "設定ファイル{}が読めません".format(file_name),
                "wasureji_input")
        sys.exit(-1)
    server = wasureji_server(
            json_dict["directory"],
            json_dict["database"],
            json_dict["port"])
    server.start()
    