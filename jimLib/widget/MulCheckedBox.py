# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

'''
多个复选框
列表中包含删除项目
'''
class MulCheckedBox(QtGui.QWidget):
    def __init__ (self, parent = None,resource=None):
        super(MulCheckedBox, self).__init__(parent)
        self.data = []
        self.cur_row = -1
        if resource:
            self.data = resource
        self.setWindowTitle("weather")
        self.resize(200, 200)
        girdLayout = QtGui.QGridLayout()
        girdLayout.setMargin(0)
        rows = 0
        cols = 0
        print self.data
        #复选框
        for item in self.data:
            newCheckBox = QtGui.QCheckBox(item)
            newCheckBox.setFixedWidth(100)
            girdLayout.addWidget(newCheckBox,rows,cols)
            cols += 1
            if cols>3:
                cols = 0
                rows += 1

        self.setLayout( girdLayout)

    def text(self):
        return self.data

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MulCheckedBox()
    window.show()
    sys.exit(app.exec_())