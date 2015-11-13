# -*- coding: utf-8 -*-
#!/usr/bin/env python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from jimLib.widget.WebViewEx import WebViewEx
import webbrowser

class WebPage(QWebPage):
    def __init__(self):
        super(WebPage, self).__init__()

    def acceptNavigationRequest(self, frame, request, type):
        if(type == QWebPage.NavigationTypeLinkClicked):
            if(frame == self.mainFrame()):
                self.view().load(request.url())
            else:
                webbrowser.open(request.url().toString())
                return False
        return QWebPage.acceptNavigationRequest(self, frame, request, type)

class MyWebView(QWidget):

    def __init__(self, parent = None):
        super(MyWebView, self).__init__(parent)
        self.createLayout()
        self.createConnection()
        self.webView.page().mainFrame().addToJavaScriptWindowObject("myWindow", self)
        self.message = ''

    def search(self):
        address = str('http://192.168.1.131/bug/Ueditor/')
        if address:
            if address.find('://') == -1:
                address = 'http://' + address
            url = QUrl(address)
            self.webView.load(url)
            self.webView.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
            self.webView.page().linkClicked.connect(self.linkClicked)
            self.webView.show()
    def linkClicked(self, url):
        self.load(url)

    def createLayout(self):
        self.setWindowTitle("keakon's browser")
        self.webView = WebViewEx()
        self.webSettings = self.webView.settings()
        self.webSettings.setAttribute(QWebSettings.PluginsEnabled,True)
        self.webSettings.setAttribute(QWebSettings.JavascriptEnabled,True)
        self.webView.setPage(WebPage())
        self.btnTest = QPushButton(u'测试')
        self.connect(self.btnTest,SIGNAL("clicked()"),self.test)

        layout = QVBoxLayout()
        layout.addWidget(self.btnTest)
        layout.addWidget(self.webView)

        self.setLayout(layout)

    def createConnection(self):
        #调用查询
        self.search()

    def test(self):
        print 'result:',self.webView.message
        #print self.webView.page().mainFrame().toHtml()
        pass

    def text(self):
        return self.webView.message

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = MyWebView ()
    browser.show()
    sys.exit(app.exec_())
