# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

'''
一个listwidget和一个按钮
列表中包含删除项目
'''
class ListButton(QtGui.QWidget):
    def __init__ (self, parent = None):
        super(ListButton, self).__init__(parent)
        self.setWindowTitle("weather")
        self.resize(1000, 200)
        girdLayout = QtGui.QGridLayout()
        girdLayout.setMargin(0)
        #按钮
        button1 = QtGui.QPushButton('+')
        button1.setFixedWidth(20)
        girdLayout.addWidget ( button1 , 0, 1)
        #列表
        list = QtGui.QListView()
        girdLayout.addWidget(list,0,0)
        self.setLayout( girdLayout)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = ListButton()
    window.show()
    sys.exit(app.exec_())

