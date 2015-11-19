# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from jimLib.lib.business import business
from jimLib.lib.util import file_down
from jimLib.lib.util import file_extension
import tkFileDialog

'''
一个image、一个按钮
'''
class FileUpload(QtGui.QWidget):
    def __init__ (self, parent = None,filename=None):
        super(FileUpload, self).__init__(parent)
        self.parent = parent
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
        self.filename = ''
        self.filetype = ''
        if filename:
            self.filename = filename
            self.lab.setText("<a href='%s'>%s</a>"%(self.filename,self.filename))
            btnDownFile = QtGui.QPushButton(u'下载')
            btnDownFile.setFixedWidth(30)
            btnDownFile.clicked.connect(self.file_down)
            girdLayout.addWidget(btnDownFile,0,2)

    def openFileDialog(self):
        self.filename,filetype = QtGui.QFileDialog.getOpenFileName(self,
                                    u"选取文件",
                                    "C:/",
                                    "PDF Files (*.pdf *.PDF);;Doc Files (*.doc *.DOC);;Docx Files (*.docx *.DOCX);;Xls Files (*.xls *.XLS);;Xlax Files (*.xlsx *.XLSX);;Zip Files (*.zip *.ZIP);;Rar Files (*.rar *.RAR)")
        self.lab.setText(self.filename)
        pass

    def file_down(self):
        if '' != self.lab.text():
            #打开保存对话框
            save_path = ''
            f_ext = file_extension(self.filename)
            f_ext = f_ext.replace('.','')
            save_path = QtGui.QFileDialog.getSaveFileName(self,
                                    "文件保存",
                                   u"./未命名.%s"%f_ext,
                                    "All Files (%s.*)"%f_ext)
            print save_path
            file_down(self.filename,save_path)
            self.parent.parent.set_message(u'提示',u'成功下载')
            return True
        pass

    def text(self):
        return self.filename

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = FileUpload()
    window.show()
    sys.exit(app.exec_())



