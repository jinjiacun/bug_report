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
from jimLib.widget.FileUpload import FileUpload
from jimLib.lib.business import business
from jimLib.lib.util import Dict
from jimLib.lib.util import get_cur_admin_id

class Add(QDialog):
    title = ''
    title_index = 0
    module = ''
    module_index = 0
    status = False
    message = ''
    def __init__(self, parent=None,title_index=0,module_index=0):
        super(Add, self).__init__(parent)
        mainLayout = QVBoxLayout()
        self.parent = parent

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
        (status,result) = my_business.get_dict()
        if result.has_key('part'):
            for (key,item) in result['part'].items():
                self.part.addItems([item])
        layout.addRow(QLabel(u"<font color='red'>*</font>部门:"), self.part)
        self.role = QComboBox()
        if result.has_key('role'):
            for (key,item) in result['role'].items():
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
        my_business = business()
        number = my_business.get_number(Add.module_index)
        #部门添加
        layout = QFormLayout()
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.name = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>部门名称:"), self.name)
        self.formGroupBox.setLayout(layout)

    #添加简历
    def AddResumeForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Add.module_index)
        #简历添加
        layout = QFormLayout()
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.candidates = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>应聘人:"), self.candidates)
        self.telephone = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>联系方式:"), self.telephone)
        self.position_id = QComboBox()
        (status,content) = my_business.get_dict()
        if status:
            if content.has_key('positionhr'):
                for (key,value) in content['positionhr'].items():
                    self.position_id.addItems([value])
        layout.addRow(QLabel(u"<font color='red'>*</font>应聘岗位:"), self.position_id)
        self.part_id = QComboBox()
        if status:
            for (key,value) in content['part'].items():
                self.part_id.addItems([value])
        layout.addRow(QLabel(u"<font color='red'>*</font>应聘部门:"), self.part_id)
        self.accessories = FileUpload()
        layout.addRow(QLabel(u"<font color='red'>*</font>简历附件:"), self.accessories)
        self.remark = QTextEdit()
        layout.addRow(QLabel(u"备注:"), self.remark)
        self.formGroupBox.setLayout(layout)

    #添加招聘岗位
    def AddPositionhrForm(self):
        layout = QFormLayout()

        #招聘岗位添加
        layout = QFormLayout()
        self.part_id = QComboBox()
        my_business = business()
        (status,content) = my_business.get_dict()
        if status:
            for (key,item) in content['part'].items():
                self.part_id.addItems([item])
        layout.addRow(QLabel(u"<font color='red'>*</font>部门:"), self.part_id)

        self.name = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>岗位:"),self.name)
        self.description = QTextEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>要求:"), self.description)
        self.formGroupBox.setLayout(layout)

    def AddToolBar(self):
        self.horizontalGroupBox = QGroupBox(u"操作")
        self.horizontalGroupBox.setFixedHeight(50)
        layout = QHBoxLayout()

        btn_save = QPushButton(u'保存')
        self.connect(btn_save,SIGNAL("clicked()"),self,SLOT("accept()"))
        btn_save.setFixedWidth(50)
        btn_save.clicked.connect(self.SaveForm)
        layout.addWidget(btn_save)

        btn_cancel = QPushButton(u'取消')
        btn_cancel.setFixedWidth(50)
        btn_cancel.clicked.connect(self.Cancel)
        layout.addWidget(btn_cancel)

        btn_close = QPushButton(u'关闭')
        btn_close.setFixedWidth(50)
        btn_close.clicked.connect(self.Close)
        layout.addWidget(btn_close)

        self.horizontalGroupBox.setLayout(layout)
        pass

    def Cancel(self):
        pass

    def Close(self,event):
        #self.emit(SIGNAL('closeEmitApp()'))
        self.close()
        pass
    #-----------------保存-----------------------------
    def SaveForm(self):
        if 'Project' == Add.module:
            self.SaveProejct()
        elif 'Bug' == Add.module:
            self.SaveBug()
        elif 'Admin' == Add.module:
            self.SaveAdmin()
        elif 'Role' == Add.module:
            self.SaveRole()
        elif 'Part' == Add.module:
            self.SavePart()
        elif 'Resume' == Add.module:
            self.SaveResume()
        elif 'Positionhr' == Add.module:
            self.SavePositionhr()
        pass

    #保存项目
    def SaveProejct(self):
        pass

    #保存bug
    def SaveBug(self):
        pass

    #保存用户
    def SaveAdmin(self):
        pass

    #保存角色
    def SaveRole(self):
        pass

    #保存部门
    def SavePart(self):
        data={'number':'','name':'','create':0}
        my_business = business()

        #组装数据
        data['number'] = urllib.quote(str(self.number.text()))
        data['name']   = urllib.quote(str(self.name.text()))
        data['create'] = get_cur_admin_id()

        (status,content) = my_business.add_part(data)
        print 'content:%s'%content
        if status:
            Add.message = content
            Add.status = True
            self.parent.set_message(u'提示',content)
            return True
        else:
            Add.message = content
            Add.status = False
            self.parent.set_message(u'错误',content)
        pass

    #保存简历
    def SaveResume(self):
        pass

    #保存简历岗位
    def SavePositionhr(self):
        pass

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myWindow = Add()
    #myWindow.show()
    myWindow.showMaximized()
    sys.exit(app.exec_())


