# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4 import QtGui
from jimLib.ui.App import MainWindow
from jimLib.ui.Login import login
from jimLib.lib.business import business
from multiprocessing import Process,Pipe

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class app():
    def __init__(self,conn=None):
        self.conn = conn
        pass

    def start(self):
        app = QtGui.QApplication(sys.argv)

        mainWindow = MainWindow()
        #登录界面
        loginWindow = login(mainWindow)
        loginWindow.setupUi(loginWindow)
        if loginWindow.exec_() == QtGui.QDialog.Accepted:
            #print "user_name:%s\n"%loginWindow.user_name
            #print "passwd:%s\n"%loginWindow.passwd
            #检查用户名和密码是否正确
            user_name = str(loginWindow.user_name)
            #开启mqtt推送
            #my_mqtt = CMqtt("debug_bug/"+user_name)
            #重设左导航
            mainWindow.createToolBoxEx()
            mainWindow.my_time()
            mainWindow.timer.stop()
            #发送消息给监控进程,以便启动mqtt服务
            message = {'command':'send','params':{'app':'master','function':{'name':'start_app_mqtt','param':''}},'message':'启动app_mqtt'}
            message['params']['function']['param'] = user_name
            print message
            self.conn.send(message)

        #主界面
        mainWindow.setGeometry(100, 100, 800, 500)
        mainWindow.showMaximized()

        sys.exit(app.exec_())

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    my_app = app()
    my_app.start()