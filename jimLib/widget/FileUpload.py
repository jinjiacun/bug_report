# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from jimLib.lib.business import business

'''
一个image、一个按钮
'''
class FileUpload(QtGui.QWidget):
    def __init__ (self, parent = None):
        super(FileUpload, self).__init__(parent)
        self.setWindowTitle("weather")
        self.data = {}#总数据
        self.display_data = []#可以显示的数据
        self.cur_index = -1
        self.resize(1000, 200)
        girdLayout = QtGui.QGridLayout()
        girdLayout.setMargin(0)
        #Lable
        self.lab = QtGui.QLabel()
        girdLayout.addWidget(self.lab,0,0)
        self.setLayout(girdLayout)
        #按钮
        btnOpenDialog = QtGui.QPushButton(u'上传')
        btnOpenDialog.clicked.connect(self.openFileDialog)
        btnOpenDialog.setFixedWidth(30)
        girdLayout.addWidget( btnOpenDialog , 0, 1)

    def openFileDialog(self):
        pass

    def text(self):
        re_data = []
        for key in self.display_data:
            re_data.append(self.data[key])
        return re_data

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = FileUpload()
    window.show()
    sys.exit(app.exec_())



