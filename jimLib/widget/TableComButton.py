# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

'''
一个table、combox选择器和一个按钮
列表中包含删除项目
'''
class TableComButton(QtGui.QWidget):
    def __init__ (self, parent = None):
        super(TableComButton, self).__init__(parent)
        self.setWindowTitle("weather")
        self.resize(1000, 200)
        girdLayout = QtGui.QGridLayout()
        girdLayout.setMargin(0)
        #表格
        self.table = QtGui.QTableWidget(1,2)
        girdLayout.addWidget(self.table,1,0)
        self.setLayout( girdLayout)
        #按钮
        btnAdd = QtGui.QPushButton('+')
        btnAdd.clicked.connect(self.addText)
        btnAdd.setFixedWidth(20)
        girdLayout.addWidget ( btnAdd , 0, 0)

    def addText(self):
        old_rows = self.table.rowCount()
        self.table.insertRow(0)

        pass

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = TableComButton()
    window.show()
    sys.exit(app.exec_())



