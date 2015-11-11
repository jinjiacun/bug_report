# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

try:
    import diagramscene_rc3
except ImportError:
    import diagramscene_rc2

from PyQt4 import QtGui
from jimLib.ui.App import MainWindow
from jimLib.ui.Login import login
from jimLib.lib.business import business
import paho.mqtt.client as mqtt

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class CMqtt():
    topic = ''
    def __init__(self,topic):
        CMqtt.topic = topic
        self.my_client = mqtt.Client()
        self.my_client.on_connect = self.on_connect
        self.my_client.on_message = self.on_message
        self.my_client.connect("192.168.1.131", 1883, 60)
        self.my_client.loop_start()
        pass

    def on_connect(self,client, userdata,flag, rc):
        client.subscribe(CMqtt.topic)

    def on_message(self,client, userdata, msg):
        #调用消息提示
        mainWindow.touch_sig(str(msg.payload))

    # pass

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    #登录界面
    loginWindow = login()
    loginWindow.setupUi(loginWindow)
    is_login_ok = False
    my_business = business()
    global user_name
    while not is_login_ok:
        if loginWindow.exec_():
            #print "user_name:%s\n"%loginWindow.user_name
            #print "passwd:%s\n"%loginWindow.passwd
            #检查用户名和密码是否正确
            (message,status,admin_id) = my_business.login(loginWindow.user_name, loginWindow.passwd)
            user_name = str(loginWindow.user_name)
            if status:
                #发送成功消息
                mainWindow.set_message(u'提示',message)
                mainWindow.set_tray(1)
                is_login_ok = True
                #开启mqtt推送
                my_mqtt = CMqtt("bug/"+user_name)
                mainWindow.my_time()
                #查询我的bug
                (status,is_success,message) = my_business.get_my_bug(admin_id)
                #500,,参数错误 | 200,0,严重错误 | 200,1,一般错误 | 200,-1,没有错误 | 其他查询失败
                if 500 == status:#500,,参数错误
                    pass
                elif 200 == status and 0 == is_success:#200,0,严重错误
                    pass
                elif 200 == status and 1 == is_success:#200,1,一般错误
                    pass
                elif 200 == status and -1 == is_success:#200,-1,没有错误
                    pass
                else:
                    pass
            else:
                #发送错误消息
                mainWindow.set_message(u'错误',message)
                pass
    #主界面
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.showMaximized()

    sys.exit(app.exec_())
