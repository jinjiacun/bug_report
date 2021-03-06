#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui, QtWebKit

'''
getJsValue = """
w = document.getElementsByTagName('p')[0];
myWindow.showMessage(w.innerHTML);
"""
'''
getJsValue = """
myWindow.showMessage(123);
"""

class myWindow(QtWebKit.QWebView):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)

        self.page().mainFrame().addToJavaScriptWindowObject("myWindow", self)

        self.loadFinished.connect(self.on_loadFinished)

        self.load(QtCore.QUrl('http://192.168.1.131/bug/Ueditor/'))

    @QtCore.pyqtSlot(str)
    def showMessage(self, message):
        print "Message from website:", message

    @QtCore.pyqtSlot()
    def on_loadFinished(self):
        self.page().mainFrame().evaluateJavaScript(getJsValue)

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myWindow')

    main = myWindow()
    main.show()

    sys.exit(app.exec_())
