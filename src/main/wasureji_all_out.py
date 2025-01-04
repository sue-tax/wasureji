'''
右クリックで一括出力ダイアログを起動するクライアント
Created on 2024/12/14
@author: sue-t
'''

# from main import PORT
from main.sequence import Sequence

import datetime
from dateutil.relativedelta import relativedelta
import os
import sys
import json
import win32com.client
import TkEasyGUI as eg


class wasureji_all_out(object):
    layout_all_out = [
        [eg.Label("引渡し")],
        [eg.Label("いつ　"), eg.Combo("", key="-output_date-")],
        [eg.Label("誰へ　"), eg.Combo("", key="-output_delivery-")],
        [eg.Label("何で　"), eg.Combo("", key="-output_by-")],

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
        list_out_delivery = self.seq.send_ask_out_delivery()
        list_out_by = self.seq.send_ask_out_by()
        d_today = datetime.date.today()
        d_yesterday = d_today + relativedelta(days=-1)
        list_date = [d_today.strftime('%Y%m%d'), d_yesterday.strftime('%Y%m%d')]

        self.window = eg.Window("一括引渡し設定", self.layout_all_out)
        self.window["-output_date-"].set_values(list_date)
        self.window["-output_date-"].set_value("")
        self.window["-output_delivery-"].set_values(list_out_delivery)
        self.window["-output_delivery-"].set_value("")
        self.window["-output_by-"].set_values(list_out_by)
        self.window["-output_by-"].set_value("")
        self.window["-cancel-"].set_disabled(False)
        self.window["-ok-"].set_disabled(False)
      
        while True:
            event, _values = self.window.read()
            if event == "-ok-":
                str_date = self.window["-output_date-"].get()
                str_delivery = self.window["-output_delivery-"].get()
                str_by = self.window["-output_by-"].get()
                for str_file_name in list_file_name:
                    rcv = self.seq.send_ask_file(str_file_name)
                    if rcv == None:
                        self.seq.send_insert_file(
                                str_file_name,
                                "", "","")
                    # outは複数設定可能なので、常にinsert
                    self.seq.send_insert_out(str_file_name,
                            str_date, str_delivery, str_by)
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
    # file_name = str(sys.argv[1])
    list_file_name = []
    for index in range(1, len(sys.argv)):
        list_file_name.append(str(sys.argv[index]))
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
                "wasureji_all_in")
        sys.exit(-1)
    input_ = wasureji_all_out(
            json_dict["host"], json_dict["port"])
    input_.start(list_file_name)
    sys.exit(0)
