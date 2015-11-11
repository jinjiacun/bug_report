# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from jimLib.lib.business import business

'''
一个table、combox选择器和一个按钮
列表中包含删除项目
'''
class TableComButton(QtGui.QWidget):
    def __init__ (self, parent = None):
        super(TableComButton, self).__init__(parent)
        self.setWindowTitle("weather")
        self.data = {}#总数据
        self.display_data = []#可以显示的数据
        self.cur_index = -1
        my_business = business()
        (status,content) = my_business.get_dict()
        if status:
            for (key,value) in content['admin'].items():
                tmp_value = str(value)
                self.data[tmp_value] = int(str(key))
        self.resize(1000, 200)
        girdLayout = QtGui.QGridLayout()
        girdLayout.setMargin(0)
        #表格
        self.table = QtGui.QTableWidget(1,1)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        #verticalHeader
        girdLayout.addWidget(self.table,0,0)
        self.setLayout( girdLayout)
        #下拉列表
        self.combo = QtGui.QComboBox()
        for key in self.data:
            self.combo.addItems([key])
        girdLayout.addWidget(self.combo,1,0)
        #按钮
        btnAdd = QtGui.QPushButton('+')
        btnAdd.clicked.connect(self.addText)
        btnAdd.setFixedWidth(20)
        girdLayout.addWidget ( btnAdd , 1, 1)
        btnDel = QtGui.QPushButton('-')
        btnDel.clicked.connect(self.delText)
        btnDel.setFixedWidth(20)
        girdLayout.addWidget ( btnDel , 1, 2)

    def addText(self):
        self.display_data.append(str(self.combo.currentText()))
        #移除字典及其下拉列表
        self.data.pop(str(self.combo.currentText()))
        self.combo.removeItem(self.combo.currentIndex())
        self.table.setRowCount(len(self.display_data))
        row = 0
        print self.display_data
        for item in self.display_data:
            newItem = QtGui.QTableWidgetItem(item)
            self.table.setItem(row, 0, newItem)
            row += 1

    def delText(self):
        item = self.table.item(self.table.currentRow(),0)
        print 'item:%s'%item.text()
        print self.display_data
        self.display_data.remove(item.text())
        self.combo.addItems([str(item.text())])
        self.table.removeRow(self.table.currentRow())
        pass

    def text(self):
        re_data = []
        for key in self.display_data:
            re_data.append(self.data[key])
        return re_data

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = TableComButton()
    window.show()
    sys.exit(app.exec_())



