# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from PyQt4 import QtGui
from PyQt4 import QtCore

'''
一个listwidget、单行文本编辑器和一个按钮
列表中包含删除项目
'''
class TableTextButton(QtGui.QWidget):
    def __init__ (self, parent = None,display_data=None):
        super(TableTextButton, self).__init__(parent)
        self.data = []
        if display_data:
            self.data = display_data
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
        self.list.verticalHeader().setVisible(False)
        self.list.horizontalHeader().setVisible(False)
        self.list.setHorizontalHeaderLabels([u'名称'])
        girdLayout.addWidget(self.list,0,0)
        row = 0
        #预加载数据
        if display_data:
            self.bind()

        self.setLayout( girdLayout)
        #单行文本
        self.editText = QtGui.QLineEdit()
        self.editText.setFixedWidth(150)
        girdLayout.addWidget(self.editText,1,0)
        #self.connect(self.editText,QtCore.SIGNAL("returnPressed()"),self.editChange)
        self.editText.textChanged.connect(self.editChange)
        #按钮
        self.btnAdd = QtGui.QPushButton('+')
        self.btnAdd.clicked.connect(self.addText)
        self.btnAdd.setFixedWidth(20)
        self.btnAdd.setEnabled(False)
        girdLayout.addWidget ( self.btnAdd , 1, 1)
        self.btnDel = QtGui.QPushButton('-')
        self.btnDel.clicked.connect(self.delText)
        self.btnDel.setFixedWidth(20)
        self.btnDel.setEnabled(False)
        if display_data:
            self.btnDel.setEnabled(True)
        girdLayout.addWidget(self.btnDel,1,2)

        #测试
        '''
        self.btnTest = QtGui.QPushButton(u'测试')
        self.btnTest.clicked.connect(self.test)
        girdLayout.addWidget(self.btnTest,1,3)
        '''

    def editChange(self):
        if '' == self.editText.text():
            self.btnAdd.setEnabled(False)
        else:
            self.btnAdd.setEnabled(True)
        if 0< self.list.rowCount():
            self.btnDel.setEnabled(True)
        else:
            self.btnDel.setEnabled(False)
        pass

    def addText(self):
        if '' == self.editText.text():
            return
        self.data.append(str(self.editText.text()))
        #去重排序
        my_data = sorted(set(self.data),key=self.data.index)
        self.data = my_data

        #设置行数
        self.list.setRowCount(len(self.data))
        row = 0
        for item_text in self.data:
            newItem = QtGui.QTableWidgetItem(unicode(item_text))
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list.setItem(row, 0, newItem)
            row += 1

        self.editText.setText('')
        if 0< self.list.rowCount():
            self.btnDel.setEnabled(True)
        else:
            self.btnDel.setEnabled(False)

    #绑定数据
    def bind(self):
        #去重排序
        my_data = sorted(set(self.data),key=self.data.index)
        self.data = my_data

        #设置行数
        self.list.setRowCount(len(self.data))
        row = 0
        for item_text in self.data:
            newItem = QtGui.QTableWidgetItem(unicode(item_text))
            newItem.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            self.list.setItem(row, 0, newItem)
            row += 1


    def delText(self):
        if -1 == self.list.currentRow():
            item = self.list.item(0,0)
        else:
            item = self.list.item(self.list.currentRow(),0)
        #tmp_text = item.text()
        self.data.remove(str(item.text()))
        #移除数据
        if -1 == self.list.currentRow():
            self.list.removeRow(0)
        else:
            self.list.removeRow(self.list.currentRow())
        if 0< self.list.rowCount():
            self.btnDel.setEnabled(True)
        else:
            self.btnDel.setEnabled(False)

    def text(self):
        return self.data

    #修改更新
    def toText(self):
        pass

    def test(self):
        print self.text()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    #显示数据
    data = []
    data.append('模块一')
    data.append('模块二')
    data.append('模块三')
    window = TableTextButton(None,data)
    #window = TableTextButton()
    window.show()
    sys.exit(app.exec_())


