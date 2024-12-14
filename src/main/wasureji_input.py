'''
右クリックで入力ダイアログを起動するクライアント
Created on 2024/12/10

@author: sue-t
'''

from main import PORT
from main.sequence import Sequence

import pyperclip
import datetime
from dateutil.relativedelta import relativedelta
import os
import sys


'''
作成予定の他のクライアント
ユーティリティ
　KILL
　検索
　検索後、削除・置換
　SQL 検索、その他
'''

'''
TODO before,latestの処理
'''


import TkEasyGUI as eg

class wasureji_input(object):
    layout_input = [
        [eg.Label("ファイル名"), eg.Input("", key='-file-'  ),],
                    # text_align="right" )],
        [eg.Label("書類名"), eg.Combo([], key='-document-')],
        [eg.Label("顧客名"), eg.Combo([], key='-customer-')],
        [eg.Label("区分名"), eg.Combo([], key='-section-')],
    
        [eg.Label("入力")],
        [eg.Label("いつ　"), eg.Combo("", key="-input_date-")],
        [eg.Label("誰から"), eg.Combo("", key="-input_origin-")],
        [eg.Label("何で　"), eg.Combo("", key="-input_by-")],
        
        [eg.Label("出力"), 
                eg.Button("追加", key="-output_append-"),
                eg.Button("変更", key="-output_change-"),
                eg.Button("中止", key="-output_abort-"),
                eg.Button("確定", key="-output_confirm-")],
        [eg.Label("いつ　"), eg.Combo("", key="-output_date-")],
        [eg.Label("誰へ　"), eg.Combo("", key="-output_delivery-")],
        [eg.Label("何で　"), eg.Combo("", key="-output_by-")],
        [eg.Button("≪", key="-output_left-"),
                # eg.Input("", width=2, key="-output_index-"),
                eg.Label("", width=2, key="-output_index-"),
                eg.Label("／"),
                eg.Label("", width=2, key="-output_all-"),
                eg.Button("≫", key="-output_right-")],
        
        [eg.Button("Cancel", key="-cancel-"),
                eg.Button("OK", key="-ok-")]
    ]

    def event_tsuika(self):
        self.out_index = self.out_all + 1
        self.window["-output_date-"].set_value("")
        self.window["-output_delivery-"].set_value("")
        self.window["-output_by-"].set_value("")
        self.window["-output_date-"].set_readonly(False)
        self.window["-output_date-"].set_disabled(False)
        self.window["-output_delivery-"].set_readonly(False)
        self.window["-output_delivery-"].set_disabled(False)
        self.window["-output_by-"].set_readonly(False)
        self.window["-output_by-"].set_disabled(False)
        self.window["-output_index-"].set_text(str(self.out_index))

        self.window["-output_append-"].set_disabled(True)
        self.window["-output_change-"].set_disabled(True)
        self.window["-output_abort-"].set_disabled(False)
        self.window["-output_confirm-"].set_disabled(False)
        self.window["-output_left-"].set_disabled(True)
        self.window["-output_right-"].set_disabled(True)
        self.window["-cancel-"].set_disabled(True)
        self.window["-ok-"].set_disabled(True)
        return True

    def event_henkou(self):
        self.window["-output_date-"].set_readonly(False)
        self.window["-output_date-"].set_disabled(False)
        self.window["-output_delivery-"].set_readonly(False)
        self.window["-output_delivery-"].set_disabled(False)
        self.window["-output_by-"].set_readonly(False)
        self.window["-output_by-"].set_disabled(False)
        self.window["-output_index-"].set_text(str(self.out_index))

        self.window["-output_append-"].set_disabled(True)
        self.window["-output_change-"].set_disabled(True)
        self.window["-output_abort-"].set_disabled(False)
        self.window["-output_confirm-"].set_disabled(False)
        self.window["-output_left-"].set_disabled(True)
        self.window["-output_right-"].set_disabled(True)
        self.window["-cancel-"].set_disabled(True)
        self.window["-ok-"].set_disabled(True)
        return True

    def event_chushi(self):
        if self.out_index == self.out_all + 1:
            self.out_index = self.out_all
            self.window["-output_index-"]. \
                    set_text(str(self.out_index))
            if self.out_index == 0:
                self.window["-output_date-"].set_value("")
                self.window["-output_delivery-"].set_value("")
                self.window["-output_by-"].set_value("")
            else:
                out_ = self.list_out[self.out_index-1]
                self.window["-output_date-"].set_value(out_[0])
                self.window["-output_delivery-"].set_value(out_[1])
                self.window["-output_by-"].set_value(out_[2])
        else:
            out_ = self.list_out[self.out_index-1]
            self.window["-output_date-"].set_value(out_[0])
            self.window["-output_delivery-"].set_value(out_[1])
            self.window["-output_by-"].set_value(out_[2])
        self.window["-output_append-"].set_disabled(False)
        self.window["-output_change-"].set_disabled(False)
        self.window["-output_abort-"].set_disabled(True)
        self.window["-output_confirm-"].set_disabled(True)
        self.window["-output_date-"].set_readonly(True)
        self.window["-output_date-"].set_disabled(True)
        self.window["-output_delivery-"].set_readonly(True)
        self.window["-output_delivery-"].set_disabled(True)
        self.window["-output_by-"].set_readonly(True)
        self.window["-output_by-"].set_disabled(True)
        if self.out_index > 1:
            self.window["-output_left-"].set_disabled(False)
        if self.out_index == self.out_all:
            self.window["-output_right-"].set_disabled(False)
        self.window["-cancel-"].set_disabled(False)
        self.window["-ok-"].set_disabled(False)
        return True

    def event_kakutei(self):
        str_date = self.window["-output_date-"].get()
        str_delivery = self.window["-output_delivery-"].get()
        str_by = self.window["-output_by-"].get()
        if self.out_index == self.out_all + 1:
            # 追加
            if self.out_index == 1:
                self.list_out = [[str_date, str_delivery, str_by]]
            else:
                self.list_out.append(
                        [str_date, str_delivery, str_by])
            self.out_all += 1
            # TODO DBをここでしない
            self.seq.send_insert_out(
                   file_name,
                   str_date, str_delivery, str_by)
            self.window["-output_all-"]. \
                    set_text(str(self.out_all))
        else:
            # 変更
            self.list_out[self.out_index-1] = \
                        [str_date, str_delivery, str_by]
            # TODO DBをここでしない
            self.seq.send_delete_out(file_name)
            for out_ in self.list_out:
                self.seq.send_insert_out(
                       file_name,
                       out_[0], out_[1], out_[2])
        self.window["-output_append-"].set_disabled(False)
        self.window["-output_change-"].set_disabled(False)
        self.window["-output_abort-"].set_disabled(True)
        self.window["-output_confirm-"].set_disabled(True)
        self.window["-output_date-"].set_readonly(True)
        self.window["-output_date-"].set_disabled(True)
        self.window["-output_delivery-"].set_readonly(True)
        self.window["-output_delivery-"].set_disabled(True)
        self.window["-output_by-"].set_readonly(True)
        self.window["-output_by-"].set_disabled(True)
        if self.out_index > 1:
            self.window["-output_left-"].set_disabled(False)
        if self.out_index == self.out_all:
            self.window["-output_right-"].set_disabled(False)
        self.window["-cancel-"].set_disabled(False)
        self.window["-ok-"].set_disabled(False)
        return True

    def event_left(self):
        self.out_index -= 1
        self.window["-output_date-"].set_value(
                self.list_out[self.out_index-1][0])
        self.window["-output_delivery-"].set_value(
                self.list_out[self.out_index-1][1])
        self.window["-output_by-"].set_value(
                self.list_out[self.out_index-1][2])
        self.window["-output_index-"]. \
                set_text(str(self.out_index))
        if self.out_index == 1:
            self.window["-output_left-"].set_disabled(True)
        self.window["-output_right-"].set_disabled(False)
        return True

    def event_right(self):
        self.out_index += 1
        self.window["-output_date-"].set_value(
                self.list_out[self.out_index-1][0])
        self.window["-output_delivery-"].set_value(
                self.list_out[self.out_index-1][1])
        self.window["-output_by-"].set_value(
                self.list_out[self.out_index-1][2])
        self.window["-output_index-"]. \
                set_text(str(self.out_index))
        self.window["-output_left-"].set_disabled(False)
        if self.out_index == self.out_all:
            self.window["-output_right-"].set_disabled(True)
        return True

    def start(self, file_name):
        self.seq = Sequence(PORT)
        list_doc = self.seq.send_ask_document()
        list_cust = self.seq.send_ask_customer()
        list_sect = self.seq.send_ask_section()
        list_in_origin = self.seq.send_ask_in_origin()
        list_in_by = self.seq.send_ask_in_by()
        list_out_delivery = self.seq.send_ask_out_delivery()
        list_out_by = self.seq.send_ask_out_by()
        
        d_today = datetime.date.today()
        d_yesterday = d_today + relativedelta(days=-1)
        list_date = [d_today.strftime('%Y%m%d'), d_yesterday.strftime('%Y%m%d')]
    
        list_base = self.seq.send_ask_file(file_name)
        # print(list_base)
        flag_exist_base = True 
        if list_base == None:
            flag_exist_base = False 
            list_base = ["", "", "", "", ""]
        set_doc = list_base[0]
        set_cust = list_base[1]
        set_sect = list_base[2]
        list_in = self.seq.send_ask_in(file_name)
        # print(list_in)
        flag_exist_in = True
        if list_in == None:
            flag_exist_in = False
            list_in = ["", "", ""]
        set_in_date = list_in[0]
        set_in_origin = list_in[1]
        set_in_by = list_in[2]
        
        self.list_out = self.seq.send_ask_out(file_name)
        print(self.list_out)
        # flag_exist_out = True
        if self.list_out == None:
            # flag_exist_out = False
            self.out_index = 0
            self.out_all = 0
            self.list_out = [["", "", ""]]
        else:
            self.out_index = 1
            self.out_all = len(self.list_out)
        # out_exist = out_all
        set_out_date = self.list_out[0][0]
        set_out_delivery = self.list_out[0][1]
        set_out_by = self.list_out[0][2]
    
        self.window = eg.Window("wasureji", self.layout_input)
        # with eg.Window("wasureji", self.layout_input) as window:
            # window["-file-"].set_text(file_name)
            # window["-file-"].set_cursor_pos(len(file_name)-1)
            # window["-file-"].set_readonly(True)
        base_name = os.path.basename(file_name)
        self.window["-file-"].update(text=base_name,
                readonly=True) #, text_align="right")
        self.window["-file-"].set_cursor_pos(len(file_name)-1)
        self.window["-document-"].set_values(list_doc)
        self.window["-document-"].set_value(set_doc)
        self.window["-customer-"].set_values(list_cust)
        self.window["-customer-"].set_value(set_cust)
        self.window["-section-"].set_values(list_sect)
        self.window["-section-"].set_value(set_sect)

        self.window["-input_date-"].set_values(list_date)
        self.window["-input_date-"].set_value(set_in_date)
        self.window["-input_origin-"].set_values(list_in_origin)
        self.window["-input_origin-"].set_value(set_in_origin)
        self.window["-input_by-"].set_values(list_in_by)
        self.window["-input_by-"].set_value(set_in_by)

        self.window["-output_index-"].set_text(str(self.out_index))
        self.window["-output_all-"].set_text(str(self.out_all))
        self.window["-output_date-"].set_values(list_date)
        self.window["-output_date-"].set_value(set_out_date)
        self.window["-output_delivery-"].set_values(list_out_delivery)
        self.window["-output_delivery-"].set_value(set_out_delivery)
        self.window["-output_by-"].set_values(list_out_by)
        self.window["-output_by-"].set_value(set_out_by)
        self.window["-output_date-"].set_readonly(True)
        self.window["-output_date-"].set_disabled(True)
        self.window["-output_delivery-"].set_readonly(True)
        self.window["-output_delivery-"].set_disabled(True)
        self.window["-output_by-"].set_readonly(True)
        self.window["-output_by-"].set_disabled(True)

        self.window["-output_date-"].set_readonly(False)
        self.window["-output_date-"].set_disabled(False)
        self.window["-output_delivery-"].set_readonly(False)
        self.window["-output_delivery-"].set_disabled(False)
        self.window["-output_by-"].set_readonly(False)
        self.window["-output_by-"].set_disabled(False)
        self.window["-output_index-"].set_text(str(self.out_index))

        self.window["-output_append-"].set_disabled(False)
        self.window["-output_change-"].set_disabled(False)
        self.window["-output_abort-"].set_disabled(True)
        self.window["-output_confirm-"].set_disabled(True)
        if self.out_index <= 1:
            self.window["-output_left-"].set_disabled(True)
        else:
            self.window["-output_left-"].set_disabled(False)
        if self.out_index == 1 and self.out_all == 1:
            self.window["-output_right-"].set_disabled(True)
        else:
            self.window["-output_right-"].set_disabled(False)
        self.window["-cancel-"].set_disabled(False)
        self.window["-ok-"].set_disabled(False)
      
        while True:
            event, _values = self.window.read()
        # for event, _values in self.window.event_iter():
            if event == "-output_append-":
                self.event_tsuika()
                continue
            if event == "-output_change-":
                self.event_henkou()
                continue
            if event == "-output_abort-":
                self.event_chushi()
                continue
            if event == "-output_confirm-":
                self.event_kakutei()
                continue
            if event == "-output_left-":
                self.event_left()
                continue
            if event == "-output_right-":
                self.event_right()
                continue
            
            if event == "-ok-":
                if flag_exist_base:
                    self.seq.send_replace_file(
                            file_name,
                            self.window["-document-"].get(),
                            self.window["-customer-"].get(),
                            self.window["-section-"].get(), "", "")
                else:
                    self.seq.send_insert_file(
                            file_name,
                            self.window["-document-"].get(),
                            self.window["-customer-"].get(),
                            self.window["-section-"].get(), "", "")
                
                pyperclip.copy(self.window["-section-"].get())
                pyperclip.copy(self.window["-customer-"].get())
                pyperclip.copy(self.window["-document-"].get())
                
                if flag_exist_in:
                    self.seq.send_replace_in(
                            file_name,
                            self.window["-input_date-"].get(),
                            self.window["-input_origin-"].get(),
                            self.window["-input_by-"].get())
                else:
                    self.seq.send_insert_in(
                            file_name,
                            self.window["-input_date-"].get(),
                            self.window["-input_origin-"].get(),
                            self.window["-input_by-"].get())
                # TODO outも、ここでDB処理
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
    file_name = str(sys.argv[1])
    # file_name = str("c:/dfafafa/adfaafafa/afafafa/abcd.pdf")
    input_ = wasureji_input()
    input_.start(file_name)
    sys.exit(0)
