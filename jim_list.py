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


class MyDialog(QDialog):
    #数据列表
    table_list = {'Project':[u'编号',u'项目名称',u'创建人',u'最后更新时间',u'项目描述'],
                  'Bug':[u'编号',u'所属项目',u'指派给',u'所属模块',u'优先级',u'状态',u'最后更新人',u'最后更新日期',u'描述',u'提交人'],
                  'Admin':[u'编号',u'用户账号',u'姓名',u'状态',u'角色',u'部门',u'添加日期'],
                  'Role':[u'编号',u'名称',u'权限'],
                  'Part':[u'编号',u'部门名称',u'创建人',u'添加日期'],
                  'Resume':[u'编号',u'应聘人',u'联系方式',u'应聘岗位',u'应聘部门',u'进度',u'预约时间',u'状态',u'最后更新人',u'备注'],
                  'Positionhr':[u'岗位',u'部门',u'状态',u'开启日期',u'发布人',u'要求']}

    #列表宽度
    table_width_list = {'Project':[100,200,100,150,500],
                        'Bug':[100,100,100,100,100,100,100,100,100,100],
                        'Admin':[100,100,100,100,100,100,100],
                        'Role':[100,100,100],
                        'Part':[100,100,100,100],
                        'Resume':[100,100,100,100,100,100,100,100,100,100],
                        'Positionhr':[100,100,100,100,100,100,100]}

    #数据字段列表
    table_field_list = {'Project':['number','name','create','last_time','description'],
                        'Bug':['number','project_id','get_member','project_mod_id','level','status','last_update','last_update_time','description','put_member'],
                        'Admin':[u'number','admin_name','name','status','role','part','add_time'],
                        'Role':['number','name','resource'],
                        'Part':['number','name','create','add_time'],
                        'Resume':['number','candidates','telephone','position_id','part_id','stage','stage_time','status','last','remartk'],
                        'Positionhr':['name','part_id','status','start_time','create','description']}
    #数据格式化表
    table_format_list = {'Project':['%s','%s','%s','%s','%s'],
                         'Bug':[],
                         'Admin':[]}
    #
    table_action_list = {}

    table_cur_index = 'Admin'                         #数据列表索引

    def __init__(self, parent=None):  
        super(MyDialog, self).__init__(parent)

        #引导
        self.createWizard()

        self.createFilterGroupBox()
        self.createToolGroupBox()
        #self.init_data_project()

        self.com_list.setCurrentIndex(2)

        self.MyTable = QTableWidget()
        self.MyTable.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.addWidget(self.wizardGroupBox)
        layout.addWidget(self.filterGroupBox)
        layout.addWidget(self.toolGroupBox)
        layout.addWidget(self.MyTable)  
        self.setLayout(layout)      
        
        self.setWindowFlags(Qt.Window)

    def createWizard(self):
        self.wizardGroupBox = QGroupBox(u"引导操作")
        layout = QHBoxLayout()
        self.com_list = QComboBox()
        self.com_list.addItem('Project'),self.com_list.addItem('Bug'),self.com_list.addItem('Admin')
        self.com_list.addItem('Role'),self.com_list.addItem('Part'),self.com_list.addItem('Resume')
        self.com_list.addItem('Positionhr')
        layout.addWidget(self.com_list)

        btn_change = QPushButton(u'切换测试')
        btn_change.clicked.connect(self.change_table)
        layout.addWidget(btn_change)
        self.wizardGroupBox.setLayout(layout)
        pass

    #切换列表
    def change_table(self, index=''):
        #MyDialog.table_cur_index = str(self.com_list.currentText())
        if '' == index:
            MyDialog.table_cur_index = str(self.com_list.currentText())
        else:
            MyDialog.table_cur_index = index
        i =j=0

        #情况内容
        self.MyTable.clear()

        self.MyTable.setColumnCount(len(self.table_list[MyDialog.table_cur_index]))
        self.MyTable.setHorizontalHeaderLabels(self.table_list[MyDialog.table_cur_index])

        #设置列宽度
        for width in MyDialog.table_width_list[MyDialog.table_cur_index]:
            self.MyTable.setColumnWidth(i, MyDialog.table_width_list[MyDialog.table_cur_index].__getitem__(i))
            i += 1


        #绑定数据
        method  = MyDialog.table_cur_index+'.get_list'
        content = {'page_size':10}
        result = lib.lib_post(method, content)
        if 200 == result['status_code']:
            rows = int(result['content']['record_count'])
            i = 0
            if rows >10:
                rows = 10
            for i in range(0, rows):
                j = 0
                for field in MyDialog.table_field_list[MyDialog.table_cur_index]:
                    itemValue = "%s"%result['content']['list'][i][field]
                    newItem = QTableWidgetItem(itemValue)
                    #newItem.setText(itemValue)
                    newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.MyTable.setItem(i, j, newItem)
                    j += 1
                i += 1
        self.MyTable.setRowCount(rows)

    #筛选条件
    def createFilterGroupBox(self):
        self.filterGroupBox = QGroupBox(u"筛选条件")
        layout = QHBoxLayout()
        layout.addWidget(QLabel(u"项目名称:"))
        self.txt_keyword = QLineEdit()
        layout.addWidget(self.txt_keyword)
        self.bn_select = QPushButton(u"查询")
        layout.addWidget(self.bn_select)
        self.filterGroupBox.setLayout(layout)
        self.bn_select.clicked.connect(self.action_select)

    #快捷工具
    def createToolGroupBox(self):
        self.toolGroupBox = QGroupBox(u"工具箱")
        layout = QHBoxLayout()
        item = QPushButton(u"新增项目")
        layout.addWidget(item)
        layout.addWidget(QPushButton(u"批量删除"))
        layout.addWidget(QPushButton(u"查询所有"))
        self.toolGroupBox.setLayout(layout)

    def init_data_project(self):
        method  = 'Project.get_list'
        content = {'page_size':20}
        result = lib.lib_post(method, content)
        rows = int(result['content']['record_count'])
        self.MyTable = QTableWidget(rows, 5)  
        self.MyTable.setHorizontalHeaderLabels([u'编号',u'项目名称',u'创建人',u'最后更新日期',u'项目描述'])  

        #调整列宽度
        self.MyTable.setColumnWidth(0,100)#编号
        self.MyTable.setColumnWidth(1,200)#项目名称
        self.MyTable.setColumnWidth(2,100)#创建人
        self.MyTable.setColumnWidth(3,150)#最后更新时间
        self.MyTable.setColumnWidth(4,1000)#项目描述

        if 200 == result['status_code']:
            for i in range(0, int(result['content']['record_count'])):
                #编号
                newItem = QTableWidgetItem(result['content']['list'][i]['number'])
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter) 
                self.MyTable.setItem(i, 0, newItem)          

                #项目名称
                newItem = QTableWidgetItem(result['content']['list'][i]['name'])  
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 1, newItem)   

                #创建人
                newItem = QTableWidgetItem(result['content']['list'][i]['create'])  
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 2, newItem)          

                #最后更新日期
                newItem = QTableWidgetItem(lib.timestamp_datetime(result['content']['list'][i]['last_time'])) 
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 3, newItem)

                #项目描述
                newItem = QTableWidgetItem(result['content']['list'][i]['description'])  
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 4, newItem)  

    #----------------------------action------------------------
    #查询action
    def action_select(self):
        keyword = unicode(self.txt_keyword.text().toUtf8(),'utf8','ignore').encode('utf8')
        #keyword = '测试'
        #unicode(self.txt_keyword.text().toUtf8(),'utf8','ignore').encode('utf8')
        #keyword = unicode(str(keyword))
        #keyword = urllib.quote(keyword.encode('utf-8'))
        method  = 'Project.get_list'
        content = {'page_size':20,'where':{'name':['like','$'+urllib.quote(keyword)+'$']}}
        result  = lib.lib_post(method, content)
        row_count = 0
        if 200 == result['status_code']:
            cur_row_count = self.MyTable.rowCount()
            self.MyTable.setRowCount(0)
            self.MyTable.clearContents()
            for i in range(0,cur_row_count):
                self.MyTable.removeRow(i)
            row_count = int(result['content']['record_count'])
            self.MyTable.setRowCount(int(result['content']['record_count']))
            for i in range(0, row_count):
                #编号
                newItem = QTableWidgetItem(result['content']['list'][i]['number'])
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 0, newItem)

                #项目名称
                newItem = QTableWidgetItem(result['content']['list'][i]['name'])
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 1, newItem)

                #创建人
                newItem = QTableWidgetItem(result['content']['list'][i]['create'])
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 2, newItem)

                #最后更新日期
                newItem = QTableWidgetItem(lib.timestamp_datetime(result['content']['list'][i]['last_time']))
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 3, newItem)

                #项目描述
                newItem = QTableWidgetItem(result['content']['list'][i]['description'])
                newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.MyTable.setItem(i, 4, newItem)

if __name__ == '__main__':  
    import sys  
    app = QApplication(sys.argv)  
    myWindow = MyDialog()
    #myWindow.show()
    myWindow.showMaximized()
    sys.exit(app.exec_())         
