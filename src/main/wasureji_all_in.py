'''
右クリックで一括入力ダイアログを起動するクライアント
Created on 2024/12/14
@author: sue-t
'''

from main.sequence import Sequence

import datetime
from dateutil.relativedelta import relativedelta
import os
import sys
import json
import win32com.client
import TkEasyGUI as eg


class wasureji_all_in(object):
    layout_all_in = [
        [eg.Label("受取り")],
        [eg.Label("いつ　"), eg.Combo("", key="-input_date-")],
        [eg.Label("誰から"), eg.Combo("", key="-input_origin-")],
        [eg.Label("何で　"), eg.Combo("", key="-input_by-")],

        [eg.Button("Cancel", key="-cancel-"),
                eg.Button("OK", key="-ok-")]
    ]

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self, list_file_name):
        # self.seq = Sequence(PORT)
        self.seq = Sequence(self.host, self.port)
        str_msg = self.seq.ping()
        if str_msg != None:
            eg.popup_error(str_msg,
                    "サーバーが起動していない")
            return -1
        list_in_origin = self.seq.send_ask_in_origin()
        list_in_by = self.seq.send_ask_in_by()
        
        d_today = datetime.date.today()
        d_yesterday = d_today + relativedelta(days=-1)
        list_date = [d_today.strftime('%Y%m%d'), d_yesterday.strftime('%Y%m%d')]
    
        self.window = eg.Window("一括受取り設定", self.layout_all_in)
        self.window["-input_date-"].set_values(list_date)
        self.window["-input_date-"].set_value("")
        self.window["-input_origin-"].set_values(list_in_origin)
        self.window["-input_origin-"].set_value("")
        self.window["-input_by-"].set_values(list_in_by)
        self.window["-input_by-"].set_value("")
        self.window["-cancel-"].set_disabled(False)
        self.window["-ok-"].set_disabled(False)
      
        while True:
            event, _values = self.window.read()
            if event == "-ok-":
                str_date = self.window["-input_date-"].get()
                str_origin = self.window["-input_origin-"].get()
                str_by = self.window["-input_by-"].get()
                for str_file_name in list_file_name:
                    rcv = self.seq.send_ask_file(str_file_name)
                    if rcv == None:
                        self.seq.send_insert_file(
                                str_file_name,
                                "", "","")
                    rcv = self.seq.send_ask_in(str_file_name)
                    if rcv == None:
                        self.seq.send_insert_in(str_file_name,
                                str_date, str_origin, str_by)
                    else:
                        self.seq.send_replace_in(str_file_name,
                                str_date, str_origin, str_by)
                break
            if event == "-cancel-" or event == "WINDOW_CLOSED":
                answer = eg.confirm(
                        "登録せずに終了して良いですか？",
                        "")
                if answer:
                    break
                continue
        self.window.close()

if __name__ == '__main__':
    list_file_name = []
    for index in range(1, len(sys.argv)):
        list_file_name.append(str(sys.argv[index]))
    try:
        objShell = win32com.client.Dispatch("WScript.Shell")
        dir_name = objShell.SpecialFolders("SENDTO")
        file_name = os.path.join(dir_name, 'wasureji.json')
        json_file = open(file_name, 'r')
        json_dict = json.load(json_file)    
    except Exception as e:
        eg.popup_error(
                "設定ファイル{}が読めません".format(file_name),
                "wasureji_all_in")
        sys.exit(-1)
    input_ = wasureji_all_in(
            json_dict["host"], json_dict["port"])
    input_.start(list_file_name)
    sys.exit(0)
