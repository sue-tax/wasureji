'''
忘れじサーバー
Created on 2024/12/10

@author: sue-t
'''

from main import KILL,PING
from main.sequence import Sequence

from database.wasureji_db import WasurejiDB
from com.server import WasurejiHandler

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

import signal
# from signal import SIGKILL
import sys
import TkEasyGUI as eg
import json
import os
import win32com.client

server = None

def sig_handler(signum, frame) -> None:
    server.term
    sys.exit(1)

class wasureji_server(object):
    def __init__(self, directory_name, database_name, port):
        self.directory_name = directory_name
        self.database_name = database_name
        self.port = port
        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT, sig_handler)
        WasurejiHandler.sequence = Sequence(
                None, self.port)
        eg.popup_auto_close(
                "wasureji_server 起動しました",
                "Information",
                buttons=[])

    def start(self):
        database_name_ = os.path.join(self.directory_name,
                self.database_name)
        self.database = WasurejiDB(database_name_)
        # signal.signal(signal.SIGTERM, sig_handler)
        # signal.signal(signal.SIGINT, sig_handler)
        self.database.create_table()
        # WasurejiHandler.sequence = Sequence(
        #         None, self.port)
        # eg.popup_auto_close(
        #         "wasureji_server 起動しました",
        #         "Information",
        #         buttons=[])
        WasurejiHandler.start_server(
                self.port, self)
    
    def term(self):
        self.database.term()
        
    def recv(self, str_msg):
        if str_msg.startswith(KILL):
            self.term()
            # sys.exit(0)
            os.kill(os.getpid(), 9) #signal.SIGKILL)
        if str_msg.startswith(PING):
            ret_msg = "reply"
        else:
            ret_msg = WasurejiHandler.sequence.listen(
                    str_msg, self.database)
        return ret_msg

class MyWatcher:
 
    def __init__(self, host, port, directory=".",
            ):
            # handler=FileSystemEventHandler()):
        self.seq = Sequence(host, port)
        # self.handler = handler
        self.directory = directory
 
    def get_seq(self):
        return self.seq

    def set_handler(self,
            handler=FileSystemEventHandler()):
        self.handler = handler

    def run(self):
        self.observer = Observer()
        self.observer.schedule(self.handler,
                self.directory, recursive=True)
        self.observer.start()
        # print(f"MyWatcher Running in {self.directory}")
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        # print("\nMyWatcher Terminated\n")
 
 
class MyHandler(FileSystemEventHandler):
    def __init__(self, seq):
        self.seq = seq

    # ファイル削除、移動
    def on_deleted(self, event):
        filepath = event.src_path
        _flag_exist = self.seq.send_exist_del(filepath)

    # リネーム
    def on_moved(self, event):
        filepath = event.src_path
        _flag_exist = self.seq.send_exist_ren(filepath)


if __name__ == '__main__':
    try:
        objShell = win32com.client.Dispatch("WScript.Shell")
        dir_name = objShell.SpecialFolders("SENDTO")
        json_file_name = os.path.join(dir_name, 'wasureji.json')
        json_file = open(json_file_name, 'r')
        json_dict = json.load(json_file)    
    except Exception as e:
        eg.popup_error(
                "設定ファイル{}が読めません".format(
                        json_file_name),
                "wasureji_input")
        sys.exit(-1)
    server = wasureji_server(
            json_dict["directory"],
            json_dict["database"],
            json_dict["port"])
    w = MyWatcher(json_dict["host"], json_dict["port"],
            json_dict["watchdog_directory"])
    myHandler = MyHandler(w.get_seq())
    w.set_handler(myHandler)
    thread1 = threading.Thread(target=w.run)
    thread1.start()
    server.start()
    