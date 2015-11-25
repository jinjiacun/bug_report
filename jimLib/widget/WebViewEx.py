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
UE.getEditor('editor').execCommand('insertHtml','%s');
"""
#UE.getEditor('editor').setContent('%s');
insertImage = """
UE.getEditor('editor').execCommand('insertImage',{
        src: '%s',
        width: 300,
        height: 400,
        border: 2,
        hspace: 5,
        vspace: 2,
        alt: 'UEditor-logo',
        title: 'clipboard'
    });
"""

class WebViewEx(QtWebKit.QWebView):
    def __init__(self, parent=None,value=None):
        super(WebViewEx, self).__init__(parent)

        self.page().mainFrame().addToJavaScriptWindowObject("myWindow", self)
        if value:
            self.value = value
        QtCore.QObject.connect(self.page().mainFrame(),QtCore.SIGNAL('loadFinished(bool)'),self.do_do)
        self.page().mainFrame().javaScriptWindowObjectCleared.connect(self.register_service)
        self.loadFinished.connect(self.on_loadFinished)
        self.load(QtCore.QUrl('http://192.168.1.131/bug/Ueditor/'))

        self.is_first = True
        self.message = ''
        self.index = 0
        self.ctl = True

    @QtCore.pyqtSlot()
    def register_service(self):
        self.page().mainFrame().addToJavaScriptWindowObject("myWindow", self)

    @QtCore.pyqtSlot(str)
    def showMessage(self, message):
        self.message = message
        print "Message from website:", message
        self.ctl = False


    @QtCore.pyqtSlot()
    def on_loadFinished(self):
        self.index += 1
        print self.index
        if self.ctl:
            self.page().mainFrame().evaluateJavaScript(setJsValue%self.value)
        '''
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
        '''


        self.page().mainFrame().evaluateJavaScript(getJsValue)

    @QtCore.pyqtSlot()
    def do_do(self):
        print 'load finish'
        if self.value:
            self.page().mainFrame().evaluateJavaScript(setJsValue%self.value)
            print 'set value'
            print self.value

    def insertHTML(self,content):
        print insertImage%content
        self.page().mainFrame().evaluateJavaScript(insertImage%content)
        pass

    @QtCore.pyqtSlot(result="int")
    def setValue(self):
        return self.value

    def text(self):
        self.page().mainFrame().evaluateJavaScript(getJsValue)
        return self.message

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myWindow')

    main = WebViewEx(None,u'中国')
    main.show()

    sys.exit(app.exec_())
