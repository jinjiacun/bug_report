#!/usr/bin/env python
#coding=utf-8
import sip
#sip.setapi('QVariant', 2)

from PyQt4.QtGui  import *  #目测table的类应该是在qt.gui里面的
from PyQt4.QtCore import *
import math
import time
import lib
import urllib


class JimAdd(QDialog):

    def __init__(self, parent=None):
        super(JimAdd, self).__init__(parent)
        mainLayout = QVBoxLayout()

        self.AddToolBar()
        self.AddForm()

        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)
        self.setFixedWidth(500)
        self.setFixedHeight(400)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'项目添加')

    def AddForm(self):
        layout = QFormLayout()
        self.formGroupBox = QGroupBox(u"表单")
        layout = QFormLayout()
        layout.addRow(QLabel(u"<font color='red'>*</font>项目名称:"), QLineEdit())
        layout.addRow(QLabel(u"    编号:"), QLabel())
        layout.addRow(QLabel(u"项目描述:"), QTextEdit())
        layout.addRow(QLabel(u"    成员:"), QSpinBox())
        layout.addRow(QLabel(u"    模块:"), QLineEdit())
        self.formGroupBox.setLayout(layout)


    def AddToolBar(self):
        self.horizontalGroupBox = QGroupBox(u"操作")
        self.horizontalGroupBox.setFixedHeight(50)
        layout = QHBoxLayout()

        button = QPushButton(u'保存')
        layout.addWidget(button)

        button = QPushButton(u'取消')
        layout.addWidget(button)

        button = QPushButton(u'返回')
        layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)
        pass


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myWindow = JimAdd()
    #myWindow.show()
    myWindow.showMaximized()
    sys.exit(app.exec_())

