'''
Created on 2024/12/08

@author: sue-t
'''

import sqlite3

class WasurejiDB(object):
    
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
    
    def term(self):
        self.cur.close()
        self.conn.close()

    def create_table(self):
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS ' \
            'base(file STRING PRIMARY KEY,' \
                'document STRING,' \
                'customer STRING,' \
                'section STRING,' \
                'before STRING,'
                'latest STRING)')
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS ' \
            'input(file STRING PRIMARY KEY,' \
                'date STRING,' \
                'origin STRING,' \
                'by STRING)')
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS ' \
            'output(file STRING,' \
                'date STRING,' \
                'delivery STRING,' \
                'by STRING)')
        self.conn.commit()

    def execute_sql(self, str_sql):
        try:
            self.cur.execute(str_sql)
        except sqlite3.Error as e:
            return f"{e}"
        list_ = self.cur.fetchall()
        print(list_)
        # str_result = str(list_)
        str_result = ""
        if type(list_) is list:
            str_result += "[ \n"
            for atom_ in list_:
                # print(atom_)
                if type(atom_) is tuple:
                    str_result += "[ "
                    for val_ in atom_:
                        # print(val_)
                        str_result += str(val_)
                        str_result += ", "
                    str_result = str_result[:-2] + " ],\n"
                else:
                    str_result += str(atom_) + ", "
            str_result = str_result[:-2] + "\n]"
        else:
            str_result += str(list_)
        # print(str_result)
        return str_result
    
    def commit(self):
        try:
            self.cur.commit()
        except sqlite3.Error as e:
            return f"{e}"
        return "ok"
        
    def rollback(self):
        try:
            self.cur.rollback()
        except sqlite3.Error as e:
            return f"{e}"
        return "ok"

    def select_file(self, file_name):
        str_sql = r'SELECT file, document, customer, section,' \
                'before, latest' \
                ' FROM base WHERE file = "{}"'. \
                format(file_name)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
        except sqlite3.Error as e:
            print(f"error_db: {e}")
            exit(-1)
        list_base = self.cur.fetchall()
        # print(list_base)
        return list_base

    def insert_file(self, file, document, customer, section,
            before, latest):
        str_sql = r'INSERT INTO base' \
                '(file, document, customer, section,' \
                'before, latest)' \
                ' VALUES("{}", "{}", "{}", "{}", "{}", "{}")'. \
                format(file, document, customer, section,
                before, latest)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"

    def replace_file(self, file, document, customer, section,
            before, latest):
        str_sql = r'UPDATE base SET ' \
                'document = "{}", customer="{}", ' \
                'section = "{}",' \
                'before ="{}", latest="{}"' \
                ' WHERE file = "{}"'. \
                format(document, customer, section,
                before, latest, file)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"

    def select_document(self):
        str_sql = r'SELECT DISTINCT document' \
                ' FROM base'
        # print(str_sql)
        self.cur.execute(str_sql)
        list_document = self.cur.fetchall()
        # print(list_document)
        return list_document
        
    def select_customer(self):
        str_sql = r'SELECT DISTINCT customer' \
                ' FROM base'
        # print(str_sql)
        self.cur.execute(str_sql)
        list_document = self.cur.fetchall()
        # print(list_document)
        return list_document
        
    def select_section(self):
        str_sql = r'SELECT DISTINCT section' \
                ' FROM base'
        # print(str_sql)
        self.cur.execute(str_sql)
        list_document = self.cur.fetchall()
        # print(list_document)
        return list_document

    def select_input(self, file_name):
        str_sql = r'SELECT file, date, origin, by' \
                ' FROM input WHERE file = "{}"'. \
                format(file_name)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
        except sqlite3.Error as e:
            print(f"error_db: {e}")
            exit(-1)
        list_input = self.cur.fetchall()
        # print(list_input)
        return list_input

    def insert_input(self, file, date, origin, by):
        str_sql = r'INSERT INTO input' \
                '(file, date, origin, by)' \
                ' VALUES("{}", "{}", "{}", "{}")'. \
                format(file, date, origin, by)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"

    def replace_input(self, file, date, origin, by):
        str_sql = r'UPDATE input SET ' \
                'date = "{}", origin="{}", ' \
                'by = "{}"' \
                ' WHERE file = "{}"'. \
                format(date, origin, by, file)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"


    def select_in_origin(self):
        str_sql = r'SELECT DISTINCT origin' \
                ' FROM input'
        # print(str_sql)
        self.cur.execute(str_sql)
        list_origin = self.cur.fetchall()
        # print(list_origin)
        return list_origin
        
    def select_in_by(self):
        str_sql = r'SELECT DISTINCT by' \
                ' FROM input'
        # print(str_sql)
        self.cur.execute(str_sql)
        list_by = self.cur.fetchall()
        # print(list_by)
        return list_by


    def select_output(self, file_name):
        str_sql = r'SELECT file, date, delivery, by' \
                ' FROM output WHERE file = "{}"'. \
                format(file_name)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
        except sqlite3.Error as e:
            print(f"error_db: {e}")
            exit(-1)
        list_output = self.cur.fetchall()
        return list_output

    def insert_output(self, file, date, delivery, by):
        str_sql = r'INSERT INTO output' \
                '(file, date, delivery, by)' \
                ' VALUES("{}", "{}", "{}", "{}")'. \
                format(file, date, delivery, by)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"

    def replace_output(self, file, date, delivery, by):
        # 複数指定では、使わない
        str_sql = r'UPDATE output SET ' \
                'date = "{}", delivery="{}", ' \
                'by = "{}"' \
                ' WHERE file = "{}"'. \
                format(date, delivery, by, file)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"

    def delete_output(self, file):
        str_sql = r'DELETE output ' \
                ' WHERE file = "{}"'. \
                format(file)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"


    def select_out_delivery(self):
        str_sql = r'SELECT DISTINCT delivery' \
                ' FROM output'
        # print(str_sql)
        self.cur.execute(str_sql)
        list_delivery = self.cur.fetchall()
        return list_delivery
        
    def select_out_by(self):
        str_sql = r'SELECT DISTINCT by' \
                ' FROM output'
        # print(str_sql)
        self.cur.execute(str_sql)
        list_by = self.cur.fetchall()
        return list_by


if __name__ == '__main__':
    # dbname = dir_name + '\\' + WasurejiDB.DATABASE_NAME
    database = WasurejiDB(".\\wasureji.db")
    database.create_table()
    l = database.select_file("abc.pdf")
    print(l)
    database.insert_file(
            "def.pdf", "修正申告書", "佐藤　栄作", "令和４年",
            "", "")
    if len(l) == 0:
        database.insert_file(
                "abc.pdf", "確定申告書", "佐藤　栄作", "令和４年",
                "", "")
        l = database.select_file("abc.pdf")
        print(l)
    l = database.select_document()
    print(l)
    database.term()


        