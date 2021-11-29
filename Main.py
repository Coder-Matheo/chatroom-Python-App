#für die kivy entwicklung werden alle die bibiothek benötigt

#python -m pip install https://github.com/kivy/kivy/archive/master.zip  kivy installtion
#python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew;
#pip install matplotlib==3.0.0

import kivy
import requests
import os
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition , FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
#from datetime import datetime, timedelta, date
from kivy.graphics import Color
from kivy.graphics import Canvas
from kivy.graphics import Rectangle
from kivy.graphics import RoundedRectangle
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.core.window import Window
import csv
import pandas as pd
import random
import sqlite3
import re
import socket
import time
import datetime
from api_docu import api_key
from Database_query_docu.query_db import query_db_interface

from api_docu.api_key import reg_location
from api_docu import api_key
#laden alle die kv file

Builder.load_file('myMain.kv')
Builder.load_file('dis_view.kv')
Builder.load_file('Chat.kv')
Builder.load_file('info_graphi.kv')
Builder.load_file('viewChatFile.kv')

#bildschirm size und kivy version
Window.size = (400,680)
Config.set('graphics', 'resizable', True)
kivy.require('1.9.0')
#kombinerte port und server-IP zu socket einrichten
HEADER = 64
PORT = 5050  # port yahoo masanger
FORMAT = 'utf-8'

# DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"  # depends which client(ipv4) to be connecting
# SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
# The TCP connection used (socket.AF_INET)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)



#difinete local time-datum zu benötigten in App
date_and_time = time.localtime()
timestamp = 1528797322
date_time = datetime.datetime.fromtimestamp(timestamp)

dater = time.strftime("%Y-%m-%d", date_and_time)
timer = time.strftime("%H:%M:%S", date_and_time)
timerCSV = time.strftime("%H:%M", date_and_time)
clockTime = time.strftime("%H:%M",date_and_time)
clockTimeHour = time.strftime("%H",date_and_time)
clockTimeMinute = time.strftime("%M",date_and_time)
dateDayName = date_time.strftime("%A")
dateMonthDayNumber = date_time.strftime("%B %d")






lst_msg_view = []
lst_msg_view_new = []





class Display_view_layout(FloatLayout):
    def __init__(self, **kwargs):
        super(Display_view_layout, self).__init__(**kwargs)

class Display_start_entrace(Screen):
    def __init__(self, **kwargs):
        super(Display_start_entrace, self).__init__(**kwargs)
        clock_display = self.ids.clockHour
        clock_display.text = str(clockTimeHour)
        clock_display = self.ids.clockMinute
        clock_display.text = str(clockTimeMinute)

        #Das wird überprüft internet connection, wenn ja, wird die function wetter aufrufen
        if api_key.connection_check() == True:
            api_key.connection_check()
            self.weather()

        else:
            print(api_key.connection_check())


    def weather(self):
        res = api_key.reg_location
        loc = res.json()
        location = loc['city']
        api_keyHold = api_key.api
        path_apiweatherHold = api_key.path_weatherIpi
        complate_api_link= path_apiweatherHold +location+"&appid="+api_keyHold

        api_link = requests.get(complate_api_link)
        api_data = api_link.json()
        temp_kelvin = api_data['main']['temp']
        temp_celsius = temp_kelvin -273.15

        iconWaether = self.ids.picWeather
        iconWaether.source = 'wheatherPic/{}.png'.format(api_data['weather'][0]['icon'])

        Temparator_View = self.ids.Temp_id
        Temparator_View.text = str('{0:,.2f}'.format(temp_celsius)+' C')

        dayname = self.ids.dayName_view
        dayname.text = str(dateDayName)
        monthDayNum = self.ids.monthDayNumber
        monthDayNum.text = str(dateMonthDayNumber)


class User_intro_Info(FloatLayout):
    def __init__(self, **kwargs):
        super(User_intro_Info, self).__init__(**kwargs)


#MainMenu ist eingang die App, wird hier alle userinformation abgeben und in DB speichert



class MainMenu(Screen):

    def __init__( self, **kwargs ):
        super( MainMenu, self ).__init__( **kwargs )


    # (1, 'Matheo', 'ali.dinarvand1370@gmail.com', 'Matheo1370?', 'Germany')
    #wenn nicht exist würde,wird in DB speichern
    def entryInfo(self, name, email, passwort, country):
        email_ver = query_db_interface().email_pass_verifaction(email, passwort)
        #pass_name_ver = query_db_interface().pass_name_verify(name,passwort)
        print("Selected",query_db_interface().select_all_query_db())
        #überprüfen alle eingabeinformation
        sel_user_db = query_db_interface().select_and_query_db(name, email, passwort, country)
        try:
            if sel_user_db[0][1] == name and sel_user_db[0][2] == email and sel_user_db[0][3] == passwort and email_ver == True :

                #Nach prüfung spring zur chat site
                self.ids.chatButton.disabled = False
                self.ids.chatButton.opacity = 1
                self.ids.failedMsg.text = "Let's Chat"
                print('Find User')
            else:
                #query_db_interface().insert_query_db(self.name,self.email,self.passwort,self.country)
                # Nach prüfung spring zur chat site
                print('New User Created')
        except:
            self.ids.failedMsg.text = "Try Again"
            print("Failed")


class Chat_site(Widget):
    def __init__(self, **kwargs):
        super(Chat_site, self).__init__(**kwargs)


class Chat(Screen):
    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)
        clock = self.ids.clock
        clock.text = str(clockTime)


        #show the location user
        res = reg_location
        location = res.json()

        loc = self.ids.loc
        loc.text = location['city']




    # (1, 'Matheo', 'ali.dinarvand1370@gmail.com', 'Matheo1370?', 'Germany')

    def message_recv(self, msg):

        try:
            self.usernameDB = query_db_interface().show_username_chat()
            self.ids.usernameChat.text = self.usernameDB
            self.userMsgCSV = msg

            msg = query_db_interface().show_username_chat() + ' : ' + msg

            message = msg.encode(FORMAT)
            msg_length = len(message)
            #Nachricht größen
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))

            print(message)

            #send message and length to socket
            client.send(send_length)
            client.send(message)
            #recive the user port from socket
            ir = client.recv(2048).decode(FORMAT)

            ir = ir.replace(',', '\n')
            ir = ir.replace("'", " ")
            msgChat = self.ids.msgChat
            msgChat.text = str(ir[2:-1])

            #Sending Message to Label for showing in Screen User
            if ir[2:ir.index('>')-1]:
                ir = ir.replace(',', '\n')
                ir = ir.replace("'"," ")
                msgChat = self.ids.msgChat
                msgChat.text = str(ir[2:-2])
                print(msgChat)
        except:
            pass
        finally:
            # CSV file wurde erstellt, für die Nachrichten zu speichern
            with open('userActivity.csv ', 'a', newline='') as tracfile:
                fieldhead = ['userMessage','username',  'DateChat', 'TimeChat']
                writertrac = csv.DictWriter(tracfile, fieldnames=fieldhead)
                #writertrac.writeheader()

                writertrac.writerow({'userMessage': self.userMsgCSV,'username': self.usernameDB,
                                     'DateChat': str(dater),'TimeChat': str(timerCSV)})





class View_site(Screen):
    def __init__(self, **kwargs):
        super(View_site, self).__init__(**kwargs)
        self.i = 1

    #night-day mood in show-message file
    def night_day_mood(self):
        if (self.i %2 == 1):
            self.ids.canColor.my_color=rgba('#0d1328')
            self.ids.boxColor_id.mybox_color=(1,1,1)
            self.ids.footboxColor.myfootColor=(1,1,1)
            self.i = self.i + 1
        elif(self.i%2==0):
            self.ids.canColor.my_color = (1, 1, 1)
            self.ids.boxColor_id.mybox_color = ('#333333')
            self.ids.boxColor_id.mybox_color = rgba('#0d1328')
            self.ids.footboxColor.myfootColor = rgba('#0d1328')
            self.i = self.i + 1


    def view_msg_csv(self, datum):
        self.datum = datum
        print(self.datum)

        data = pd.read_csv('userActivity.csv', index_col=False)
        messageToshow = data[data['DateChat'] == datum]['userMessage']
        #dateMessageToshow = data[data['DateChat'] == datum]['DateChat']
        timeMessageToshow = data[data['DateChat'] == datum]['TimeChat']

        msgviewBox = self.ids.msgBoxId
        msgviewBox.text = str(messageToshow)
        ls = ''
        for med in messageToshow:
            ls += med


        print(ls)
        print(messageToshow)


        msgTimeBox = self.ids.msgTimeId
        msgTimeBox.text = str(timeMessageToshow)
        print(timeMessageToshow)




class InfoGraphi(Screen):
    def __init__(self, **kwargs):
        super(InfoGraphi, self).__init__(**kwargs)


sm = ScreenManager()

sm.add_widget(Display_start_entrace(name='display_view'))
sm.add_widget(MainMenu(name='mainmenu'))
sm.add_widget(View_site(name='view_chat'))
sm.add_widget(InfoGraphi(name='infoGraphi'))
sm.add_widget(Chat(name='chatting'))

class ChattProjekt(App):
    def build(self):
        return sm

if __name__ == "__main__":
    ChattProjekt().run()