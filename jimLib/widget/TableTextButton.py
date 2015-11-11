# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from jimLib.widget.PushButtonEx import PushButtonEx

'''
一个listwidget、单行文本编辑器和一个按钮
列表中包含删除项目
'''
class TableTextButton(QtGui.QWidget):
    def __init__ (self, parent = None):
        super(TableTextButton, self).__init__(parent)
        self.data = []
        self.cur_row = -1
        self.setWindowTitle("weather")
        self.resize(200, 200)
        girdLayout = QtGui.QGridLayout()
        girdLayout.setMargin(0)
        #列表
        self.list = QtGui.QTableWidget(1,1)
        self.list.setFixedWidth(150)
        self.list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.list.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.list.setHorizontalHeaderLabels([u'名称'])
        girdLayout.addWidget(self.list,0,0)
        self.setLayout( girdLayout)
        #单行文本
        self.editText = QtGui.QLineEdit()
        self.editText.setFixedWidth(150)
        girdLayout.addWidget(self.editText,1,0)
        #按钮
        btnAdd = QtGui.QPushButton('+')
        btnAdd.clicked.connect(self.addText)
        btnAdd.setFixedWidth(20)
        girdLayout.addWidget ( btnAdd , 1, 1)
        btnDel = QtGui.QPushButton('-')
        btnDel.clicked.connect(self.delText)
        btnDel.setFixedWidth(20)
        girdLayout.addWidget(btnDel,1,2)

    def addText(self):
        self.data.append(str(self.editText.text()))
        #去重排序
        my_data = sorted(set(self.data),key=self.data.index)
        TableTextButton.data = my_data

        #设置行数
        self.list.setRowCount(len(self.data))
        row = 0
        for item_text in TableTextButton.data:
            newItem = QtGui.QTableWidgetItem(item_text)
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list.setItem(row, 0, newItem)

            row += 1

        self.editText.setText('')

    def delText(self):
        item = self.list.item(self.list.currentRow(),0)
        #移除数据
        self.list.removeRow(self.list.currentRow())
        pass

    def text(self):
        return self.data

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = TableTextButton()
    window.show()
    sys.exit(app.exec_())


