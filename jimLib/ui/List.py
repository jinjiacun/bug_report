 #!/usr/bin/env python
#coding=utf-8
import sip
#sip.setapi('QVariant', 2)

from PyQt4.QtGui  import *  #目测table的类应该是在qt.gui里面的
from PyQt4.QtCore import *
import math
import time
import urllib
from jimLib.lib.util import lib_post
from jimLib.lib.util import lib_format
from jimLib.lib.util import get_cur_admin_id
from jimLib.lib.util import Dict
from jimLib.lib.business import business


class KUnit:
    #调试类
    @staticmethod
    def run(name,C):

        if name == "__main__":
            import sys
            app = QApplication(sys.argv)

            obj = C()
            obj.show()
            sys.exit(app.exec_())

class KTabBar(QTabBar):

    #自定义tabbar,实现双击关闭
    def __init__(self,parent = None):
        QTabBar.__init__(self,parent)

    def mouseDoubleClickEvent(self, event):

        #获取点击的tab
        tabId = self.tabAt(event.pos())
        #发送关闭信号和tabid
        self.emit(SIGNAL("tabCloseRequested(int)"),self.tabAt(event.pos()))

        QTabBar.mouseDoubleClickEvent(self, event)

class MyDialog(QDialog):
    #数据列表
    table_list = {'Project':['id',u'编号',u'项目名称',u'创建人',u'最后更新时间',u'项目描述'],
                  'Bug':['id',u'编号',u'所属项目',u'指派给',u'所属模块',u'优先级',u'状态',u'最后更新人',u'最后更新日期',u'描述',u'提交人'],
                  'Admin':['id',u'编号',u'用户账号',u'姓名',u'状态',u'角色',u'部门',u'添加日期'],
                  'Role':['id',u'编号',u'名称',u'权限'],
                  'Part':['id',u'编号',u'部门名称',u'创建人',u'添加日期'],
                  'Resume':['id',u'编号',u'应聘人',u'联系方式',u'应聘岗位',u'应聘部门',u'进度',u'预约时间',u'状态',u'最后更新人',u'最后更新日期',u'备注'],
                  'Positionhr':['id',u'岗位',u'部门',u'状态',u'开启日期',u'发布人',u'要求'],
                  'Buglog':[]}

    #列表宽度
    table_width_list = {'Project':[0,100,200,100,150,500],
                        'Bug':[0,100,100,100,100,100,100,100,150,500,100],
                        'Admin':[0,100,100,100,100,100,100,200],
                        'Role':[0,100,100,500],
                        'Part':[0,100,100,100,200],
                        'Resume':[0,100,100,100,100,100,100,150,100,100,150,350],
                        'Positionhr':[0,100,100,100,150,100,500],
                        'Buglog':[]}

    #数据字段列表
    table_field_list = {'Project':['id','number','name','create','last_time','description'],
                        'Bug':['id','number','project_id','get_member','project_mod_id','level','status','last_update','last_update_time','title','put_member'],
                        'Admin':['id','number','admin_name','name','status','role','part','add_time'],
                        'Role':['id','number','name','resource'],
                        'Part':['id','number','name','create','add_time'],
                        'Resume':['id','number','candidates','telephone','position_id','part_id','stage','stage_time','status','last','last_time','remartk'],
                        'Positionhr':['id','name','part_id','status','start_time','create','description'],
                        'Buglog':[]}
    #数据格式化表
    '''0-数字,1-字符串,2-日期,3-人员,4-角色,5-项目,6-模块,7-优先级,8-bug状态,9-部门,10-用户状态,
   11-资源替换,12-人事岗位,13-简历进度,14-base64解码
   '''
    table_format_list = {'Project':[0,1,1,3,2,1],
                         'Bug':[0,1,5,3,6,7,8,3,2,1,3],
                         'Admin':[0,1,1,1,10,4,9,2],
                         'Role':[0,1,1,11],
                         'Part':[0,1,1,3,2],
                         'Resume':[0,1,1,1,12,9,13,2,10,3,2,1],
                         'Positionhr':[0,1,9,10,2,3,1],
                         'Buglog':[]}
    #
    table_action_list = {}

    table_cur_index = 0                         #数据列表索引
    my_dict = {}

    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.max_index = -1
        self.lbookmark = []
        self.page_size = 2
        self.page = [1,1,1,1,1,1,1,1]
        #引导
        #self.createWizard()

        self.createFilterGroupBox()
        self.createPageGroupBox()
       # self.createToolGroupBox()
        #self.init_data_project()

#        self.com_list.setCurrentIndex(2)
        self.MyTable = []
        for i in range(0,10):
            self.MyTable.append(QTableWidget())
            #self.MyTable[i].setAlternatingRowColors(True)

        self.tab = QTabWidget()
        self.tab.currentChanged.connect(self.tab_change)
        layout = QVBoxLayout()
        #layout.addWidget(self.wizardGroupBox)
        layout.addWidget(self.filterGroupBox)
        layout.addWidget(self.pageGroupBox)
        #layout.addWidget(self.toolGroupBox)
        self.tab.setTabBar(KTabBar())
        self.tab.setTabsClosable(True)
        '''
        self.tab.addTab(self.MyTable[0],u'项目列表')
        self.tab.addTab(self.MyTable[1],u'问题列表')
        self.tab.addTab(self.MyTable[2],u'用户列表')
        self.tab.addTab(self.MyTable[3],u'角色列表')
        self.tab.addTab(self.MyTable[4],u'部门列表')
        self.tab.addTab(self.MyTable[5],u'招聘列表')
        self.tab.addTab(self.MyTable[6],u'岗位列表')
        self.tab.addTab(self.MyTable[7],u'日志列表')
        '''
        layout.addWidget(self.tab)
        self.setLayout(layout)

        #双击关闭
        self.connect(self.tab, SIGNAL("tabCloseRequested(int)"),self.closeTab)


        self.init_dict()

        self.setWindowFlags(Qt.Window)

    def tab_change(self,index):
        if 0< len(self.lbookmark):
            i = 0
            for value in self.lbookmark:#value为table索引
                if i == index:
                    self.change_table(value)
                    break
                i += 1

    def closeTab(self,tabId):
        #移除
        index = 0
        #后面的序列号前移动
        for i in self.lbookmark:
            if index == tabId:
                self.lbookmark.remove(i)
                break
            index += 1
        self.max_index -= 1
        #关闭置顶信号槽
        self.tab.removeTab(tabId)

    #初始化字典
    def init_dict(self):
        method  = 'Map.get_map'
        content = {}
        result = lib_post(method, content)
        MyDialog.my_dict = result['content']
        print MyDialog.my_dict
        pass

    def createWizard(self):
        self.wizardGroupBox = QGroupBox(u"引导操作")
        layout = QHBoxLayout()
        self.com_list = QComboBox()
        self.com_list.addItem('0'),self.com_list.addItem('1'),self.com_list.addItem('2')
        self.com_list.addItem('3'),self.com_list.addItem('4'),self.com_list.addItem('5')
        self.com_list.addItem('6')
        layout.addWidget(self.com_list)

        btn_change = QPushButton(u'切换测试')
        btn_change.clicked.connect(self.change_table)
        layout.addWidget(btn_change)
        self.wizardGroupBox.setLayout(layout)
        pass

    #切换列表
    def change_table(self, index=0, where={},is_clean=True):
        #MyDialog.table_cur_index = str(self.com_list.currentText())
        if index>=0:
            MyDialog.table_cur_index = index
            #self.tab.setCurrentIndex(index)
            #if self.max_index <8:
            if index in self.lbookmark:
                item = 0
                for i in self.lbookmark:
                    if i == index:
                        self.tab.setCurrentIndex(item)
                    item += 1
            else:
                self.max_index += 1
                #self.max_index = self.max_index % 8
                self.lbookmark.append(index)
                #self.lbookmark[index] =
                self.tab.addTab(self.MyTable[index],Dict.menu_list[index])
                self.tab.setCurrentIndex(self.tab.count()-1)
        else:
            MyDialog.table_cur_index = int(self.com_list.currentText())
        i =j=0

        self.createFilterDymic(is_clean)

        #情况内容
        self.MyTable[index].clear()

        self.MyTable[index].setColumnCount(len(self.table_list[Dict.module_list[MyDialog.table_cur_index]]))
        self.MyTable[index].setHorizontalHeaderLabels(self.table_list[Dict.module_list[MyDialog.table_cur_index]])

        #设置列宽度
        for width in MyDialog.table_width_list[Dict.module_list[MyDialog.table_cur_index]]:
            self.MyTable[index].setColumnWidth(i, MyDialog.table_width_list[Dict.module_list[MyDialog.table_cur_index]].__getitem__(i))
            i += 1

        #绑定数据
        method  = Dict.module_list[MyDialog.table_cur_index]+'.get_list'
        content = {'page_size':self.page_size,'page_index':self.page[index]}
        if 0< len(where):
            content['where'] = where
        result = lib_post(method, content)
        if 200 == result['status_code']:
            rows = len(result['content']['list'])
            record_count = int(result['content']['record_count'])
            self.record_count.setText(unicode(record_count))
            page_count = record_count/self.page_size
            if 0 <> record_count%self.page_size:
                page_count += 1
            self.cmb_page.clear()
            for i in range(0,page_count):
                self.cmb_page.addItem(unicode(i+1),QVariant(i+1))
            i = 0
            if rows >self.page_size:
                rows = self.page_size
            if is_clean:
                self.btn_prefix.setEnabled(True)
                self.btn_next.setEnabled(True)
            self.MyTable[index].setRowCount(rows)
            for i in range(0, rows):
                j = 0
                for field in MyDialog.table_field_list[Dict.module_list[MyDialog.table_cur_index]]:
                    itemValue = lib_format(MyDialog.table_format_list[Dict.module_list[MyDialog.table_cur_index]][j],
                                              result['content']['list'][i][field],
                                              MyDialog.my_dict)
                    newItem = QTableWidgetItem(itemValue)
                    #newItem.setText(itemValue)
                    newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.MyTable[index].setItem(i, j, newItem)
                    j += 1
                i += 1

    #筛选条件
    def createFilterGroupBox(self):
        self.filterGroupBox = QGroupBox(u"筛选条件")
        self.layout = QHBoxLayout()
        self.filterGroupBox.setLayout(self.layout)

    def createFilterDymic(self,is_clean=True):
        my_business = business()
        if is_clean:
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().deleteLater()
        else:
            return

        if 0 == MyDialog.table_cur_index:
            self.layout.addWidget(QLabel(u"项目名称:"))
            self.txt_keyword = QLineEdit()
            self.layout.addWidget(self.txt_keyword)

        elif 1 == MyDialog.table_cur_index:
            self.layout.addWidget(QLabel(u"项目:"))
            self.project_id = QComboBox()
            (status,my_dict) = my_business.get_dict()
            self.project_id.addItem(u'----项目----',QVariant(0))
            self.my_dict = my_dict
            if my_dict.has_key('project'):
                for (key,value) in my_dict['project'].items():
                    self.project_id.addItem(value,QVariant(key))
            self.layout.addWidget(self.project_id)
            self.layout.addWidget(QLabel(u"模块:"))
            self.connect(self.project_id, SIGNAL('activated(int)'), self.onActivatedModule)
            self.project_mod_id = QComboBox()
            self.project_mod_id.setFixedWidth(150)
            self.project_mod_id.addItem(u'----项目模块----',QVariant(0))
            self.layout.addWidget(self.project_mod_id)
            self.layout.addWidget(QLabel(u"状态:"))
            self.status = QComboBox()
            self.status.addItem(u'----状态----',QVariant(0))
            self.status.setFixedWidth(100)
            self.status.addItem(u'待解决',QVariant(1))
            self.status.addItem(u'已解决',QVariant(2))
            self.status.addItem(u'已关闭',QVariant(3))
            self.layout.addWidget(self.status)
            self.layout.addWidget(QLabel(u"分类:"))
            self.classify = QComboBox()
            self.classify.addItem(u'----分类----',QVariant(0))
            self.classify.setFixedWidth(100)
            self.classify.addItem(u'指派给我的',QVariant(1))
            self.classify.addItem(u'我提交的',QVariant(2))
            self.classify.addItem(u'我相关的',QVariant(3))
            self.layout.addWidget(self.classify)
            self.layout.addWidget(QLabel(u"编号关键字:"))
            self.txt_keyword = QLineEdit()
            self.layout.addWidget(self.txt_keyword)
        elif 2 == MyDialog.table_cur_index:
            self.layout.addWidget(QLabel(u"用户帐号:"))
            self.txt_keyword = QLineEdit()
            self.layout.addWidget(self.txt_keyword)
        elif 3 == MyDialog.table_cur_index:
            self.layout.addWidget(QLabel(u"角色名称:"))
            self.txt_keyword = QLineEdit()
            self.layout.addWidget(self.txt_keyword)
        elif 4 == MyDialog.table_cur_index:
            self.layout.addWidget(QLabel(u"部门名称:"))
            self.txt_keyword = QLineEdit()
            self.layout.addWidget(self.txt_keyword)
        elif 5 == MyDialog.table_cur_index:
            self.layout.addWidget(QLabel(u"进度:"))
            self.stage = QComboBox()
            self.stage.addItem(u'----进度----',QVariant(0))
            self.stage.setFixedWidth(100)
            self.stage.addItem(u'未筛选',QVariant(1))
            self.stage.addItem(u'未预约',QVariant(2))
            self.stage.addItem(u'已预约',QVariant(3))
            self.stage.addItem(u'面试',QVariant(4))
            self.stage.addItem(u'复试',QVariant(5))
            self.stage.addItem(u'入职',QVariant(6))
            self.stage.addItem(u'废弃',QVariant(7))
            self.layout.addWidget(self.stage)
            self.layout.addWidget(QLabel(u"应聘部门:"))
            self.part_id = QComboBox()
            (status,content) = my_business.get_dict()
            self.part_id.addItem(u'----部门----',QVariant(0))
            self.part_id.setFixedWidth(100)
            if status:
                for (key,value) in content['part'].items():
                    self.part_id.addItems([value])
            self.layout.addWidget(self.part_id)
            self.layout.addWidget(QLabel(u"应聘岗位:"))
            self.position_id = QComboBox()
            self.position_id.addItem(u'----应聘岗位----',QVariant(0))
            self.position_id.setFixedWidth(150)
            if status:
                if content.has_key('positionhr'):
                    for (key,value) in content['positionhr'].items():
                        self.position_id.addItems([value])
            self.layout.addWidget(self.position_id)
            self.layout.addWidget(QLabel(u"应聘人:"))
            self.txt_keyword = QLineEdit()
            self.layout.addWidget(self.txt_keyword)
        elif 6 == MyDialog.table_cur_index:
            self.layout.addWidget(QLabel(u"岗位名称:"))
            self.txt_keyword = QLineEdit()
            self.layout.addWidget(self.txt_keyword)
        elif 7 == MyDialog.table_cur_index:
            self.layout.addWidget(QLabel(u"系统类型:"))
            self.system = QComboBox()
            self.system.addItem(u'----系统类型----',QVariant(0))
            self.system.setFixedWidth(150)
            self.system.addItem(u'IOS',QVariant(1))
            self.system.addItem(u'Android',QVariant(2))
            self.layout.addWidget(self.system)
            self.layout.addWidget(QLabel(u"应用名称:"))
            self.txt_keyword = QLineEdit()
            self.layout.addWidget(self.txt_keyword)
        self.bn_select = QPushButton(u"查询")
        self.layout.addWidget(self.bn_select)
        self.layout.addWidget(QSplitter())
        self.bn_select.clicked.connect(self.action_select)

    #创建分页组
    def createPageGroupBox(self):
        self.pageGroupBox = QGroupBox(u"分页")
        layout = QHBoxLayout()
        self.btn_prefix = QPushButton(u'上一页')
        layout.addWidget(self.btn_prefix)
        self.btn_prefix.clicked.connect(self.page_prefix)
        self.btn_next = QPushButton(u'下一页')
        layout.addWidget(self.btn_next)
        self.btn_next.clicked.connect(self.page_next)
        label = QLabel(u'转到第:')
        layout.addWidget(label)
        txt_page_index = QLineEdit()
        txt_page_index.setFixedWidth(70)
        layout.addWidget(txt_page_index)
        label = QLabel(u'页,总共')
        layout.addWidget(label)
        self.record_count = QLabel()
        layout.addWidget(self.record_count)
        label = QLabel(u'条记录')
        layout.addWidget(label)
        self.cmb_page = QComboBox()
        layout.addWidget(self.cmb_page)
        btn_go = QPushButton('G&o')
        layout.addWidget(btn_go)
        layout.addWidget(QSplitter())
        self.pageGroupBox.setLayout(layout)
        pass

    #上一页
    def page_prefix(self):
        record_count = int(self.record_count.text())
        self.page[self.table_cur_index] -= 1
        if self.page[self.table_cur_index]<1:
            self.page[self.table_cur_index] = 1
            self.btn_prefix.setEnabled(False)
        self.change_table(self.table_cur_index)

        if 1 == self.page[self.table_cur_index]:
            self.btn_prefix.setEnabled(False)
            self.btn_next.setEnabled(True)

    def page_next(self):
        record_count = int(self.record_count.text())
        page_count = record_count/self.page_size
        if 0 <> record_count%self.page_size:
            page_count += 1
        self.page[self.table_cur_index] += 1
        if page_count>= self.page[self.table_cur_index]:
            self.btn_next.setEnabled(True)
            self.change_table(self.table_cur_index)

        if page_count <= self.page[self.table_cur_index]:
            self.page[self.table_cur_index] = page_count
            self.btn_prefix.setEnabled(True)
            self.btn_next.setEnabled(False)


    #级联关系(项目-模块)
    def onActivatedModule(self, cuindex):
        #print 'cuindex:%d'%cuindex
        project_id = cuindex
        if 0 == project_id:
            self.project_mod_id.clear()
            self.project_mod_id.addItem(u'----项目模块----',QVariant(0))
        if 0 >= project_id:
            return
        #查询项目下面的模块
        my_business = business()
        (status,content) = my_business.get_project_mod_by_project_id(project_id)
        self.project_mod_id.clear()
        self.project_mod_id.addItem(u'----项目模块----',QVariant(0))
        if status:
            for (key,item) in content.items():
                self.project_mod_id.addItem(unicode(key),QVariant(item))

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
        result = lib_post(method, content)
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
        where = {}
        if 0 == MyDialog.table_cur_index:#项目列表
            if '' != str(self.txt_keyword.text()).strip():
                keyword = urllib.quote(str(self.txt_keyword.text()))
                where['name'] = ['like','$%s$'%keyword]
        elif 1 == MyDialog.table_cur_index:#bug列表
            if 0 < int(str(self.project_id.itemData(self.project_id.currentIndex()).toPyObject())):
                where['project_id'] = urllib.quote(str(self.project_id.itemData(self.project_id.currentIndex()).toPyObject()))
            if 0 < int(str(self.project_mod_id.itemData(self.project_mod_id.currentIndex()).toPyObject())):
                where['project_mod_id'] = urllib.quote(str(self.project_mod_id.itemData(self.project_mod_id.currentIndex()).toPyObject()))
            if 0 < int(str(self.status.itemData(self.status.currentIndex()).toPyObject())):
                where['status'] = urllib.quote(str(self.status.itemData(self.status.currentIndex()).toPyObject()))
            if 0 < int(str(self.classify.itemData(self.classify.currentIndex()).toPyObject())):
                my_class = str(self.classify.itemData(self.classify.currentIndex()).toPyObject())
                if 1 == my_class:#指派给我
                    where['get_member'] = urllib.quote(get_cur_admin_id())
                elif 2 == my_class:#我提交
                    where['put_member'] = urllib.quote(get_cur_admin_id())
                elif 3 == my_class:#我相关的(我提交或者我接受的)
                    where['_logic'] = 'or'
                    where['_complex'] = {'get_member':urllib.quote(get_cur_admin_id()),'put_member':urllib.quote(get_cur_admin_id())}
            if '' != str(self.txt_keyword.text()).strip():
                keyword = urllib.quote(str(self.txt_keyword).toPyObject())
                where['number'] = ['like','$%s$'%keyword]
        elif 2 == MyDialog.table_cur_index:#用户列表
            if '' != str(self.txt_keyword.text()).strip():
                keyword = str(self.txt_keyword.text()).strip()
                where['admin_name'] = ['like','$%s$'%keyword]
        elif 3 == MyDialog.table_cur_index:#角色列表
            if '' != str(self.txt_keyword.text()).strip():
                keyword = str(self.txt_keyword.text()).strip()
                where['name'] = ['like','$%s$'%keyword]
        elif 4 == MyDialog.table_cur_index:#部门列表
            if '' != str(self.txt_keyword.text()).strip():
                keyword = str(self.txt_keyword.text()).strip()
                where['name'] = ['like','$%s$'%keyword]
        elif 5 == MyDialog.table_cur_index:#简历列表
            if 0 < int(str(self.stage.itemData(self.stage.currentIndex()).toPyObject())):
                where['stage'] = urllib.quote(str(self.stage.itemData(self.stage.currentIndex()).toPyObject()))
            if 0 < int(str(self.part_id.itemData(self.part_id.currentIndex()).toPyObject())):
                where['part_id'] = urllib.quote(str(self.part_id.itemData(self.part_id.currentIndex()).toPyObject()))
            if 0 < int(str(self.position_id.itemData(self.position_id.currentIndex()).toPyObject())):
                where['position_id'] = urllib.quote(str(self.position_id.itemData(self.position_id.currentIndex()).toPyObject()))
            if '' != str(self.txt_keyword.text()).strip():
                keyword = str(self.txt_keyword.text()).strip()
                where['candidates'] = urllib.quote(str(self.txt_keyword.text()).strip())
        elif 6 == MyDialog.table_cur_index:#简历岗位
            if '' != str(self.txt_keyword.text()).strip():
                keyword = str(self.txt_keyword.text()).strip()
                where['name'] = ['like','$%s$'%keyword]
        elif 7 == MyDialog.table_cur_index:#系统日志
            if 0 < int(str(self.system.itemData(self.system.currentIndex()).toPyObject())):
                where['system'] = ['like','$%s$'%urllib.quote(str(self.system.currentText()))]
            if '' != str(self.txt_keyword.text()).strip():
                keyword = str(self.txt_keyword.text()).strip()
                if where.has_key('system'):
                    where['_logic'] = 'or'
                    where['_complex'] = {'system':where['system'],'app_name':['like','$%s$'%urllib.quote(keyword)]}
                    where.pop('system')
                else:
                    where['app_name'] = ['like','$%s$'%keyword]
        #调用数据列表
        self.change_table(MyDialog.table_cur_index,where,False)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myWindow = MyDialog()
    #myWindow.show()
    myWindow.showMaximized()
    sys.exit(app.exec_())

