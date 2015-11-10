# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

'''
一个listwidget、单行文本编辑器和一个按钮
列表中包含删除项目
'''
class ListTextButton(QtGui.QWidget):
    def __init__ (self, parent = None):
        super(ListTextButton, self).__init__(parent)
        self.setWindowTitle("weather")
        self.resize(1000, 200)
        girdLayout = QtGui.QGridLayout()
        girdLayout.setMargin(0)
        #列表
        self.list = QtGui.QTableWidget()
        girdLayout.addWidget(self.list,0,0)
        self.setLayout( girdLayout)
        #单行文本
        self.editText = QtGui.QLineEdit()
        girdLayout.addWidget(self.editText,1,0)
        #按钮
        btnAdd = QtGui.QPushButton('+')
        btnAdd.clicked.connect(self.addText)
        btnAdd.setFixedWidth(20)
        girdLayout.addWidget ( btnAdd , 1, 1)

    def addText(self):
        self.editText.text('')
        pass

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = ListTextButton()
    window.show()
    sys.exit(app.exec_())


