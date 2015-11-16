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
from jimLib.widget.WebViewEx import WebViewEx
from jimLib.lib.business import business
from jimLib.lib.util import Dict
from jimLib.lib.util import get_cur_admin_id

class Edit(QDialog):
    title = ''
    title_index = 0
    module = ''
    module_index = 0
    status = False
    message = ''
    def __init__(self, parent=None,title_index=1,module_index=1,id=0):
        super(Edit, self).__init__(parent)
        mainLayout = QVBoxLayout()
        self.parent = parent
        self.id = id

        Edit.title  = Dict.title_list[title_index]
        Edit.module = Dict.module_list[module_index]
        Edit.title_index  = title_index
        Edit.module_index = module_index


        self.AddToolBar()
        self.formGroupBox = QGroupBox(u"表单:")
        if 'Project' == Edit.module:
            self.EditProjectForm()
        elif 'Bug' == Edit.module:
            self.EditBugForm()
        elif 'Admin' == Edit.module:
            self.EditAdminForm()
        elif 'Role' == Edit.module:
            self.EditRoleForm()
        elif 'Part' == Edit.module:
            self.EditPartForm()
        elif 'Resume' == Edit.module:
            self.EditResumeForm()
        elif 'Positionhr' == Edit.module:
            self.EditPositionhrForm()


        mainLayout.addWidget(self.horizontalGroupBox)
        mainLayout.addWidget(self.formGroupBox)
        self.setLayout(mainLayout)
        self.setFixedWidth(1000)
        self.setFixedHeight(800)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(Edit.title)

    #编辑项目
    def EditProjectForm(self,id):
        layout = QFormLayout()
        my_business = business()
        (status,my_info) = my_business.get_project_one_by_id(self.id)
        if not status:
            content = u'查询错误'
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'警告',content)
            self.close()
        #项目添加
        layout = QFormLayout()
        layout.addRow(QLabel(u"<font color='red'>*</font>项目名称:"), QLineEdit())
        self.number = QLabel(my_info['number'])
        layout.addRow(QLabel(u" 编号:"), self.number)
        layout.addRow(QLabel(u"项目描述:"), QTextEdit())

        layout.addRow(QLabel(u"成员:"), TableComButton())
        layout.addRow(QLabel(u"模块:"), TableTextButton())
        self.formGroupBox.setLayout(layout)

    #编辑bug
    def EditBugForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Edit.module_index)
        #bug添加
        layout = QFormLayout()
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.level = QComboBox()
        layout.addRow(QLabel(u"<font color='red'>*</font>优先级:"), self.level)
        self.status = QComboBox()
        layout.addRow(QLabel(u"<font color='red'>*</font>状态:"), self.status)
        self.project_id = QComboBox()
        layout.addRow(QLabel(u"<font color='red'>*</font>所属项目:"), self.project_id)
        self.project_mod_id = QComboBox()
        layout.addRow(QLabel(u"<font color='red'>*</font>所属模块:"), self.project_mod_id)
        self.get_member = QComboBox()
        layout.addRow(QLabel(u"<font color='red'>*</font>受理人:"), self.get_member)
        self.title = QTextEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>问题描述:"), self.title)
        self.description = WebViewEx()
        layout.addRow(QLabel(u"操作过程:"), self.description)
        self.formGroupBox.setLayout(layout)
        self.formGroupBox.resize(600,700)
        self.resize(600, 700)

    #编辑用户
    def EditAdminForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Edit.module_index)
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

    #编辑角色
    def EditRoleForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Edit.module_index)
        #角色添加
        layout = QFormLayout()
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.name = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>角色名称:"), self.name)
        #查询资源
        (status,content) = my_business.get_resource()
        source_name_list = {}
        if status:
             rows = int(content['record_count'])
             for i in range(0,rows-1):
                 key = content['list'][i]['source_name']
                 id  = content['list'][i]['id']
                 source_name_list[key] = id
        self.resource = MulCheckedBox(self,source_name_list)
        layout.addRow(QLabel(u"<font color='red'>*</font>权限:"), self.resource)
        self.formGroupBox.setLayout(layout)

    #编辑部门
    def EditPartForm(self):
        layout = QFormLayout()
        my_business = business()
        (status,my_info) = my_business.get_part_one_by_id(self.id)
        if not status:
            content = u'查询错误'
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'警告',content)
            self.close()
        #部门添加
        layout = QFormLayout()
        self.number = QLabel(my_info['number'])
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.name = QLineEdit()
        self.name.setText(my_info['name'])
        layout.addRow(QLabel(u"<font color='red'>*</font>部门名称:"), self.name)
        self.formGroupBox.setLayout(layout)

    #编辑简历
    def EditResumeForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Edit.module_index)
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

    #编辑招聘岗位
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
        if 'Project' == Edit.module:
            self.SaveProejct()
        elif 'Bug' == Edit.module:
            self.SaveBug()
        elif 'Admin' == Edit.module:
            self.SaveAdmin()
        elif 'Role' == Edit.module:
            self.SaveRole()
        elif 'Part' == Edit.module:
            self.SavePart()
        elif 'Resume' == Edit.module:
            self.SaveResume()
        elif 'Positionhr' == Edit.module:
            self.SavePositionhr()
        pass

    #保存项目
    def SaveProejct(self):
        pass

    #保存bug
    def SaveBug(self):
        time.sleep(3)
        print self.description.text()

        pass

    #保存用户
    def SaveAdmin(self):
        data={'number':0,'admin_name':'','passwd':'','re_passwd':'','name':'','status':0,'part':0,'role':0}
        my_business = business()

        #组装数据
        data['number']     = urllib.quote(str(self.number.text()))
        data['admin_name'] = urllib.quote(str(self.user_name.text()))
        data['passwd']    = urllib.quote(str(self.passwd.text()))
        data['re_passwd'] = urllib.quote(str(self.re_passwd.text()))
        data['name']       = urllib.quote(str(self.name.text()))
        data['status']     = 0
        data['part']       = 1
        data['role']       = 2
        #data['position']   = 1

        if data['passwd'] != data['re_passwd']:
            content = u'两次密码不一致'
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'警告',content)
            return False
        data.pop('re_passwd')
        (status,content) = my_business.add_admin(data)

        print 'content:%s'%content
        if status:
            Edit.message = content
            Edit.status = True
            self.parent.set_message(u'提示',content)
            return True
        else:
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'错误',content)

    #保存角色
    def SaveRole(self):
        data={'number':'','name':'','resource':0}
        my_business = business()

        #组装数据
        data['number']   = urllib.quote(str(self.number.text()))
        data['name']     = urllib.quote(str(self.name.text()))
        data['resource'] = urllib.quote(str(self.resource.text()))

        (status,content) = my_business.add_role(data)
        print 'content:%s'%content
        if status:
            Edit.message = content
            Edit.status = True
            self.parent.set_message(u'提示',content)
            return True
        else:
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'错误',content)

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
            Edit.message = content
            Edit.status = True
            self.parent.set_message(u'提示',content)
            return True
        else:
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'错误',content)
        pass

    #保存简历
    def SaveResume(self):
        data={'number':'','candidates':'','telephone':'','position_id':0,'part_id':0,
            'accessories':0,'remartk':'','create':0}
        my_business = business()

        #组装数据
        data['number']      = urllib.quote(str(self.number.text()))
        data['candidates']  = urllib.quote(str(self.candidates.text()))
        data['telephone']   = urllib.quote(str(self.telephone.text()))
        data['position_id'] = 1
        data['part_id']     = 1
        data['accessories'] = 0
        #附件
        (status,content) = my_business.file_upload(str(self.accessories.filename))
        if status:
            data['accessories'] = int(content['content']['id'])
        else:
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'错误',content)
            return False

        data['remartk']      = urllib.quote(str(self.remark.toPlainText()))
        data['create']      = get_cur_admin_id()

        (status,content) = my_business.add_resume(data)
        print 'content:%s'%content
        if status:
            Edit.message = content
            Edit.status = True
            self.parent.set_message(u'提示',content)
            return True
        else:
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'错误',content)

    #保存简历岗位
    def SavePositionhr(self):
        data={'part_id':0,'name':'','description':'','create':0}
        my_business = business()

        #组装数据
        data['part_id'] = 2
        data['description'] = urllib.quote(str(self.description.toPlainText()))
        data['name']   = urllib.quote(str(self.name.text()))
        data['create'] = get_cur_admin_id()

        (status,content) = my_business.add_positionhr(data)
        print 'content:%s'%content
        if status:
            Edit.message = content
            Edit.status = True
            self.parent.set_message(u'提示',content)
            return True
        else:
            Edit.message = content
            Edit.status = False
            self.parent.set_message(u'错误',content)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myWindow = Edit()
    #myWindow.show()
    myWindow.showMaximized()
    sys.exit(app.exec_())