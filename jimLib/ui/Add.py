#!/usr/bin/env python
#coding=utf-8
import sip
#sip.setapi('QVariant', 2)

from PyQt4.QtGui  import *  #目测table的类应该是在qt.gui里面的
from PyQt4.QtCore import *
import math
import time
import urllib
import jimLib.widget.ListButton
import jimLib.widget.TableTextButton


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
        layout.addRow(QLabel(u"模块:"), jimLib.widget.TableTextButton.ListTextButton())
        self.formGroupBox.setLayout(layout)

    #添加bug
    def AddBugForm(self):
        layout = QFormLayout()

        #bug添加
        layout = QFormLayout()
        layout.addRow(QLabel(u" 编号:"), QLabel())
        layout.addRow(QLabel(u"<font color='red'>*</font>优先级:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>状态:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>所属项目:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>所属模块:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>受理人:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>问题描述:"), QTextEdit())
        layout.addRow(QLabel(u"操作过程:"), QTextEdit())

    #添加用户
    def AddUserForm(self):
        layout = QFormLayout()

        #用户添加
        layout = QFormLayout()
        layout.addRow(QLabel(u" 编号:"), QLabel())
        layout.addRow(QLabel(u"<font color='red'>*</font>用户帐号:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>密码:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>确认密码:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>姓名:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>状态:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>部门:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>角色:"), QTextEdit())
        self.formGroupBox.setLayout(layout)

    #添加角色
    def AddRoleForm(self):
        layout = QFormLayout()

        #角色添加
        layout = QFormLayout()
        layout.addRow(QLabel(u" 编号:"), QLabel())
        layout.addRow(QLabel(u"<font color='red'>*</font>角色名称:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>权限:"), QTextEdit())
        self.formGroupBox.setLayout(layout)

    #添加部门
    def AddPartForm(self):
        layout = QFormLayout()

        #部门添加
        layout = QFormLayout()
        layout.addRow(QLabel(u" 编号:"), QLabel())
        layout.addRow(QLabel(u"<font color='red'>*</font>部门名称:"), QTextEdit())
        self.formGroupBox.setLayout(layout)

    #添加简历
    def AddResumeForm(self):
        layout = QFormLayout()

        #简历添加
        layout = QFormLayout()
        layout.addRow(QLabel(u" 编号:"), QLabel())
        layout.addRow(QLabel(u"<font color='red'>*</font>应聘人:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>联系方式:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>应聘岗位:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>应聘部门:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>简历附件:"), QTextEdit())
        layout.addRow(QLabel(u"备注:"), QTextEdit())
        self.formGroupBox.setLayout(layout)

    #添加招聘岗位
    def AddPositionhrForm(self):
        layout = QFormLayout()

        #招聘岗位添加
        layout = QFormLayout()
        layout.addRow(QLabel(u"<font color='red'>*</font>部门:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>岗位:"), QTextEdit())
        layout.addRow(QLabel(u"<font color='red'>*</font>要求:"), QTextEdit())
        self.formGroupBox.setLayout(layout)

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


