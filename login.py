# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\jim\jim_project\bug_report\untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from PyQt4 import QtCore, QtGui

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

class Ui_login(object):
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
        self.b_ok.clicked.connect(self.b_ok_clicked)
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
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        login.setWindowTitle(_translate("login", "登录", None))
        self.l_name.setText(_translate("login", "用户名:", None))
        self.label_2.setText(_translate("login", "密码:", None))
        self.b_ok.setText(_translate("login", "登录", None))
        self.b_cancel.setText(_translate("login", "取消", None))
        
    def b_ok_clicked(self):
        import lib
        import urllib
        import sys
        method  = 'Admin.login'
        name    = unicode(self.t_name.text().toUtf8(),'utf8','ignore').encode('utf8')
        passwd  = unicode(self.t_password.text().toUtf8(),'utf8','ignore').encode('utf8')
        content = {'admin_name':urllib.quote(name.encode('utf-8')),'passwd':passwd}
        result = lib.lib_post(method, content)
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            sys.exit()
        else:
            QtGui.QMessageBox.information(None, u"错误",
                u"用户名或密码错误")       
            return
        
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = Ui_login()
    mainWindow.show()
    sys.exit(app.exec_())