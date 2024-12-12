'''
Created on 2024/12/10

@author: sue-t
'''

from main import *
from com.client import client

class Sequence(object):
    def __init__(self, port):
        '''
        Constructor
        '''
        self.port = port

    def listen(self, str_msg, database):
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
                    list_str[3][1:-1],
                    list_str[4][1:-1],
                    list_str[5][1:-1])
            return str_msg
        if str_msg.startswith(REP_FILE):
            list_str = str_msg[len(REP_FILE):].split(',')
            str_msg = database.replace_file(list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1],
                    list_str[3][1:-1],
                    list_str[4][1:-1],
                    list_str[5][1:-1])
            return str_msg

        if str_msg.startswith(ASK_DOC):
            list_doc = database.select_document()
            if len(list_doc) == 0:
                return("[]")
            ret_msg = r'["' + r',"'.join(list_doc[0]) + r'"]'
            return ret_msg
        if str_msg.startswith(ASK_CUST):
            list_cust = database.select_customer()
            if len(list_cust) == 0:
                return("[]")
            ret_msg = r'["' + r',"'.join(list_cust[0]) + r'"]'
            return ret_msg
        if str_msg.startswith(ASK_SECT):
            list_sect = database.select_section()
            if len(list_sect) == 0:
                return("[]")
            ret_msg = r'["' + r',"'.join(list_sect[0]) + r'"]'
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
            ret_msg = r'["' + r',"'.join(list_origin[0]) + r'"]'
            return ret_msg
        if str_msg.startswith(ASK_IN_BY):
            list_by = database.select_in_by()
            if len(list_by) == 0:
                return("[]")
            ret_msg = r'["' + r',"'.join(list_by[0]) + r'"]'
            return ret_msg

        if str_msg.startswith(ASK_OUT):
            list_out = database.select_output(
                    str_msg[len(ASK_OUT):])
            if len(list_out) == 0:
                return("[]")
            ret_msg = r'["{}","{}","{}"]'. \
                    format(list_out[0][1],
                           list_out[0][2], list_out[0][3])
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

        if str_msg.startswith(ASK_OUT_DELIV):
            list_delivery = database.select_out_delivery()
            if len(list_delivery) == 0:
                return("[]")
            ret_msg = r'["' + r',"'.join(list_delivery[0]) + r'"]'
            return ret_msg
        if str_msg.startswith(ASK_OUT_BY):
            list_by = database.select_out_by()
            if len(list_by) == 0:
                return("[]")
            ret_msg = r'["' + r',"'.join(list_by[0]) + r'"]'
            return ret_msg

        return ("??")

    def send_ask_file(self, str_file_name):
        client_ = client()
        str_send = "{}{}".format(ASK_FILE, str_file_name)
        str_rcv = client_.send(self.port, str_send)
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
            str_document, str_customer, str_section,
            str_before, str_latest):
        client_ = client()
        str_send = r'{}"{}","{}","{}","{}","{}","{}"'. \
                format(INS_FILE, str_file_name,
                str_document, str_customer, str_section,
                str_before, str_latest)
        str_rcv = client_.send(self.port, str_send)
        return str_rcv

    def send_replace_file(self, str_file_name,
            str_document, str_customer, str_section,
            str_before, str_latest):
        client_ = client()
        str_send = r'{}"{}","{}","{}","{}","{}","{}"'. \
                format(REP_FILE, str_file_name,
                str_document, str_customer, str_section,
                str_before, str_latest)
        str_rcv = client_.send(self.port, str_send)
        return str_rcv

    def send_ask_document(self):
        client_ = client()
        str_send = ASK_DOC
        str_rcv = client_.send(self.port, str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            print(list_atom)
            return list_atom

    def send_ask_customer(self):
        client_ = client()
        str_send = ASK_CUST
        str_rcv = client_.send(self.port, str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            print(list_atom)
            return list_atom

    def send_ask_section(self):
        client_ = client()
        str_send = ASK_SECT
        str_rcv = client_.send(self.port, str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            print(list_atom)
            return list_atom


    def send_ask_in(self, str_file_name):
        client_ = client()
        str_send = "{}{}".format(ASK_IN, str_file_name)
        str_rcv = client_.send(self.port, str_send)
        print(str_rcv)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            return (list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1])

    def send_insert_in(self, str_file_name,
            str_date, str_origin, str_by):
        client_ = client()
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(INS_IN, str_file_name,
                str_date, str_origin, str_by)
        str_rcv = client_.send(self.port, str_send)
        return str_rcv

    def send_replace_in(self, str_file_name,
            str_date, str_origin, str_by):
        client_ = client()
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(REP_IN, str_file_name,
                str_date, str_origin, str_by)
        str_rcv = client_.send(self.port, str_send)
        return str_rcv


    def send_ask_in_origin(self):
        client_ = client()
        str_send = ASK_IN_ORIGIN
        str_rcv = client_.send(self.port, str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            print(list_atom)
            return list_atom

    def send_ask_in_by(self):
        client_ = client()
        str_send = ASK_IN_BY
        str_rcv = client_.send(self.port, str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            print(list_atom)
            return list_atom


    def send_ask_out(self, str_file_name):
        client_ = client()
        str_send = "{}{}".format(ASK_OUT, str_file_name)
        str_rcv = client_.send(self.port, str_send)
        print(str_rcv)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            return (list_str[0][1:-1],
                    list_str[1][1:-1],
                    list_str[2][1:-1])

    def send_insert_out(self, str_file_name,
            str_date, str_deliv, str_by):
        client_ = client()
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(INS_OUT, str_file_name,
                str_date, str_deliv, str_by)
        str_rcv = client_.send(self.port, str_send)
        return str_rcv

    def send_replace_out(self, str_file_name,
            str_date, str_deliv, str_by):
        client_ = client()
        str_send = r'{}"{}","{}","{}","{}"'. \
                format(REP_OUT, str_file_name,
                str_date, str_deliv, str_by)
        str_rcv = client_.send(self.port, str_send)
        return str_rcv


    def send_ask_out_delivery(self):
        client_ = client()
        str_send = ASK_OUT_DELIV
        str_rcv = client_.send(self.port, str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            print(list_atom)
            return list_atom

    def send_ask_out_by(self):
        client_ = client()
        str_send = ASK_OUT_BY
        str_rcv = client_.send(self.port, str_send)
        if str_rcv == "[]":
            return None
        else:
            list_str = str_rcv[1:-1].split(',')
            list_atom = []
            for atom in list_str:
                list_atom.append(atom[1:-1])
            print(list_atom)
            return list_atom