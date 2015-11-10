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
import jimLib.widget.ListButton
import jimLib.widget.ListTextButton


class Add(QDialog):
    title = ''
    module = ''#Project,Bug
    def __init__(self, parent=None,title='',module=''):
        super(Add, self).__init__(parent)
        mainLayout = QVBoxLayout()

        self.AddToolBar()
        self.formGroupBox = QGroupBox(u"表单:")
        if 'Project' == module:
            self.AddProjectForm()
        elif 'Bug' == module:
            self.AddBugForm()
        elif 'User' == module:
            self.AddUserForm()
        elif 'Role' == module:
            self.AddRoleForm()

        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)
        self.setFixedWidth(500)
        self.setFixedHeight(400)
        self.setWindowFlags(Qt.Window)
        Add.title = title
        Add.module = module
        self.setWindowTitle(Add.title)

    #添加项目
    def AddProjectForm(self):
        layout = QFormLayout()

        #项目添加
        layout = QFormLayout()
        layout.addRow(QLabel(u"<font color='red'>*</font>项目名称:"), QLineEdit())
        layout.addRow(QLabel(u" 编号:"), QLabel())
        layout.addRow(QLabel(u"项目描述:"), QTextEdit())
        layout.addRow(QLabel(u"成员:"), jimLib.widget.ListButton.ListButton())
        layout.addRow(QLabel(u"模块:"), jimLib.widget.ListTextButton.ListTextButton())
        self.formGroupBox.setLayout(layout)

    #添加bug
    def AddBugForm(self):
        pass

    #添加用户
    def AddUserForm(self):
        pass

    #添加角色
    def AddRoleForm(self):
        pass

    #添加部门
    def AddPartForm(self):
        pass

    #添加简历
    def AddResumeForm(self):
        pass

    #添加招聘岗位
    def AddPositionhrForm(self):
        pass

    def AddToolBar(self):
        self.horizontalGroupBox = QGroupBox(u"操作")
        self.horizontalGroupBox.setFixedHeight(50)
        layout = QHBoxLayout()

        button = QPushButton(u'保存')
        button.setFixedWidth(50)
        layout.addWidget(button)

        button = QPushButton(u'取消')
        button.setFixedWidth(50)
        layout.addWidget(button)

        button = QPushButton(u'返回')
        button.setFixedWidth(50)
        layout.addWidget(button)

        self.horizontalGroupBox.setLayout(layout)
        pass


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myWindow = Add()
    #myWindow.show()
    myWindow.showMaximized()
    sys.exit(app.exec_())


