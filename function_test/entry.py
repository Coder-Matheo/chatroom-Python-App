import re
import sqlite3

from numpy import random


def entryInfo():
    nameInfo='Matheo'
    emailInfo='ali.dinarvand1370@gmail.com'
    passwortInfo='Matheo1370'
    country ='Germany'
    # filter entry E-mail address
    filterEmail = re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", emailInfo)

    # verify alle entry the Informationbox
    if (nameInfo != "" and filterEmail and passwortInfo != "" and len(passwortInfo) > 8):

        try:
            # try to connecting with the Database
            conn = sqlite3.connect('User_Info_DB.db')
            # prepared=True
            c = conn.cursor()

            # Creating Database for save User Information in Sqlite3
            #
            c.execute('''CREATE TABLE IF NOT EXISTS user_infoBank( 
                                                        User_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        User_name TEXT  NULL,
                                                        User_email TEXT NULL,
                                                        User_pass TEXT NOT NULL,
                                                        Country TEXT NULL)''')

            conn.commit()

            ##self.c.execute("""INSERT OR IGNORE INTO user_infoBank VALUES(1, 'Matheo', 'ali.dinarvand1370@gmail.com','Matheo1370','Germany')""")
            ##self.conn.commit()

            # aprove the input value
            c.execute("SELECT * FROM user_infoBank WHERE User_name=? OR User_email=? OR User_pass=?",
                           (nameInfo, emailInfo, passwortInfo,))
            if (c.fetchone()):
                c.execute("SELECT * FROM user_infoBank WHERE User_name=? AND User_email=? AND User_pass=?",
                               (nameInfo, emailInfo, passwortInfo,))

                if (c.fetchone()):

                    # aprove the input value, the aren't empty
                    if (nameInfo != '' and nameInfo != '' and passwortInfo != ''):
                        # open the chat window
                        # self._popups['chatsite'].open()

                        userNameVerify = nameInfo
                        emailInfoVerify = emailInfo
                        passwortInfoVerify = passwortInfo

                        c.execute('SELECT * FROM user_infoBank')
                        print(c.fetchall())
                else:

                    # After verify user Information, if haven't account, then create new account and save in Database
                    c.execute("INSERT OR IGNORE INTO user_infoBank VALUES(?, ?, ?, ?, ?)",
                                   (str(random.randint(0, 100)), nameInfo, emailInfo,passwortInfo, country,))

                    conn.commit()
                    # after creating account, then jumping to chat site
                    # self._popups['chatsite'].open()



        except sqlite3.Error as error:
            print("Error : ", error)
            conn.close()
        finally:
            if (conn):
                # conn.close()
                print("sqlite connection")


entryInfo()
