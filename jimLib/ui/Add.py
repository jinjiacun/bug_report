#!/usr/bin/env python
#coding=utf-8
import sip
#sip.setapi('QVariant', 2)

from PyQt4.QtGui  import *  #目测table的类应该是在qt.gui里面的
from PyQt4.QtCore import *
import math
import time
import urllib
from jimLib.widget.ListButton import ListButton
from jimLib.widget.TableTextButton import TableTextButton
from jimLib.widget.TableComButton import TableComButton
from jimLib.widget.MulCheckedBox import MulCheckedBox
from jimLib.lib.business import business
from jimLib.lib.util import Dict


class Add(QDialog):
    title = ''
    title_index = 0
    module = ''
    module_index = 0
    def __init__(self, parent=None,title_index=3,module_index=3):
        super(Add, self).__init__(parent)
        mainLayout = QVBoxLayout()

        Add.title  = Dict.title_list[title_index]
        Add.module = Dict.module_list[module_index]
        Add.title_index  = title_index
        Add.module_index = module_index

        self.AddToolBar()
        self.formGroupBox = QGroupBox(u"表单:")
        if 'Project' == Add.module:
            self.AddProjectForm()
        elif 'Bug' == Add.module:
            self.AddBugForm()
        elif 'Admin' == Add.module:
            self.AddAdminForm()
        elif 'Role' == Add.module:
            self.AddRoleForm()
        elif 'Part' == Add.module:
            self.AddPartForm()
        elif 'Resume' == Add.module:
            self.AddResumeForm()
        elif 'Positionhr' == Add.module:
            self.AddPositionhrForm()


        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)
        self.setFixedWidth(500)
        self.setFixedHeight(400)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(Add.title)

    #添加项目
    def AddProjectForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Add.module_index)
        #项目添加
        layout = QFormLayout()
        layout.addRow(QLabel(u"<font color='red'>*</font>项目名称:"), QLineEdit())
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), QLabel(number))
        layout.addRow(QLabel(u"项目描述:"), QTextEdit())

        layout.addRow(QLabel(u"成员:"), TableComButton())
        layout.addRow(QLabel(u"模块:"), TableTextButton())
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
        self.formGroupBox.setLayout(layout)

    #添加用户
    def AddAdminForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Add.module_index)
        #用户添加
        layout = QFormLayout()
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.user_name = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>用户帐号:"), self.user_name)
        self.passwd = QLineEdit()
        self.passwd.setEchoMode(QLineEdit.Password)
        layout.addRow(QLabel(u"<font color='red'>*</font>密码:"), self.passwd)
        self.re_passwd = QLineEdit()
        self.re_passwd.setEchoMode(QLineEdit.Password)
        layout.addRow(QLabel(u"<font color='red'>*</font>确认密码:"), self.re_passwd)
        self.name = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>姓名:"), self.name)
        self.status = QComboBox()
        self.status.addItems([u'正常'])
        self.status.addItems([u'禁用'])
        layout.addRow(QLabel(u"<font color='red'>*</font>状态:"), self.status)
        self.part = QComboBox()
        #查询部门
        my_business = business()
        (status,resule) = my_business.get_dict()
        for (key,item) in resule['part'].items():
            self.part.addItems([item])
        layout.addRow(QLabel(u"<font color='red'>*</font>部门:"), self.part)
        self.role = QComboBox()
        for (key,item) in resule['role'].items():
            self.role.addItems([item])
        layout.addRow(QLabel(u"<font color='red'>*</font>角色:"), self.role)
        self.formGroupBox.setLayout(layout)

    #添加角色
    def AddRoleForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Add.module_index)
        #角色添加
        layout = QFormLayout()
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.name = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>角色名称:"), self.name)
        #查询资源
        (status,content) = my_business.get_resource_name()
        source_name_list = []
        if status:
            source_name_list = content
        self.resource = MulCheckedBox(self,source_name_list)
        layout.addRow(QLabel(u"<font color='red'>*</font>权限:"), self.resource)
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


