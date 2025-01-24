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
            # COMMIT,ROLLBACK は、ユーザー任せ
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
            self.conn.commit()
        except sqlite3.Error as e:
            return f"{e}"
        return "ok"
        
    def rollback(self):
        try:
            self.conn.rollback()
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

    def insert_file(self, file,
            document, customer, section):
            # before, latest):
        (msg, old_latest) = self.set_history(file,
                document, customer, section)
        # print(msg)
        # print(old_latest)
        if (old_latest == None):
            old_latest = ""
        str_sql = r'INSERT INTO base' \
                '(file, document, customer, section,' \
                'before)' \
                ' VALUES("{}", "{}", "{}", "{}", "{}")'. \
                format(file, document, customer, section,
                old_latest)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"

    def replace_file(self, file,
            document, customer, section,
            old_document, old_customer, old_section):
        rv = self.reset_history(file,
                old_document, old_customer, old_section)
        if (rv == None):
            (_msg, old_latest) = self.set_history(file,
                    document, customer, section)
            # print(msg)
            # print(old_latest)
            if (old_latest == None):
                old_latest = ""
        else:
            old_latest = ""
        str_sql = r'UPDATE base SET ' \
                'document = "{}", customer="{}", ' \
                'section = "{}",' \
                'before ="{}", latest=""' \
                ' WHERE file = "{}"'. \
                format(document, customer, section,
                old_latest, file)
        # print(str_sql)
        try:
            self.cur.execute(str_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            return f"error_db:{e}"
        return "ok"


    def exist_file(self, file_name):
        # 削除も名前変更も共用
        str_sql = r'SELECT file' \
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


    def set_history(self, file, document, customer, section):
        str_sql_select = r'SELECT file, before, latest ' \
                'FROM base WHERE ' \
                'document = "{}" AND customer="{}" ' \
                'AND section = "{}"'. \
                format(document, customer, section)
        # print(str_sql_select)
        try:
            self.cur.execute(str_sql_select)
        except sqlite3.Error as e:
            return (f"error_db:{e}", None)
        list_ = self.cur.fetchall()
        if len(list_) == 0:
            return ("ok", None)
        # 現時点のlatestを探す
        for base_ in list_:
            if (base_[2] == None) or (base_[2] == ""):
                break
        else:
            return ("error:not exist least", None)
        
        old_latest = base_[0]
        str_sql_update = r'UPDATE base SET ' \
                'latest="{}"' \
                ' WHERE file="{}" AND ' \
                'document = "{}" AND customer="{}" AND ' \
                'section = "{}"'. \
                format(file, base_[0],
                        document, customer, section)
        # print(str_sql_update)
        try:
            self.cur.execute(str_sql_update)
        except sqlite3.Error as e:
            return (f"error_db:{e}", None)
        
        while not((base_[1] == None) or (base_[1] == "")):
            before_file = base_[1]
            for before_ in list_:
                if (before_[0] == before_file):
                    str_sql_update = r'UPDATE base SET ' \
                            'latest="{}"' \
                            ' WHERE file="{}" AND ' \
                            'document = "{}" AND customer="{}" ' \
                            'AND section = "{}"'. \
                            format(file, before_[0],
                                    document, customer, section)
                    # print(str_sql_update)
                    try:
                        self.cur.execute(str_sql_update)
                    except sqlite3.Error as e:
                        self.conn.rollback()
                        return (f"error_db:{e}", None)
                    base_ = before_
                    break
            else:
                self.conn.rollback()
                return ("error:not exist before", None)
            # print(base_)
        self.conn.commit()
        return ("ok", old_latest)

    def reset_history(self, file,
            document, customer, section):
        str_sql_select = r'SELECT file, before, latest ' \
                'FROM base WHERE ' \
                'document = "{}" AND customer="{}" ' \
                'AND section = "{}"'. \
                format(document, customer, section)
        # print(str_sql_select)
        try:
            self.cur.execute(str_sql_select)
        except sqlite3.Error as e:
            return (f"error_db:{e}", None)
        list_ = self.cur.fetchall()
        if len(list_) == 0:
            return ("ok", None)
        # 現時点のlatestを探す
        for base_ in list_:
            if (base_[2] == None) or (base_[2] == ""):
                break
        else:
            return ("error:not exist least", None)
        
        if base_[0] == file:
            # 指定されたファイルがlatestの場合
            # print("指定されたファイルがlatestの場合")
            new_latest = base_[1]
            if (not((new_latest == None) or (new_latest == ""))):
                str_sql_update = r'UPDATE base SET ' \
                        'latest=""' \
                        ' WHERE file="{}" AND ' \
                        'document = "{}" AND customer="{}" AND ' \
                        'section = "{}"'. \
                        format(new_latest,
                                document, customer, section)
                # print(str_sql_update)
                try:
                    self.cur.execute(str_sql_update)
                except sqlite3.Error as e:
                    return (f"error_db:{e}", None)
                if ((base_[1] == None) or (base_[1] == "")):
                    return None
                for before_ in list_:
                    if (before_[0] == base_[1]):
                        break
                else:
                    self.conn.rollback()
                    return ("error:not exist before", None)
                base_ = before_
                while not((base_[1] == None) or (base_[1] =="")):
                    before_file = base_[1]
                    for before_ in list_:
                        if (before_[0] == before_file):
                            str_sql_update = r'UPDATE base SET ' \
                                    'latest="{}"' \
                                    ' WHERE file="{}" AND ' \
                                    'document = "{}" AND customer="{}" ' \
                                    'AND section = "{}"'. \
                                    format(new_latest, before_[0],
                                            document, customer, section)
                            # print(str_sql_update)
                            try:
                                self.cur.execute(str_sql_update)
                            except sqlite3.Error as e:
                                self.conn.rollback()
                                return (f"error_db:{e}", None)
                            base_ = before_
                            break
                    else:
                        self.conn.rollback()
                        return ("error:not exist before", None)
                    # print(base_)
        else:
            # 指定されたファイルがlatestでない場合
            # base_ がlatest
            # print("base_ がlatest")
            while not((base_[1] == None) or (base_[1] == "")):
                if base_[1] == file:
                    # print("base_[1] == file")
                    for before_ in list_:
                        if before_[0] == file:
                            break
                    else:
                        self.conn.rollback()
                        return ("error:not exist before", None)
                    # for before_before in list_:
                    #     if before_before[0] == before_[1]:
                    #         break;
                    # else:
                    #     self.conn.rollback()
                    #     return ("error:not exist before", None)
                    # print(before_)
                    # print(before_before)
                    str_sql_update = r'UPDATE base SET ' \
                            'before="{}"' \
                            ' WHERE file="{}" AND ' \
                            'document = "{}" AND customer="{}" ' \
                            'AND section = "{}"'. \
                            format(before_[1],
                                    base_[0],
                                    document, customer, section)
                    # print(str_sql_update)
                    try:
                        self.cur.execute(str_sql_update)
                    except sqlite3.Error as e:
                        self.conn.rollback()
                        return (f"error_db:{e}", None)
                    return None
                for before_ in list_:
                    if before_[0] == base_[1]:
                        break
                else:
                    self.conn.rollback()
                    return ("error:not exist before", None)
                base_ = before_
            else:
                self.conn.rollback()
                return ("error:not exist before", None)
        return None

    def select_history(self, document, customer, section):
        str_sql_select = r'SELECT file, before, latest ' \
                'FROM base WHERE ' \
                'document = "{}" AND customer="{}" ' \
                'AND section = "{}"'. \
                format(document, customer, section)
        # print(str_sql_select)
        try:
            self.cur.execute(str_sql_select)
        except sqlite3.Error as e:
            return (f"error_db:{e}", None)
        list_ = self.cur.fetchall()
        # print(list_)
        if len(list_) == 0:
            return ("ok", None)
        return list_
    
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


        