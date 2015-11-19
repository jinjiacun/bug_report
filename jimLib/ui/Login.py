# -*- coding: utf-8 -*-
import sip

from PyQt4 import QtCore, QtGui
import os
import sys
from jimLib.lib.business import business

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class login(QtGui.QDialog):

    def __init__(self,parent=None):
        super(login, self).__init__()
        self.parent = parent


    def setupUi(self, login):
        login.setObjectName(_fromUtf8("login"))
        login.resize(402, 222)
        self.l_name = QtGui.QLabel(login)
        self.l_name.setGeometry(QtCore.QRect(50, 40, 54, 12))
        self.l_name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_name.setObjectName(_fromUtf8("l_name"))
        self.label_2 = QtGui.QLabel(login)
        self.label_2.setGeometry(QtCore.QRect(50, 100, 54, 12))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.b_ok = QtGui.QPushButton(login)
        self.b_ok.setGeometry(QtCore.QRect(90, 170, 75, 23))
        self.b_ok.setObjectName(_fromUtf8("b_ok"))
        self.b_ok.clicked.connect(self.my_login)
        self.b_cancel = QtGui.QPushButton(login)
        self.b_cancel.setGeometry(QtCore.QRect(250, 170, 75, 23))
        self.b_cancel.setObjectName(_fromUtf8("b_cancel"))
        self.t_name = QtGui.QLineEdit(login)
        self.t_name.setGeometry(QtCore.QRect(110, 40, 211, 20))
        self.t_name.setObjectName(_fromUtf8("t_name"))
        self.t_password = QtGui.QLineEdit(login)
        self.t_password.setGeometry(QtCore.QRect(110, 93, 211, 20))
        self.t_password.setEchoMode(QtGui.QLineEdit.Password)
        self.t_password.setObjectName(_fromUtf8("t_password"))

        self.retranslateUi(login)
        #QtCore.QObject.connect(self.b_ok, QtCore.SIGNAL(_fromUtf8("clicked()")), login.accept)
        QtCore.QMetaObject.connectSlotsByName(login)
        self.user_name = ''
        self.passwd = ''

    def retranslateUi(self, login):
        login.setWindowTitle(_translate("login", "登录", None))
        self.l_name.setText(_translate("login", "用户名:", None))
        self.label_2.setText(_translate("login", "密码:", None))
        self.b_ok.setText(_translate("login", "登录", None))
        self.b_ok.clicked.connect(self.my_login)
        self.b_cancel.setText(_translate("login", "退出", None))
        self.b_cancel.clicked.connect(self.my_exit)

    def my_login(self):
        import sys
        #登录逻辑处理模块
        user_name    = self.t_name.text()
        passwd  = self.t_password.text()
        self.user_name = user_name
        self.passwd    = passwd
        my_business = business()
        (message,status,admin_id) = my_business.login(self.user_name, self.passwd)
        if status:
            #发送成功消息
            self.parent.set_message(u'提示',message)
            self.parent.set_tray(1)
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
            self.accept()
        else:
            #发送错误消息
            self.parent.set_message(u'错误',message)
            pass


    def my_exit(self):
        sys.exit()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = login()
    mainWindow.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())