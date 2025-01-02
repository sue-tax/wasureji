'''
右クリックで表示ダイアログを起動するクライアント
Created on 2024/12/22

@author: sue-t
'''

from main.sequence import Sequence

import os
import sys
import json
import win32com.client
import TkEasyGUI as eg


'''
TODO　削除
'''

class wasureji_browse(object):
    layout_browse = [
        [eg.Label("ファイル名"),
                eg.Input("", width=50, key='-file-'  ),
                eg.Button("表示", key="-display_file-"),
                eg.Label("　　　　　　　　　　　　　　　　　"),
                # eg.Button("削除", key="-delete_file-")
                ],

        [eg.Label("書類名"), #eg.VSeparator(pad=2),# 縦区切り線 
                eg.Label("", key='-document-')],
        [eg.Label("顧客名"), eg.Label("", key='-customer-')],
        [eg.Label("区分名"), eg.Label("", key='-section-')],
    
        [eg.Label("受取り")],
        [eg.Label("いつ　"), eg.Label("", key="-input_date-")],
        [eg.Label("誰から"), eg.Label("", key="-input_origin-")],
        [eg.Label("何で　"), eg.Label("", key="-input_by-")],
        
        [eg.Label("引渡し")],
        [eg.Label("いつ　"), eg.Label("", key="-output_date-")],
        [eg.Label("誰へ　"), eg.Label("", key="-output_delivery-")],
        [eg.Label("何で　"), eg.Label("", key="-output_by-")],
        [eg.Button("≪", key="-output_left-"),
                eg.Label("", width=2, key="-output_index-"),
                eg.Label("／"),
                eg.Label("", width=2, key="-output_all-"),
                eg.Button("≫", key="-output_right-")],
        
        [eg.Label("最新"),
                eg.Input("", width=50, key="-latest-"),
                eg.Button("表示", key="-display_latest-"),
                eg.Label("　　　　"),
                # eg.Button("削除", key="-delete_latest-"),
                ],
        [eg.Label("履歴"),
                eg.Label("　　　　"),
                # eg.Button("Excel", key="-excel_history-"),
                eg.Label("　　　 　　　　　　　　　　　　　"),
                eg.Button("表示", key="-display_history-"),
                eg.Label("　　　　"),
                # eg.Button("削除", key="-delete_history-"),
                ],
        [eg.Listbox( 
            # values=get_program_files(), 
            size=(50, 5), 
            key="-files-", # 要素の参照キー
            # enable_events=True, # アクションがあれば実行する引数
        )],
 
        [eg.Label("　　　　　　　　　　　　　　　　　　　　"),
                eg.Button("OK", key="-ok-")]
    ]

    def event_left(self):
        self.out_index -= 1
        self.window["-output_date-"].set_text(
                self.list_out[self.out_index-1][0])
        self.window["-output_delivery-"].set_text(
                self.list_out[self.out_index-1][1])
        self.window["-output_by-"].set_text(
                self.list_out[self.out_index-1][2])
        self.window["-output_index-"]. \
                set_text(str(self.out_index))
        if self.out_index == 1:
            self.window["-output_left-"].set_disabled(True)
        self.window["-output_right-"].set_disabled(False)
        return True

    def event_right(self):
        self.out_index += 1
        self.window["-output_date-"].set_text(
                self.list_out[self.out_index-1][0])
        self.window["-output_delivery-"].set_text(
                self.list_out[self.out_index-1][1])
        self.window["-output_by-"].set_text(
                self.list_out[self.out_index-1][2])
        self.window["-output_index-"]. \
                set_text(str(self.out_index))
        self.window["-output_left-"].set_disabled(False)
        if self.out_index == self.out_all:
            self.window["-output_right-"].set_disabled(True)
        return True

    def event_display(self, file_name):
        os.startfile(file_name)
        return True

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self, file_name):
        # self.seq = Sequence(PORT)
        self.seq = Sequence(self.host, self.port)
        str_msg = self.seq.ping()
        if str_msg != None:
            eg.popup_error(str_msg,
                    "サーバーが起動していない")
            return -1
        list_base = self.seq.send_ask_file(file_name)
        # print(list_base)
        if list_base == None:
            list_base = ["", "", "", "", ""]
        self.set_doc = list_base[0]
        self.set_cust = list_base[1]
        self.set_sect = list_base[2]
        list_in = self.seq.send_ask_in(file_name)
        # print(list_in)
        if list_in == None:
            list_in = ["", "", ""]
        set_in_date = list_in[0]
        set_in_origin = list_in[1]
        set_in_by = list_in[2]
        
        self.list_out = self.seq.send_ask_out(file_name)
        # print(self.list_out)
        if self.list_out == None:
            self.out_index = 0
            self.out_all = 0
            self.list_out = [["", "", ""]]
        else:
            self.out_index = 1
            self.out_all = len(self.list_out)
        set_out_date = self.list_out[0][0]
        set_out_delivery = self.list_out[0][1]
        set_out_by = self.list_out[0][2]
    
        if (self.set_doc != "") and (self.set_cust != "") \
                and (self.set_sect != ""):
            list_history = self.seq.send_ask_history(
                    self.set_doc, self.set_cust, self.set_sect)
            # print(list_history)
            if list_history != None:
                for base_ in list_history:
                    if (base_[2] == None) or (base_[2] == ""):
                        self.latest = base_[0]
                        flag_exist_latest = True
                        break
                else:
                    self.latest = "最新ファイルが見つかりません"
                    flag_exist_latest = False
            else:
                self.latest = "最新ファイルが見つかりません"
                flag_exist_latest = False
        else:
                self.latest = "履歴管理対象外です"
                flag_exist_latest = False
        self.list_file = []
        if flag_exist_latest:
            while (not((base_[1] == None) or (base_[1] == ""))):
                self.list_file.append(base_[1])
                for before_ in list_history:
                    if before_[0] == base_[1]:
                        break
                else:
                    break
                base_ = before_

        self.window = eg.Window("wasureji_browse",
                self.layout_browse)
        base_name = os.path.basename(file_name)
        self.window["-file-"].update(text=base_name,
                readonly=True) #, text_align="right")
        self.window["-file-"].set_cursor_pos(len(file_name)-1)
        self.window["-document-"].set_text(self.set_doc)
        self.window["-customer-"].set_text(self.set_cust)
        self.window["-section-"].set_text(self.set_sect)

        self.window["-input_date-"].set_text(set_in_date)
        self.window["-input_origin-"].set_text(set_in_origin)
        self.window["-input_by-"].set_text(set_in_by)

        self.window["-output_index-"].set_text(str(self.out_index))
        self.window["-output_all-"].set_text(str(self.out_all))
        self.window["-output_date-"].set_text(set_out_date)
        self.window["-output_delivery-"].set_text(set_out_delivery)
        self.window["-output_by-"].set_text(set_out_by)

        self.window["-output_index-"].set_text(str(self.out_index))
        if self.out_index <= 1:
            self.window["-output_left-"].set_disabled(True)
        else:
            self.window["-output_left-"].set_disabled(False)
        if self.out_index == 1 and self.out_all == 1:
            self.window["-output_right-"].set_disabled(True)
        else:
            self.window["-output_right-"].set_disabled(False)

        # self.window["-latest-"].set_text(self.latest)
        self.window["-latest-"].update(text=self.latest,
                readonly=True)
        self.window["-files-"].set_values(self.list_file)
        
        self.window["-ok-"].set_disabled(False)

        # self.window["-delete_file-"].set_disabled(False)
        # self.window["-delete_latest-"].set_disabled(False)
        # self.window["-delete_history-"].set_disabled(False)
        # self.window["-excel_history-"].set_disabled(False)
                
        if not flag_exist_latest:
            self.window["-display_latest-"].set_disabled(True)
            # self.window["-delete_latest-"].set_disabled(True)
            # self.window["-excel_history-"].set_disabled(True)
            self.window["-display_history-"].set_disabled(True)
            # self.window["-delete_history-"].set_disabled(True)

        while True:
            event, _values = self.window.read()
            if event == "-output_left-":
                self.event_left()
                continue
            if event == "-output_right-":
                self.event_right()
                continue
    
            if event == "-display_file-":
                self.event_display(file_name)
                continue
            if event == "-display_latest-":
                self.event_display(self.latest)
                continue
            if event == "-display_history-":
                selected_list = self.window["-files-"]. \
                        get_selected_items()
                # print(selected_list)
                for selected_ in selected_list:
                    self.event_display(selected_)
                continue
            
            if event == "-ok-":
                break
            if event == "WINDOW_CLOSED":
                break

        self.window.close()

if __name__ == '__main__':
    file_name = str(sys.argv[1])
    # file_name = str("C:\\Users\\sue-t\\Desktop\\0_印刷先\\SVF Print_20241114_0833.pdf")
    try:
        objShell = win32com.client.Dispatch("WScript.Shell")
        dir_name = objShell.SpecialFolders("SENDTO")
        file_name = os.path.join(dir_name, 'wasureji.json')
        json_file = open(file_name, 'r')
        json_dict = json.load(json_file)    
    except Exception as e:
        eg.popup_error(
                "設定ファイル{}が読めません".format(file_name),
                "wasureji_browse")
        sys.exit(-1)
    input_ = wasureji_browse(
            json_dict["host"], json_dict["port"])
    input_.start(file_name)
    sys.exit(0)
