#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
import paho.mqtt.client as mqtt
import threading
import os

try:
    import systray_rc3
except ImportError:
    import systray_rc2

class MyThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(int)
 
    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)
 
    def setup(self, name):
        self.name = name
 
    def run(self):
        #time.sleep(random.random()*5)  # random sleep to imitate working
        self.trigger.emit(window.result)
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message        
        client.connect("192.168.1.131", 1883, 60)
        client.loop_forever()
        


class Window(QtGui.QDialog):
    def __init__(self):
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
        self.t_passwd.setEchoMode(QtGui.QLineEdit.Password)

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
        i = 1
        while i<10:
            if 0 == i % 2:
                self.trayIcon.setIcon(icon)
            else:
                self.trayIcon.setIcon(QtGui.QIcon())
            i = i+1
        '''
        #self.setWindowIcon(icon)
    def my_time(self):
        #定义定时器
        self.timer.timeout.connect(self.flash)
        self.timer.start(500)
        self.flag = 0

    #定时闪烁
    def flash(self):
        icon_path = os.getcwd();
        icon = QtGui.QIcon(os.path.join(icon_path+'/images/1.png'))
        if 0 == self.flag:
            self.flag = 1
            self.trayIcon.setIcon(QtGui.QIcon())
            #print 1
        else:
            self.flag = 0
            self.trayIcon.setIcon(icon)
            #print 0
    
    
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
            import jim_io
            f = jim_io.Db_Connector("./config.ini")
            f.set_value("userconf", "user", name)
            f.set_value("userconf", "password", passwd)
            self.my_mosquitto()
            #mainWindow.show()
           
        else:
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"成功失败", icon,
                    15 * 1000)
            
    def my_mosquitto(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message        
        client.connect("192.168.1.131", 1883, 60)
        #client.loop_forever()
        client.loop_read()
        
    def start_thread(self, ):
        thread = MyThread(self)    # create a thread
        thread.trigger.connect(self.control_time)  # connect to it's signal
        thread.setup(self.name)            # just setting up a parameter
        thread.start()             # start the thread
        pass
    
    def control_time(self,result):
        print 'control_time',result
        if str(1) == str(result):
            self.my_time()
        else:
            self.timer.stop()
        pass

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    print window.name
    client.subscribe("bug/"+window.name)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    window.result = msg.payload
   
    if str(1) == str(msg.payload):
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        window.trayIcon.showMessage(u"提示",
                    u"新消息", icon,
                    1000)
        window.setIcon(2)
        #开启时钟
        #window.my_time()
        print 'open time'
    elif str(0) == str(msg.payload):
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        window.setIcon(1)
        #关闭时钟
        #window.timer.stop()
        print 'close time'
    

def my_mosquitto():
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message        
        client.connect("192.168.1.131", 1883, 60)
        client.loop_forever()

if __name__ == '__main__':
    import sys
    #改变程序执行目录路径
    ddir = sys.path[0]
    if os.path.isfile(ddir):
        ddir,filen = os.path.split(ddir)
    os.chdir(ddir)
    
    app = QtGui.QApplication(sys.argv)
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    window = Window()
    #判定是否设置了用户名和密码
    import jim_io
    icon_path = os.path.abspath('.');
    xml_file = os.path.join(icon_path+"/config.ini")
    f = jim_io.Db_Connector(xml_file)
    user = f.get_value("userconf","user")
    print user
    if '' == user:
        window.show()
    else:
        window.name = user
        #window.start_thread()
        window.my_mosquitto()
    
    #window.my_mosquitto();    
    '''
    import diagramscene
    mainWindow = diagramscene.MainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    if '' != user:
        mainWindow.show()
    '''
    #window.my_time()
    #加载程序到开机启动
    '''
    import AutoTask
    current_exe = os.getcwd()+"/systray.exe"
    my_task = AutoTask.AutoTask(current_exe)
    if my_task.work():
        print 'success'
    else:
        print 'fail'
    '''
    sys.exit(app.exec_())
