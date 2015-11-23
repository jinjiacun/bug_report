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
from threading import Thread
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class app(Process):
    def __init__(self,recv_conn=None,send_conn=None):
        super(app,self).__init__()
        if recv_conn:
            self.recv_conn = recv_conn
        if send_conn:
            self.send_conn = send_conn
        self.ctl = True

    def run(self):
        app = QtGui.QApplication(sys.argv)

        mainWindow = MainWindow(self,self.send_conn)
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
            message_send = {'command':'start_app','params':{'app':'master','function':{'name':'start_app_mqtt','param':''}},'message':'启动app_mqtt'}
            message_send['params']['function']['param'] = user_name
            self.send_conn.send(message_send)

        #主界面
        mainWindow.setGeometry(100, 100, 800, 500)
        mainWindow.showMaximized()

        #注册管道侦听线程
        self.t = Thread(target=self.listen_pipe,args=(mainWindow,))
        self.t.start()
        sys.exit(app.exec_())

    #侦听管道
    def listen_pipe(self,mainWindow):
        while self.ctl:
            try:
                message = self.recv_conn.recv()
            except IOError,e:
                print e.message
            else:
                print 'listen_pipe'
                print message
                mainWindow.touch_sig(message['params'])

    def close(self):
        self.ctl=False
        time.sleep(2)
        self.recv_conn.close()
        sys.exit()


if __name__ == '__main__':
    my_app = app()
    my_app.start()