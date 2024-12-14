'''
Created on 2024/12/14
@author: sue-t
'''

from main import PORT
from main.sequence import Sequence

import sys


import TkEasyGUI as eg

class wasureji_utility(object):
    layout_utility = [
        [eg.Button("サーバー終了", key="-kill-")],
        
        [eg.Label("ＳＱＬ実行"),
            eg.Button("実行", key="-sql_exe-")],
        [eg.Multiline(
                "",
                key="-sql-",
                size=(120, 5))],
        # [eg.MultilineBrowse(
        [eg.Multiline(
                "",
                key="-result-",
                size=(120, 10))],

        [eg.Button("終了", key="-exit-")]
    ]

    def start(self):
        self.seq = Sequence(PORT)

        self.window = eg.Window("wasurejiユーティリティ",
                self.layout_utility)
        self.window["-result-"].set_readonly(True)
      
        while True:
            event, _values = self.window.read()
            if event == "-kill-":
                answer = eg.confirm(
                        "wasurejiサーバーの終了後、終了するので良いですか？"
                        "")
                if answer:
                    self.seq.send_kill()
                    break
                continue
            if event == "-sql_exe-":
                str_sql = self.window["-sql-"].get()
                if str_sql == "":
                    continue
                # print(str_sql)
                msg_sql = str_sql.rstrip('\n')
                # print(msg_sql)
                str_result = self.seq.send_execute_sql(msg_sql)
                # print(str_result)
                self.window["-result-"].set_text(str_result)
                continue
            if event == "-exit-" or event == "WINDOW_CLOSED":
                answer = eg.confirm(
                        "終了して良いですか？",
                        "")
                if answer:
                    break
                continue
        self.window.close()

if __name__ == '__main__':
    ut_ = wasureji_utility()
    ut_.start()
    sys.exit(0)
