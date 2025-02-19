'''
Created on 2024/12/10

@author: sue-t
'''

from main import PING,KILL,SQL,COMMIT,ROLLBACK, \
        ASK_FILE,INS_FILE,REP_FILE, \
        EXIST_DEL, EXIST_REN, \
        ASK_DOC,ASK_CUST,ASK_SECT, \
        ASK_IN,INS_IN,REP_IN, \
        ASK_OUT,INS_OUT,REP_OUT,DEL_OUT, \
        ASK_IN_ORIGIN,ASK_IN_BY, \
        ASK_OUT_DELIV,ASK_OUT_BY, \
        ASK_HISTORY
from com.client import client

# import threading
import os

import TkEasyGUI as eg


class Sequence(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def ping(self):
        client_ = client(self.host, self.port)
        str_send = PING
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv.startswith("error"):
            return str_rcv
        return None

    def listen(self, str_msg, database):
        # if str_msg.startswith(PING):
        #     return "reply"

        if str_msg.startswith(SQL):
            str_result = database.execute_sql(
                    str_msg[len(SQL):])
            return str_result
         
        if str_msg.startswith(COMMIT):
            str_result = database.commit()
            return str_result

        if str_msg.startswith(ROLLBACK):
            str_result = database.rollback()
            return str_result
         
        if str_msg.startswith(ASK_FILE):
            list_base = database.select_file(
                    str_msg[len(ASK_FILE):])
            if len(list_base) == 0:
                return("[]")
            ret_msg = r'["{}","{}","{}","{}","{}"]'. \
                    format(list_base[0][1],
                           list_base[0][2], list_base[0][3],
                           list_base[0][4], list_base[0][5])
            return ret_msg
        if str_msg.startswith(INS_FILE):
            list_str = str_msg[len(INS_FILE):].split(',')
            str_msg = database.insert_file(list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1],
                    list_str[3][1:-1])
                    # list_str[4][1:-1],
                    # list_str[5][1:-1])
            return str_msg
        if str_msg.startswith(REP_FILE):
            list_str = str_msg[len(REP_FILE):].split(',')
            str_msg = database.replace_file(list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1],
                    list_str[3][1:-1],
                    list_str[4][1:-1],
                    list_str[5][1:-1],
                    list_str[6][1:-1])
            return str_msg
        
        if str_msg.startswith(EXIST_DEL):
            # 削除も名前変更も共用
            list_base = database.exist_file(
                    str_msg[len(EXIST_DEL):])
            # print("listen EXIST_DEL")
            # print(list_base)
            # print(threading.current_thread().getName())
            if len(list_base) == 0:
                return("[]")
            ret_msg = r'["{}"]'. \
                    format(list_base[0][0])
            warn_msg = "削除または移動した" \
                    "ファイル{}は、" \
                    "wasurejiデータベースに登録されています". \
                    format(list_base[0][0])
            # ここで表示は、美しくはないが
            eg.popup_warning(warn_msg, "wasureji")
            print('\007')
            return str_msg

        if str_msg.startswith(EXIST_REN):
            # 削除も名前変更も共用
            list_base = database.exist_file(
                    str_msg[len(EXIST_REN):])
            # print("listen EXIST_REN")
            # print(list_base)
            # print(threading.current_thread().getName())
            if len(list_base) == 0:
                return("[]")
            ret_msg = r'["{}"]'. \
                    format(list_base[0][0])
            warn_msg = "名前変更した" \
                    "ファイル{}は、" \
                    "wasurejiデータベースに登録されています". \
                    format(list_base[0][0])
            # ここで表示は、美しくはないが
            eg.popup_warning(warn_msg, "wasureji")
            print('\007')
            return str_msg

        if str_msg.startswith(ASK_DOC):
            list_doc = database.select_document()
            if len(list_doc) == 0:
                return("[]")
            list_ = []
            for atom in list_doc:
                list_.append(str(atom[0]))
            ret_msg = r'["' + r'","'.join(list_) + r'"]'
            # ret_msg = r'["' + r',"'.join(list_doc[0]) + r'"]'
            return ret_msg
        if str_msg.startswith(ASK_CUST):
            list_cust = database.select_customer()
            if len(list_cust) == 0:
                return("[]")
            list_ = []
            for atom in list_cust:
                list_.append(str(atom[0]))
            ret_msg = r'["' + r'","'.join(list_) + r'"]'
            return ret_msg
        if str_msg.startswith(ASK_SECT):
            list_sect = database.select_section()
            if len(list_sect) == 0:
                return("[]")
            list_ = []
            for atom in list_sect:
                list_.append(str(atom[0]))
            ret_msg = r'["' + r'","'.join(list_) + r'"]'
            return ret_msg

        if str_msg.startswith(ASK_IN):
            list_in = database.select_input(
                    str_msg[len(ASK_IN):])
            if len(list_in) == 0:
                return("[]")
            ret_msg = r'["{}","{}","{}"]'. \
                    format(list_in[0][1],
                           list_in[0][2], list_in[0][3])
            return ret_msg
        if str_msg.startswith(INS_IN):
            list_str = str_msg[len(INS_IN):].split(',')
            str_msg = database.insert_input(list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1],
                    list_str[3][1:-1])
            return str_msg
        if str_msg.startswith(REP_IN):
            list_str = str_msg[len(REP_IN):].split(',')
            str_msg = database.replace_input(list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1],
                    list_str[3][1:-1])
            return str_msg

        if str_msg.startswith(ASK_IN_ORIGIN):
            list_origin = database.select_in_origin()
            if len(list_origin) == 0:
                return("[]")
            list_ = []
            for atom in list_origin:
                list_.append(str(atom[0]))
            ret_msg = r'["' + r'","'.join(list_) + r'"]'
            return ret_msg
        if str_msg.startswith(ASK_IN_BY):
            list_by = database.select_in_by()
            if len(list_by) == 0:
                return("[]")
            list_ = []
            for atom in list_by:
                list_.append(str(atom[0]))
            ret_msg = r'["' + r'","'.join(list_) + r'"]'
            return ret_msg

        if str_msg.startswith(ASK_OUT):
            list_out = database.select_output(
                    str_msg[len(ASK_OUT):])
            if len(list_out) == 0:
                return("[]")
            ret_msg = r'['
            for list_ in list_out:
                ret_msg += r'["{}","{}","{}"];'. \
                        format(list_[1],
                               list_[2], list_[3])
            ret_msg = ret_msg[:-1] + ']'
            # [["..","..", ".."];[ ... ]; ... ]
            return ret_msg
        if str_msg.startswith(INS_OUT):
            list_str = str_msg[len(INS_OUT):].split(',')
            str_msg = database.insert_output(list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1],
                    list_str[3][1:-1])
            return str_msg
        if str_msg.startswith(REP_OUT):
            list_str = str_msg[len(REP_OUT):].split(',')
            str_msg = database.replace_output(list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1],
                    list_str[3][1:-1])
            return str_msg
        if str_msg.startswith(DEL_OUT):
            list_out = database.delete_output(
                    str_msg[len(DEL_OUT):])
            return str_msg

        if str_msg.startswith(ASK_OUT_DELIV):
            list_delivery = database.select_out_delivery()
            # print(list_delivery)
            if len(list_delivery) == 0:
                return("[]")
            list_ = []
            for atom in list_delivery:
                list_.append(str(atom[0]))
            ret_msg = r'["' + r'","'.join(list_) + r'"]'
            # print(ret_msg)
            return ret_msg
        if str_msg.startswith(ASK_OUT_BY):
            list_by = database.select_out_by()
            if len(list_by) == 0:
                return("[]")
            list_ = []
            for atom in list_by:
                list_.append(str(atom[0]))
            ret_msg = r'["' + r'","'.join(list_) + r'"]'
            return ret_msg

        if str_msg.startswith(ASK_HISTORY):
            list_str = str_msg[len(ASK_HISTORY):].split(',')
            list_history = database.select_history(
                    list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1])
            # print(list_history)
            if len(list_history) == 0:
                return("[]")
            ret_msg = r'['
            for list_ in list_history:
                ret_msg += r'["{}","{}","{}"];'. \
                        format(list_[0],
                        list_[1] if list_[1] != None else "",
                        list_[2] if list_[2] != None else "")
                # print(ret_msg)
            ret_msg = ret_msg[:-1] + ']'
            # print(ret_msg)
            return ret_msg
            
        return ("??")

    def send_kill(self):
        client_ = client(self.host, self.port)
        # _str_rcv = client_.send(self.port, KILL)
        _str_rcv = client_.send(KILL)
    
    def send_execute_sql(self, str_sql):
        client_ = client(self.host, self.port)
        str_send = "{}{}".format(SQL, str_sql)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv
        
    def send_commit(self):
        client_ = client(self.host, self.port)
        str_send = "{}".format(COMMIT)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv

    def send_rollback(self):
        client_ = client(self.host, self.port)
        str_send = "{}".format(ROLLBACK)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv
        
    def send_ask_file(self, str_file_name):
        client_ = client(self.host, self.port)
        str_send = "{}{}".format(ASK_FILE, str_file_name)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            return (list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1],
                    list_str[3][1:-1],
                    list_str[4][1:-1])

    def send_insert_file(self, str_file_name,
            str_document, str_customer, str_section):
            # str_before, str_latest):
        client_ = client(self.host, self.port)
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(INS_FILE, str_file_name,
                str_document, str_customer, str_section)
                # str_before, str_latest)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv

    def send_replace_file(self, str_file_name,
            str_document, str_customer, str_section,
            old_document, old_customer, old_section):
            # str_before, str_latest):
        client_ = client(self.host, self.port)
        str_send = r'{}"{}","{}","{}","{}","{}","{}","{}"'. \
                format(REP_FILE, str_file_name,
                str_document, str_customer, str_section,
                old_document, old_customer, old_section)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv


    def send_exist_del(self, str_file_name):
        client_ = client(self.host, self.port)
        str_send = "{}{}".format(EXIST_DEL, str_file_name)
        str_rcv = client_.send(str_send)
        # print(str_rcv)
        if str_rcv == "[]":
            return False
        else:
            return True

    def send_exist_ren(self, str_file_name):
        client_ = client(self.host, self.port)
        str_send = "{}{}".format(EXIST_REN, str_file_name)
        str_rcv = client_.send(str_send)
        # print(str_rcv)
        if str_rcv == "[]":
            return False
        else:
            return True

    def send_ask_document(self):
        client_ = client(self.host, self.port)
        str_send = ASK_DOC
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            return list_atom

    def send_ask_customer(self):
        client_ = client(self.host, self.port)
        str_send = ASK_CUST
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            return list_atom

    def send_ask_section(self):
        client_ = client(self.host, self.port)
        str_send = ASK_SECT
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        # print(str_rcv)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            # print(list_atom)
            return list_atom


    def send_ask_in(self, str_file_name):
        client_ = client(self.host, self.port)
        str_send = "{}{}".format(ASK_IN, str_file_name)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            return (list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1])

    def send_insert_in(self, str_file_name,
            str_date, str_origin, str_by):
        client_ = client(self.host, self.port)
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(INS_IN, str_file_name,
                str_date, str_origin, str_by)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv

    def send_replace_in(self, str_file_name,
            str_date, str_origin, str_by):
        client_ = client(self.host, self.port)
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(REP_IN, str_file_name,
                str_date, str_origin, str_by)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv


    def send_ask_in_origin(self):
        client_ = client(self.host, self.port)
        str_send = ASK_IN_ORIGIN
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            return list_atom

    def send_ask_in_by(self):
        client_ = client(self.host, self.port)
        str_send = ASK_IN_BY
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            return list_atom


    def send_ask_out(self, str_file_name):
        client_ = client(self.host, self.port)
        # print("*"+str_file_name+"*")
        str_send = "{}{}".format(ASK_OUT, str_file_name)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        # print(str_rcv)
        # os.system("pause")
        if str_rcv == "[]":
            return None
        else:
            list_line = str_rcv[1:-1].split(';')
            list_rcv = []
            for list_ in list_line:
                atom_ = list_[1:-1].split(',')
                list_rcv.append([ atom_[0][1:-1],
                        atom_[1][1:-1],
                        atom_[2][1:-1] ])
            # print(list_rcv)
            # os.system("pause")
            return list_rcv

    def send_insert_out(self, str_file_name,
            str_date, str_deliv, str_by):
        client_ = client(self.host, self.port)
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(INS_OUT, str_file_name,
                str_date, str_deliv, str_by)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv

    def send_delete_out(self, str_file_name):
        # str_file_nameの全てのoutを削除する
        client_ = client(self.host, self.port)
        str_send = "{}{}".format(DEL_OUT, str_file_name)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv

    def send_replace_out(self, str_file_name,
            str_date, str_deliv, str_by):
        # 複数指定では、使用しない？
        client_ = client(self.host, self.port)
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(REP_OUT, str_file_name,
                str_date, str_deliv, str_by)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        return str_rcv


    def send_ask_out_delivery(self):
        client_ = client(self.host, self.port)
        str_send = ASK_OUT_DELIV
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            # print(list_atom)
            return list_atom

    def send_ask_out_by(self):
        client_ = client(self.host, self.port)
        str_send = ASK_OUT_BY
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            return list_atom

    def send_ask_history(self,
            str_document, str_customer, str_section):
        client_ = client(self.host, self.port)
        str_send = r'{}"{}","{}","{}"'. \
                format(ASK_HISTORY,
                str_document, str_customer, str_section)
        # str_rcv = client_.send(self.port, str_send)
        str_rcv = client_.send(str_send)
        # print(str_rcv)
        if str_rcv == "[]" or str_rcv == "??":
            return None
        else:
            list_str = str_rcv[1:-1].split(';')
            # print(list_str)
            list_atom = []
            for atom_str in list_str:
                # print(atom_str)
                atom_ = atom_str[1:-1].split(',')
                list_atom.append([ atom_[0][1:-1],
                        atom_[1][1:-1],
                        atom_[2][1:-1] ])
            return list_atom
