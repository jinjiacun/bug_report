# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'http.ui'
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

class Ui_HttpWidget(object):
    def setupUi(self, HttpWidget):
        HttpWidget.setObjectName(_fromUtf8("HttpWidget"))
        HttpWidget.resize(400, 300)
        self.webView = QtWebKit.QWebView(HttpWidget)
        self.webView.setGeometry(QtCore.QRect(60, 30, 300, 200))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.url = QtGui.QLineEdit(HttpWidget)
        self.url.setGeometry(QtCore.QRect(30, 240, 161, 31))
        self.url.setObjectName(_fromUtf8("url"))
        self.reload = QtGui.QPushButton(HttpWidget)
        self.reload.setGeometry(QtCore.QRect(260, 250, 75, 23))
        self.reload.setObjectName(_fromUtf8("reload"))

        self.retranslateUi(HttpWidget)
        QtCore.QMetaObject.connectSlotsByName(HttpWidget)

    def retranslateUi(self, HttpWidget):
        HttpWidget.setWindowTitle(_translate("HttpWidget", "Dialog", None))
        self.reload.setText(_translate("HttpWidget", "reload", None))

from PyQt4 import QtWebKit
