import re
import sqlite3

from numpy import random


#aufrufen werden alle benötigte Abfrage von DB zu Main.py
#[(1, 'Matheo', 'ali.dinarvand1370@gmail.com', 'Matheo1370', 'Germany')]

class query_db_interface():
    def __init__(self):
        self.conn = sqlite3.connect('User_Info_DB.db')
        self.c = self.conn.cursor()
        #self.c.execute("UPDATE user_infoBank SET User_name='Ali' WHERE User_id=1")
        #self.conn.commit()

    #wird neu Table in DB erstellt, wenn nicht exist
    def create_table_db(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS user_infoBank( 
                                    User_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    User_name TEXT  NULL,
                                    User_email TEXT NULL,
                                    User_pass TEXT NOT NULL,
                                    Country TEXT NULL)''')

            self.conn.commit()
        except sqlite3.Error as error:
            self.conn.close()
            return 'error creating Database, error'+ error



    def select_and_query_db(self, name, email, password, country):
        try:

            self.c.execute("SELECT * FROM user_infoBank WHERE User_name=? AND User_email=? AND User_pass=?",(name,email,password))
            ret = self.c.fetchall()
            global n
            n = name
            self.e = email
            self.p = password

            return ret
        except:
            print("Failed")

    def show_username_chat(self):
        return n




    def select_or_query_db(self, name, email, password, country):
        self.c.execute("SELECT * FROM user_infoBank WHERE User_name=? OR User_email=?",(name,email,))
        return self.c.fetchone()

    def select_and_or_query_db(self, name, email, password, country):
        or_query = self.c.execute("SELECT * FROM user_infoBank WHERE User_name=? AND User_email=?", (name, email,))
        or_query.fetchone()
        and_query = self.c.execute("SELECT * FROM user_infoBank WHERE User_email=? AND User_pass=?", (email,password,))
        and_query.fetchone()
        if (or_query.fetchone() or and_query.fetchone()):
            return True
        else:
            return False

    def select_all_query_db(self):
        all_query = self.c.execute("SELECT * FROM user_infoBank")
        all_user = all_query.fetchall()
        return all_user


    def insert_query_db(self, name, email, password, country):
        self.c.execute("INSERT OR IGNORE INTO user_infoBank VALUES(?, ?, ?, ?, ?)",
                       (str(random.randint(0, 100)), name, email, password, country,))
        self.conn.commit()
        return 'Created new User'

    def del_query_db(self):
        self.c.execute("DELETE FROM user_infoBank WHERE User_pass ='12345asdf'")
        self.conn.commit()

    def email_pass_verifaction(self, email, password):

        email_aprove = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", email)

        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(reg)
        mat = re.search(pat, password)

        if bool(email_aprove) == True and bool(mat) == True:
            return True
        else:
            return False
