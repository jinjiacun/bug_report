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
myWindow.showMessage(UE.getEditor('editor').getContent());
"""
setJsValue = """
UE.getEditor('editor').setContent('123');
"""

class WebViewEx(QtWebKit.QWebView):
    def __init__(self, parent=None,value=None):
        super(WebViewEx, self).__init__(parent)

        self.page().mainFrame().addToJavaScriptWindowObject("myWindow", self)
        self.page().mainFrame().evaluateJavaScript(setJsValue)
        self.loadFinished.connect(self.on_loadFinished)
        self.load(QtCore.QUrl('http://192.168.1.131/bug/Ueditor/'))
        self.value = value

        self.message = ''

    @QtCore.pyqtSlot(str)
    def showMessage(self, message):
        self.message = message
        print "Message from website:", message

    @QtCore.pyqtSlot()
    def on_loadFinished(self):
        self.page().mainFrame().evaluateJavaScript(getJsValue)
    @QtCore.pyqtSlot(result="int")
    def setValue(self):
        return self.value

    def text(self):
        return self.message

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myWindow')

    main = WebViewEx(None,123)
    main.show()

    sys.exit(app.exec_())
