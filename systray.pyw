#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------
'''
版本说明:此版本解救mosquitto多线程冲突问题
'''
#----------------------------

import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
from multiprocessing import Process, Pipe, Queue
import paho.mqtt.client as mqtt
import os
import multiprocessing
import time

try:
    import systray_rc3
except ImportError:
    import systray_rc2

#---------------------------------处理网络推送---------------------------
class C_mqtt(multiprocessing.Process):
    def __init__(self, q):
        multiprocessing.Process.__init__(self)
        self.q = q


    def on_connect(self,client, userdata, flags, rc):
        import jim_io
        icon_path = os.path.abspath('.')
        xml_file = os.path.join(icon_path+"/config.ini")
        f = jim_io.Db_Connector(xml_file)
        prefix = f.get_value("serverconf", "topic_prefix")
        user   = f.get_value("userconf", "user")
        #client.subscribe(prefix+'/'+user)
        client.subscribe('bug/#')
        pass

    def on_message(self,client, userdata, msg):
        #print msg.payload
        self.q.put(msg.payload)
        print msg.payload
        window.setIcon(4)
        pass

    def run(self):
        c = mqtt.Client()
        import jim_io
        icon_path = os.path.abspath('.')
        xml_file = os.path.join(icon_path+"/config.ini")
        f = jim_io.Db_Connector(xml_file)
        host    = f.get_value("serverconf", "host")
        port    = f.get_value("serverconf", "port")
        timeout = f.get_value("serverconf", "timeout")
        #c.connect(host , port, timeout)
        c.connect('192.168.1.131' , '1883', 60)
        c.on_connect = self.on_connect
        c.on_message = self.on_message
        while True:
            c.loop()
        #c.loop_forever()

#---------------------------处理业务逻辑--------------------------------
class bill(multiprocessing.Process):
    def __init__(self):
        pass

    def run(self):
        pass


class Window(QtGui.QDialog):

    emit_python_list = QtCore.pyqtSignal(object)

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

        self.flag = 0
        self.flash_status = 0
        self.q = Queue()
        self.emit_python_list.connect(self.slot2)


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
        icon_path = os.getcwd()
        #icon = QtGui.QIcon(os.path.join(icon_path+'/images/logo1_64.png'))
        #icon = QtGui.QIcon(':/images/bad.svg')
        if 0 == index:#unload
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/un_load.png'))
        elif 1 == index:#load
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/normal.png'))
        elif 2 == index:#err
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/error.png'))
        elif 3 == index:#yellow warn
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/warn_yellow.png'))
        elif 4 == index:#red warn
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/warn_red.png'))
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
        icon = QtGui.QIcon(os.path.join(icon_path+'/images/warn_red.png'))
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
        self.aboutAction = QtGui.QAction(u"关于",self,
                triggered=self.showAbout)

    def createTrayIcon(self):
         self.trayIconMenu = QtGui.QMenu(self)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)
         self.trayIconMenu.addAction(self.aboutAction)
         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setContextMenu(self.trayIconMenu)
         
    #--------------------------action---------------------------
    
    def showAbout(self):
        print 'show about\n'
        pass

    def slot1(self,msg):
        self.emit_python_list.emit(msg)
    
    def slot2(self, msg):    
        print msg
        if str(1) == str(msg):#高级警告
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            window.trayIcon.showMessage(u"提示",
                        u"严重bug", icon,
                        1000)
            window.setIcon(4)
            #定时
            window.timer.start()
        elif str(0) == str(msg):#取消高级警告
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            window.setIcon(1)
            window.timer.stop()
        elif str(2) == str(msg):#一般警告
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            window.trayIcon.showMessage(u"提示",
                        u"有bug", icon,
                        1000)
            window.setIcon(3)
            window.timer.stop()
    
    #--------------------------action---------------------------
         
    def login(self):
        import sys
        #登录逻辑处理模块
        name    = unicode(self.t_name.text().toUtf8(),'utf8','ignore').encode('utf8')
        passwd  = unicode(self.t_passwd.text().toUtf8(),'utf8','ignore').encode('utf8')        
        self.my_login(name, passwd)
        
            
    def my_login(self, name, passwd):
        import lib
        import urllib
        method  = 'Admin.login'
        content = {'admin_name':urllib.quote(name.encode('utf-8')),'passwd':passwd}
        user_id = 0
        result = lib.lib_post(method, content)
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            user_id = result['content']['id']
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
            f.set_value("userconf", "user_id", user_id)
            #检查是否有需要提醒的
            self.my_bug(urllib.quote(user_id.encode('utf-8')))
            #开启网络推送
            #my_mosquitto()
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)

            #msg = self.q.get()
            '''
            
            if msg:
                result = self.q.get()
                if str(1) == str(result):#高级警告
                    self.trayIcon.showMessage(u"提示",u"严重bug", icon,1000)
                    self.setIcon(4)
                    self.flash_status = 1
                elif str(0) == str(result):#取消高级警告
                    self.setIcon(1)
                    self.flash_status = 0
                elif str(2) == str(result):#一般警告
                    self.trayIcon.showMessage(u"提示",u"有bug", icon,1000)
                    self.setIcon(3)
                    self.flash_status = 0
            '''
            pass
        else:
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"登录失败", icon,
                    15 * 1000)
            self.setIcon(2)
            self.show()
    
    def my_bug(self, admin_id):
        import lib
        import urllib
        method  = 'Bug.get_self_bug'
        content = {'admin_id':admin_id}
        result = lib.lib_post(method, content)
        if 500 == result:
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"查询参数错误", icon,
                    15 * 1000)
            self.setIcon(2)
            return

        if 200 == result['status_code'] and 0 == result['content']['is_success']:#严重bug
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"严重bug", icon,
                    15 * 1000)
            self.flash_status = 1
            self.setIcon(4)
            pass
        elif 200 == result['status_code'] and 1 == result['content']['is_success']:#一般bug
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"有bug", icon,
                    15 * 1000)
            self.flash_status = 0
            self.setIcon(3)
            pass
        elif 200 == result['status_code'] and -1 == result['content']['is_success']:#没有待解救的bug
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"没有待解决的bug", icon,
                    15 * 1000)
            self.flash_status = 0
            self.setIcon(1)
            pass
        else:
            icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
            self.trayIcon.showMessage(u"提示",
                    u"查询bug失败", icon,
                    15 * 1000)
            self.setIcon(2)
            pass
        pass
    
        
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
   
    if str(1) == str(msg.payload):#高级警告
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        window.trayIcon.showMessage(u"提示",
                    u"严重bug", icon,
                    1000)
        window.setIcon(4)
        window.flash_status = 1
    elif str(0) == str(msg.payload):#取消高级警告
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        window.setIcon(1)
        window.flash_status = 0
    elif str(2) == str(msg.payload):#一般警告
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        window.trayIcon.showMessage(u"提示",
                    u"有bug", icon,
                    1000)
        window.setIcon(3)
        window.flash_status = 0
def my_mosquitto():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message   
    try:     
        client.connect("192.168.1.131", 1883, 60)
    except:
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        window.trayIcon.showMessage(u"提示",
                    u"推送网络错误", icon,
                    1000)
        sys.exit()
        
    while True:
        #self.client.loop_forever()
        client.loop()
        window.flash()


def my_on_connect(client, userdata, flags, rc):
    client.subscribe('bug/#')
    pass

def my_on_message(client, userdata, msg):
    print msg.payload
    window.slot1(str(msg.payload))
    pass

c = mqtt.Client()
c.connect("192.168.1.131", 1883, 60)
c.on_connect = my_on_connect
c.on_message = my_on_message

if __name__ == '__main__':
    import sys
    #改变程序执行目录路径
    ddir = sys.path[0]
    if os.path.isfile(ddir):
        ddir,filen = os.path.split(ddir)
    os.chdir(ddir)
    
    app = QtGui.QApplication(sys.argv)
    '''
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    '''
    window = Window()
    #加载程序到开机启动    
    import AutoTask
    current_exe = os.getcwd()+"/systray.exe"
    my_task = AutoTask.AutoTask(current_exe)
    if my_task.work():
        print 'success'
    else:
        print 'fail'
    #判定是否设置了用户名和密码
    import jim_io
    icon_path = os.path.abspath('.')
    xml_file = os.path.join(icon_path+"/config.ini")
    f = jim_io.Db_Connector(xml_file)
    user = f.get_value("userconf","user")
    password = f.get_value("userconf","password")
    window.show()
    window.my_time()
    window.timer.stop()
    '''
    my_mqtt = C_mqtt(window.q)
    my_mqtt.start()
    '''
    c.loop_start()

    #my_mqtt.join()
    '''
    if '' == user:
        window.show()
    else:
        window.my_login(user, password)
        window.setIcon(1)
    '''
    '''
    import diagramscene
    mainWindow = diagramscene.MainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    if '' != user:
        mainWindow.show()
    '''
    #window.my_time()
    
    
    sys.exit(app.exec_())
