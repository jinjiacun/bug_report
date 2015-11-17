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
UE.getEditor('editor').setContent('%s');
"""

class WebViewEx(QtWebKit.QWebView):
    def __init__(self, parent=None,value=None):
        super(WebViewEx, self).__init__(parent)

        self.page().mainFrame().addToJavaScriptWindowObject("myWindow", self)
        self.page().mainFrame().evaluateJavaScript(setJsValue)
        self.loadFinished.connect(self.on_loadFinished)
        self.load(QtCore.QUrl('http://192.168.1.131/bug/Ueditor/'))
        self.value = value
        self.is_first = True
        self.message = ''
        self.index = 0

    @QtCore.pyqtSlot(str)
    def showMessage(self, message):
        self.message = message
        print "Message from website:", message

    @QtCore.pyqtSlot()
    def on_loadFinished(self):
        if self.value:
            if self.is_first:
                print 'first'
                self.page().mainFrame().evaluateJavaScript(setJsValue%self.value)
                self.index += 1
                print 'index:%d'%self.index
                if self.index>4:
                    self.is_first = False
                    self.value = None
                #self.is_first = False
        self.page().mainFrame().evaluateJavaScript(getJsValue)

    def insertHTML(self,content):
        self.page().mainFrame().evaluateJavaScript(setJsValue%self.message+content)
        pass

    @QtCore.pyqtSlot(result="int")
    def setValue(self):
        return self.value

    def text(self):
        return self.message

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myWindow')

    main = WebViewEx(None,'abc')
    main.show()

    sys.exit(app.exec_())
