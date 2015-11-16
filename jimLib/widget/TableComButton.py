# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from jimLib.lib.business import business

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
一个table、combox选择器和一个按钮
列表中包含删除项目
'''
class TableComButton(QtGui.QWidget):
    def __init__ (self, parent = None,data=None,display_data=None):
        super(TableComButton, self).__init__(parent)
        self.setWindowTitle(u"下拉列表")
        self.data = {}#总数据
        if data:
            self.data = data
        self.display_data = []#可以显示的数据
        self.cur_index = -1
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

        if display_data:
            self.display_data = display_data
            self.bind()

        #下拉列表
        self.combo = QtGui.QComboBox()
        print 'self.data'
        print self.data
        for key in self.data:
            if key not in self.display_data:
                self.combo.addItems([key])
        girdLayout.addWidget(self.combo,1,0)
        #按钮
        self.btnAdd = QtGui.QPushButton('+')
        self.btnAdd.clicked.connect(self.addText)
        self.btnAdd.setFixedWidth(20)
        girdLayout.addWidget ( self.btnAdd , 1, 1)
        self.btnDel = QtGui.QPushButton('-')
        self.btnDel.clicked.connect(self.delText)
        self.btnDel.setFixedWidth(20)
        girdLayout.addWidget ( self.btnDel , 1, 2)



        #测试按钮
        '''
        btnTest = QtGui.QPushButton(u'测试')
        btnTest.clicked.connect(self.test)
        girdLayout.addWidget(btnTest,1,3)
        '''

    #绑定数据
    def bind(self):
        #移除下拉表中已经在列表中显示的项目
        #todo
        #显示预先加入的数据
        #移除字典及其下拉列表
        self.table.setRowCount(len(self.display_data))
        row = 0
        print self.display_data
        for item in self.display_data:
            newItem = QtGui.QTableWidgetItem(item)
            self.table.setItem(row, 0, newItem)
            row += 1
        pass

    def addText(self):
        self.display_data.append(str(self.combo.currentText()))
        #移除字典及其下拉列表
#        self.data.pop(str(self.combo.currentText()))
        self.combo.removeItem(self.combo.currentIndex())
        if 0 == self.combo.count():
            self.btnAdd.setEnabled(False)
            self.btnDel.setEnabled(True)
        elif 0 == self.table.rowCount():
            self.btnAdd.setEnabled(True)
            self.btnDel.setEnabled(False)
        else:
            self.btnAdd.setEnabled(True)
            self.btnDel.setEnabled(True)
        self.table.setRowCount(len(self.display_data))
        row = 0
        print self.display_data
        for item in self.display_data:
            newItem = QtGui.QTableWidgetItem(item)
            self.table.setItem(row, 0, newItem)
            row += 1

    def delText(self):
        if -1 == self.table.currentRow():
            item = self.table.item(0,0)
        else:
            item = self.table.item(self.table.currentRow(),0)
        self.display_data.remove(str(item.text()))
        self.combo.addItems([str(item.text())])
        if -1 == self.table.currentRow():
            self.table.removeRow(0)
        else:
            self.table.removeRow(self.table.currentRow())
        if 0 == self.table.rowCount():
            self.btnDel.setEnabled(False)
            self.btnAdd.setEnabled(True)
        elif 0 == self.combo.count():
            self.btnAdd.setEnabled(False)
            self.btnDel.setEnabled(True)
        else:
            self.btnDel.setEnabled(True)
            self.btnAdd.setEnabled(True)
        pass

    def text(self):
        re_data = []
        for key in self.display_data:
            re_data.append(self.data[key])
        return re_data

    def test(self):
        print self.text()
        pass

if __name__ == '__main__':
    app = QtGui.QApplication([])
    data = {}
    my_business = business()
    (status,content) = my_business.get_dict()
    if status:
         for (key,value) in content['admin'].items():
             tmp_value = str(value)
             data[tmp_value] = int(str(key))
    display_data = []
    display_data.append('admin')
    window = TableComButton(None,data,display_data)
    window.show()
    sys.exit(app.exec_())



