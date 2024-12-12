'''
右クリックで入力ダイアログを起動するクライアント
Created on 2024/12/10

@author: sue-t
'''

from main import PORT
from main.sequence import Sequence

import datetime
from dateutil.relativedelta import relativedelta
import os
import sys


'''
作成予定の他のクライアント
一括IN入力
一括OUT入力
検索
SQL検索
'''

'''
outputを複数
before,latestの処理
顧問先などをクリップボードにコピー
'''


import TkEasyGUI as eg

# ウィンドウのレイアウトを定義
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
    
    # 将来的には複数
    [eg.Label("出力")],
    [eg.Label("いつ　"), eg.Combo("", key="-output_date-")],
    [eg.Label("誰へ　"), eg.Combo("", key="-output_delivery-")],
    [eg.Label("何で　"), eg.Combo("", key="-output_by-")],
    
    [eg.Button("Cancel"), eg.Button("OK")]
]

def wasureji_input(file_name):
    seq = Sequence(PORT)
    list_doc = seq.send_ask_document()
    list_cust = seq.send_ask_customer()
    list_sect = seq.send_ask_section()
    list_in_origin = seq.send_ask_in_origin()
    list_in_by = seq.send_ask_in_by()
    list_out_delivery = seq.send_ask_out_delivery()
    list_out_by = seq.send_ask_out_by()
    
    d_today = datetime.date.today()
    d_yesterday = d_today + relativedelta(days=-1)
    list_date = [d_today.strftime('%Y%m%d'), d_yesterday.strftime('%Y%m%d')]

    list_base = seq.send_ask_file(file_name)
    # print(list_base)
    flag_exist_base = True 
    if list_base == None:
        flag_exist_base = False 
        list_base = ["", "", "", "", ""]
    set_doc = list_base[0]
    set_cust = list_base[1]
    set_sect = list_base[2]
    list_in = seq.send_ask_in(file_name)
    # print(list_in)
    flag_exist_in = True
    if list_in == None:
        flag_exist_in = False
        list_in = ["", "", ""]
    set_in_date = list_in[0]
    set_in_origin = list_in[1]
    set_in_by = list_in[2]
    list_out = seq.send_ask_out(file_name)
    # print(list_out)
    flag_exist_out = True
    if list_out == None:
        flag_exist_out = False
        list_out = ["", "", ""]
    set_out_date = list_out[0]
    set_out_delivery = list_out[1]
    set_out_by = list_out[2]

    # ウィンドウを作成し、with文を使用してコンテキスト管理
    # "Hello App"はウィンドウのタイトル、layoutは上で定義したレイアウト
    with eg.Window("wasureji", layout_input) as window:
        # window["-file-"].set_text(file_name)
        # window["-file-"].set_cursor_pos(len(file_name)-1)
        # window["-file-"].set_readonly(True)
        base_name = os.path.basename(file_name)
        window["-file-"].update(text=base_name,
                readonly=True) #, text_align="right")
        window["-file-"].set_cursor_pos(len(file_name)-1)
        window["-document-"].set_values(list_doc)
        window["-document-"].set_value(set_doc)
        window["-customer-"].set_values(list_cust)
        window["-customer-"].set_value(set_cust)
        window["-section-"].set_values(list_sect)
        window["-section-"].set_value(set_sect)

        window["-input_date-"].set_values(list_date)
        window["-input_date-"].set_value(set_in_date)
        window["-input_origin-"].set_values(list_in_origin)
        window["-input_origin-"].set_value(set_in_origin)
        window["-input_by-"].set_values(list_in_by)
        window["-input_by-"].set_value(set_in_by)

        window["-output_date-"].set_values(list_date)
        window["-output_date-"].set_value(set_out_date)
        window["-output_delivery-"].set_values(list_out_delivery)
        window["-output_delivery-"].set_value(set_out_delivery)
        window["-output_by-"].set_values(list_out_by)
        window["-output_by-"].set_value(set_out_by)
       
        for event, values in window.event_iter():
            if event == "OK":
                if flag_exist_base:
                    seq.send_replace_file(
                            file_name,
                            window["-document-"].get(),
                            window["-customer-"].get(),
                            window["-section-"].get(), "", "")
                else:
                    seq.send_insert_file(
                            file_name,
                            window["-document-"].get(),
                            window["-customer-"].get(),
                            window["-section-"].get(), "", "")
                if flag_exist_in:
                    seq.send_replace_in(
                            file_name,
                            window["-input_date-"].get(),
                            window["-input_origin-"].get(),
                            window["-input_by-"].get())
                else:
                    seq.send_insert_in(
                            file_name,
                            window["-input_date-"].get(),
                            window["-input_origin-"].get(),
                            window["-input_by-"].get())
                if flag_exist_out:
                    seq.send_replace_out(
                            file_name,
                            window["-output_date-"].get(),
                            window["-output_delivery-"].get(),
                            window["-output_by-"].get())
                else:
                    seq.send_insert_out(
                            file_name,
                            window["-output_date-"].get(),
                            window["-output_delivery-"].get(),
                            window["-output_by-"].get())
                break
            if event == "Cancel":
                answer = eg.confirm(
                        "登録せずに終了して良いですか？",
                        "キャンセル")
                if answer:
                    break
                continue

if __name__ == '__main__':
    file_name = str(sys.argv[1])
    # file_name = str("c:/dfafafa/adfaafafa/afafafa/abc.pdf")
    wasureji_input(file_name)
    # print("")
    sys.exit(0)
    
    # seq = Sequence(PORT)
    # list_base = seq.send_ask_file(file_name)
    # print(list_base)
    # if list_base == None:
    #     # ダミー
    #     rv = seq.send_insert_file(file_name,
    #             "確定申告書", "豊臣秀吉", "令和６年",
    #             "", "")
    #     print(rv)
    #     list_base = seq.send_ask_file(file_name)
    #     print(list_base)
    # else:
    #     # ダミー
    #     rv = seq.send_replace_file(file_name,
    #             "確定申告書", "豊臣秀吉", "令和５年",
    #             "", "")
    #     print(rv)
    #     list_base = seq.send_ask_file(file_name)
    #     print(list_base)
    # list_doc = seq.send_ask_document()
    # print(list_doc)
