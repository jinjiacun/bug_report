#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


# This is only needed for Python v2 but is harmless for Python v3.

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
import paho.mqtt.client as mqtt
import os

try:
    import systray_rc3
except ImportError:
    import systray_rc2


class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__()

        self.createIconGroupBox()

        self.createActions()
        self.createTrayIcon()

        self.l_name = QtGui.QLabel(u"用户名:")
        self.l_name.setGeometry(QtCore.QRect(50, 40, 54, 12))
        self.l_passwd = QtGui.QLabel(u"密码:")
        self.l_passwd.setGeometry(QtCore.QRect(50, 100, 54, 12))
        
        self.t_name = QtGui.QLineEdit()
        self.t_name.setGeometry(QtCore.QRect(110, 40, 211, 20))
        self.t_passwd = QtGui.QLineEdit()

        #按钮
        self.b_ok = QtGui.QPushButton(u"登录")

        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)
    
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.l_name,1,0)
        mainLayout.addWidget(self.l_passwd,2,0)
        mainLayout.addWidget(self.t_name,1,1)
        mainLayout.addWidget(self.t_passwd,2,1)
        mainLayout.addWidget(self.b_ok,3,1)
        self.setLayout(mainLayout)

        self.b_ok.clicked.connect(self.login)

        self.trayIcon.show()
        
        self.setIcon(0)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.flash)
        self.flag = 0
        self.flash_status = 0

        self.setWindowTitle(u"登录")
        self.resize(400, 300)

    def setVisible(self, visible):
        super(Window, self).setVisible(visible)

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QtGui.QMessageBox.information(self, "Systray",
                    "The program will keep running in the system tray. To "
                    "terminate the program, choose <b>Quit</b> in the "
                    "context menu of the system tray entry.")
            self.hide()
            event.ignore()

    def setIcon(self, index):
        icon_path = os.getcwd();
        #icon = QtGui.QIcon(os.path.join(icon_path+'/images/logo1_64.png'))
        #icon = QtGui.QIcon(':/images/bad.svg')
        if 0 == index:
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/1.png'))
        elif 1 == index:
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/2.png'))
        elif 2 == index:
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/3.png'))
        self.trayIcon.setIcon(icon)
        '''
        icon_path = os.getcwd();
        print icon_path
        #icon = QtGui.QIcon(os.path.join(icon_path+'/images/logo1_64.png'))
        icon = QtGui.QIcon(':/images/bad.svg')
        
        if 0 == index:
            #icon = QtGui.QIcon(':/images/bad.svg')
            icon = QtGui.QIcon(':/logo1_64.png')
        elif 1 == index:
            icon = QtGui.QIcon(':/images/heart.svg')
        elif 2 == index:
            icon = QtGui.QIcon(':/images/trash.svg')
        
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        '''

    def iconActivated(self, reason):
        #import webbrowser
        #webbrowser.open('http://www.baidu.com', new=0, autoraise=True)
        '''
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            self.iconComboBox.setCurrentIndex(
                    (self.iconComboBox.currentIndex() + 1)
                    % self.iconComboBox.count())
        elif reason == QtGui.QSystemTrayIcon.MiddleClick:
            self.showMessage()
        '''

    def showMessage(self):
        icon = QtGui.QSystemTrayIcon.MessageIcon(
                self.typeComboBox.itemData(self.typeComboBox.currentIndex()))
        self.trayIcon.showMessage(self.titleEdit.text(),
                self.bodyEdit.toPlainText(), icon,
                self.durationSpinBox.value() * 1000)

    def messageClicked(self):
        QtGui.QMessageBox.information(None, "Systray",
                "Sorry, I already gave what help I could.\nMaybe you should "
                "try asking a human?")

    def createIconGroupBox(self):
        iconLayout = QtGui.QHBoxLayout()
        iconLayout.addStretch()

    def createActions(self):
        self.quitAction = QtGui.QAction(u"退出", self,
                triggered=QtGui.qApp.quit)

    def createTrayIcon(self):
         self.trayIconMenu = QtGui.QMenu(self)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)
         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setContextMenu(self.trayIconMenu)
         
    def login(self):
        import lib
        import urllib
        import sys
        #登录逻辑处理模块
        method  = 'Admin.login'
        name    = unicode(self.t_name.text().toUtf8(),'utf8','ignore').encode('utf8')
        passwd  = unicode(self.t_passwd.text().toUtf8(),'utf8','ignore').encode('utf8')
        content = {'admin_name':urllib.quote(name.encode('utf-8')),'passwd':passwd}
        result = lib.lib_post(method, content)
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            self.setIcon(1)
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"成功登录", icon,
                    15 * 1000)
            self.hide()
            self.name = name
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_message = on_message        
            #client.connect_async("192.168.1.131", 1883, 60)
            client.connect("192.168.1.131", 1883, 60)
            #client.loop_start();
            #client.loop_forever();
            self.run = True
            while True:
                client.loop()
                self.flash()
        else:
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"成功失败", icon,
                    15 * 1000)
            
    def my_time(self):
        #self.thread = QtCore.QThread();
        #self.thread.start()
        #定义定时器
        
        
        
        print 'my timer'
        
        self.timer.start(0)
        '''
        while self.control_msg:
            i = 0
            self.trayIcon.setIcon(QtGui.QIcon())
            while i<500:
                i = i + 1
            self.setIcon(1)
            i = 0
            while i<500:
                i = i + 1
        '''
        self.flag = 0
        
    #定时闪烁
    def flash(self):
        icon_path = os.getcwd();
        icon = QtGui.QIcon(os.path.join(icon_path+'/images/1.png'))
        if self.flash_status == 1:
            if 0 == self.flag:
                self.flag = 1
                self.trayIcon.setIcon(QtGui.QIcon())
                #print 1
            else:
                self.flag = 0
                self.trayIcon.setIcon(icon)
                #print 0

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    print window.name
    client.subscribe("bug/"+window.name)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    window.control_msg = str(msg.payload)
    if str(1) == str(msg.payload):
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        window.trayIcon.showMessage(u"提示",
                    u"新消息", icon,
                    15 * 1000)
        #window.setIcon(2)
        #window.my_time()
        window.flash_status = 1
    else:
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        window.trayIcon.showMessage(u"提示",
                    u"新消息", icon,
                    15 * 1000)
        window.setIcon(2)
        #window.my_time()
        window.flash_status = 0
    

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    window = Window()
    window.show()
    sys.exit(app.exec_())
