#!/usr/bin/env python
#coding=utf-8
import sip
#sip.setapi('QVariant', 2)

from PyQt4.QtGui  import *  #目测table的类应该是在qt.gui里面的
from PyQt4.QtCore import *
import math
import time
import urllib
import base64
import json
from jimLib.widget.ListButton import ListButton
from jimLib.widget.TableTextButton import TableTextButton
from jimLib.widget.TableComButton import TableComButton
from jimLib.widget.MulCheckedBox import MulCheckedBox
from jimLib.widget.FileUpload import FileUpload
from jimLib.widget.WebViewEx import WebViewEx
from jimLib.lib.business import business
from jimLib.lib.util import Dict
from jimLib.lib.util import get_cur_admin_id
from jimLib.lib.util import upload_clipboard_pic
from jimLib.lib.util import save_clipboard_image

class Add(QDialog):
    title = ''
    title_index = 0
    module = ''
    module_index = 0
    status = False
    message = ''
    def __init__(self, parent=None,title_index=1,module_index=1):
        super(Add, self).__init__(parent)
        mainLayout = QVBoxLayout()
        self.parent = parent

        Add.title  = Dict.title_list[title_index]
        Add.module = Dict.module_list[module_index]
        Add.title_index  = title_index
        Add.module_index = module_index
        self.remote_message = {}


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
        self.setFixedWidth(1000)
        self.setFixedHeight(800)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(Add.title)

    #添加项目
    def AddProjectForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Add.module_index)
        #项目添加
        layout = QFormLayout()
        self.name = QLineEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>项目名称:"), self.name)
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.description = QTextEdit()
        layout.addRow(QLabel(u"项目描述:"), self.description)

        data ={}
        (status,content) = my_business.get_dict()
        if status:
            for (key,value) in content['admin'].items():
                tmp_value = str(value)
                data[tmp_value] = int(str(key))
        self.project_mem = TableComButton(self,data)
        layout.addRow(QLabel(u"成员:"), self.project_mem)
        self.project_mod = TableTextButton()
        layout.addRow(QLabel(u"模块:"), self.project_mod)
        self.formGroupBox.setLayout(layout)

    #添加bug
    def AddBugForm(self):
        layout = QFormLayout()
        my_business = business()
        number = my_business.get_number(Add.module_index)
        #bug添加
        layout = QFormLayout()
        self.number = QLabel(number)
        layout.addRow(QLabel(u" 编号:"), self.number)
        self.level = QComboBox()
        self.level.addItem(u'超高',QVariant(1))
        self.level.addItem(u'高',QVariant(2))
        self.level.addItem(u'一般',QVariant(3))
        layout.addRow(QLabel(u"<font color='red'>*</font>优先级:"), self.level)
        self.status = QComboBox()
        self.status.addItem(u'待解救',QVariant(1))
        self.status.addItem(u'已解救',QVariant(2))
        self.status.addItem(u'已关闭',QVariant(3))
        layout.addRow(QLabel(u"<font color='red'>*</font>状态:"), self.status)
        self.project_id = QComboBox()
        (status,my_dict) = my_business.get_dict()
        self.project_id.addItem(u'请选择项目',QVariant(0))
        self.my_dict = my_dict
        if my_dict.has_key('project'):
            for (key,value) in my_dict['project'].items():
                self.project_id.addItem(value,QVariant(key))
        layout.addRow(QLabel(u"<font color='red'>*</font>所属项目:"), self.project_id)
        self.connect(self.project_id, SIGNAL('activated(int)'), self.onActivatedModule)
        self.project_mod_id = QComboBox()
        self.project_mod_id.addItem(u'请选择项目模块',QVariant(0))
        layout.addRow(QLabel(u"<font color='red'>*</font>所属模块:"), self.project_mod_id)
        self.get_member = QComboBox()
        self.get_member.addItem(u'请选择受理人',QVariant(0))
        layout.addRow(QLabel(u"<font color='red'>*</font>受理人:"), self.get_member)
        self.title = QTextEdit()
        layout.addRow(QLabel(u"<font color='red'>*</font>问题描述:"), self.title)
        self.description = WebViewEx()
        layout.addRow(QLabel(u"操作过程:"), self.description)
        self.formGroupBox.setLayout(layout)
        self.formGroupBox.resize(600,700)
        self.resize(600, 700)

    def myClip(self):
        #print QApplication.clipboard().text()
        print 'my clip test'
        #self.description.insertHTML('123')
        save_clipboard_image()
        message = upload_clipboard_pic()
        self.remote_message = list(message)
        if self.remote_message[0]:
            #self.description.insertHTML('<img src="%s" alt="%s"/>'%(self.remote_message[1]['url'],self.remote_message[1]['title']))
            self.description.insertHTML(self.remote_message[1]['url'])
        pass

    #级联关系(项目-模块)
    def onActivatedModule(self, cuindex):
        #print 'cuindex:%d'%cuindex
        project_id = cuindex
        if 0 >= project_id:
            return
        #查询项目下面的模块
        my_business = business()
        (status,content) = my_business.get_project_mod_by_project_id(project_id)
        self.project_mod_id.clear()
        self.project_mod_id.addItem(u'请选择项目模块',QVariant(0))
        if status:
            for (key,item) in content.items():
                self.project_mod_id.addItem(unicode(key),QVariant(item))

        #成员
        (status,content) = my_business.get_project_mem_by_project_id(project_id)
        self.get_member.clear()
        self.get_member.addItem(u'请选择受理人',QVariant(0))
        if status:
            for item in content:
                self.get_member.addItem(unicode(self.my_dict['admin'][str(item)]),QVariant(item))

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
        #self.connect(btn_save,SIGNAL("clicked()"),self,SLOT("accept()"))
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

        btn_paste = QPushButton(u'粘贴')
        btn_paste.setShortcut('Ctrl+V')
        btn_paste.clicked.connect(self.myClip)
        #btn_paste.setVisible(False)
        layout.addWidget(btn_paste)


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
        data={'number':'','name':'','description':'','create':0}
        mem_data={'project_id':0,'admin_id':[]}
        mod_data={'project_id':0,'name':[]}
        my_business = business()

        #组装数据
        data['number']        = urllib.quote(str(self.number.text()))
        data['name']          = urllib.quote(str(self.name.text()))
        data['description']  = urllib.quote(str(self.description.toPlainText()))
        data['create']        = get_cur_admin_id()

        #项目成员
        mem_data['admin_id'] = self.project_mem.text()

        #项目模块
        tmp_mod_data_name_list = self.project_mod.text()
        mod_data_name_list = []
        for item in tmp_mod_data_name_list:
            mod_data_name_list.append(urllib.quote(item))
        mod_data['name'] = mod_data_name_list


        (status,content) = my_business.add_proejct(data,mem_data,mod_data)
        if status:
            Add.message = content
            Add.status = True
            self.parent.set_message(u'提示',content)
            self.accept()
        else:
            Add.message = content
            Add.status = False
            self.parent.set_message(u'错误',content)

    #保存bug
    def SaveBug(self):
        data={'number':'','title':'','level':0,'status':0,'project_id':0,'project_mod_id':0,
            'get_member':0,'description':'','put_member':0}
        my_business = business()

        #组装数据
        data['number']        = urllib.quote(str(self.number.text()))
        data['title']         = urllib.quote(str(self.title))
        data['level']         = urllib.quote(str(self.level.itemData(self.level.currentIndex()).toPyObject()))

        data['status']        = urllib.quote(str(self.status.itemData(self.status.currentIndex()).toPyObject()))
        data['project_id']   = urllib.quote(str(self.project_id.itemData(self.project_id.currentIndex()).toPyObject()))
        data['project_mod_id'] = urllib.quote(str(self.project_mod_id.itemData(self.project_mod_id.currentIndex()).toPyObject()))
        data['get_member']   = urllib.quote(str(self.get_member.itemData(self.get_member.currentIndex()).toPyObject()))
        time.sleep(3)
        data['description']  =  base64.b64encode(self.description.text())
        data['put_member']   = get_cur_admin_id()

        (status,content) = my_business.add_bug(data)
        if status:
            Add.message = content
            Add.status = True
            self.parent.set_message(u'提示',content)
            self.accept()
        else:
            Add.message = content
            Add.status = False
            self.parent.set_message(u'错误',content)

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
            Add.message = content
            Add.status = False
            self.parent.set_message(u'警告',content)
            return False
        data.pop('re_passwd')
        (status,content) = my_business.add_admin(data)

        print 'content:%s'%content
        if status:
            Add.message = content
            Add.status = True
            self.parent.set_message(u'提示',content)
            self.accept()
        else:
            Add.message = content
            Add.status = False
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
            Add.message = content
            Add.status = True
            self.parent.set_message(u'提示',content)
            self.accept()
        else:
            Add.message = content
            Add.status = False
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
            Add.message = content
            Add.status = True
            self.parent.set_message(u'提示',content)
            self.accept()
        else:
            Add.message = content
            Add.status = False
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
            Add.message = content
            Add.status = False
            self.parent.set_message(u'错误',content)
            return False

        data['remartk']      = urllib.quote(str(self.remark.toPlainText()))
        data['create']      = get_cur_admin_id()

        (status,content) = my_business.add_resume(data)
        print 'content:%s'%content
        if status:
            Add.message = content
            Add.status = True
            self.parent.set_message(u'提示',content)
            self.accept()
        else:
            Add.message = content
            Add.status = False
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
            Add.message = content
            Add.status = True
            self.parent.set_message(u'提示',content)
            self.accept()
        else:
            Add.message = content
            Add.status = False
            self.parent.set_message(u'错误',content)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myWindow = Add()
    #myWindow.show()
    myWindow.showMaximized()
    sys.exit(app.exec_())


