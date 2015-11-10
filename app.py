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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    #登录界面
    loginWindow = login()
    loginWindow.setupUi(loginWindow)
    is_login_ok = False
    my_business = business()
    while not is_login_ok:
        if loginWindow.exec_():
            #print "user_name:%s\n"%loginWindow.user_name
            #print "passwd:%s\n"%loginWindow.passwd
            #检查用户名和密码是否正确
            (message,status) = my_business.login(loginWindow.user_name, loginWindow.passwd)
            print status
            if status:
                #发送成功消息
                mainWindow.set_message(message)
                is_login_ok = True
                break
            else:
                #发送错误消息
                mainWindow.set_message(message)
                pass


    #主界面
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.showMaximized()

    sys.exit(app.exec_())
