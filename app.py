# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4 import QtGui
from jimLib.ui.App import MainWindow
from jimLib.ui.Login import login
from jimLib.lib.business import business
import paho.mqtt.client as mqtt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CMqtt():
    def __init__(self,topic='#'):
        CMqtt.topic = topic
        self.my_client = mqtt.Client()
        self.my_client.on_connect = self.on_connect
        self.my_client.on_message = self.on_message
        self.my_client.connect("192.168.1.131", 1883, 60)
        self.my_client.loop_start()

    def on_connect(self,client, userdata,flag, rc):
        client.subscribe(CMqtt.topic)

    def on_message(self,client, userdata, msg):
        #调用消息提示
        mainWindow.touch_sig(str(msg.payload))
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    #登录界面
    loginWindow = login(mainWindow)
    loginWindow.setupUi(loginWindow)
    is_login_ok = False
    global user_name
    if loginWindow.exec_() == QtGui.QDialog.Accepted:
        #print "user_name:%s\n"%loginWindow.user_name
        #print "passwd:%s\n"%loginWindow.passwd
        #检查用户名和密码是否正确
        user_name = str(loginWindow.user_name)
        #开启mqtt推送
        my_mqtt = CMqtt("debug_bug/"+user_name)
        #重设左导航
        mainWindow.createToolBoxEx()
        mainWindow.my_time()
        mainWindow.timer.stop()

    #主界面
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.showMaximized()

    sys.exit(app.exec_())
