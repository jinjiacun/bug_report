# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from jimLib.widget.CheckboxEx import CheckboxEx
from jimLib.lib.util import lib_post

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
多个复选框
列表中包含删除项目
'''
class MulCheckedBox(QtGui.QWidget):
    def __init__ (self, parent = None,resource=None):
        super(MulCheckedBox, self).__init__(parent)
        self.re_data = []
        self.data = {}#资源名称-id的键值对
        self.cur_row = -1
        if resource:
            self.data = resource
        self.setWindowTitle("weather")
        self.resize(200, 200)
        girdLayout = QtGui.QGridLayout()
        girdLayout.setMargin(0)
        rows = 0
        cols = 0
        print self.data
        #复选框
        for (key,item) in self.data.items():
            print 'key:%s'%key
            newCheckBox = CheckboxEx(self,item)
            newCheckBox.setText(key)
            newCheckBox.stateChanged.connect(self.my_select)
            newCheckBox.setFixedWidth(100)
            girdLayout.addWidget(newCheckBox,rows,cols)
            cols += 1
            if cols>3:
                cols = 0
                rows += 1

        self.setLayout( girdLayout)

    #选中
    def my_select(self,checked):
        checkbox = self.sender()
        if checked:
            print checkbox.value()
            #self.re_data.append(self.data[str(checkbox.value())])
            pass
        else:
            #self.re_data.remove(self.data[str(checkbox.value())])
            pass
        pass

    def text(self):
        return self.re_data

if __name__ == '__main__':
    app = QtGui.QApplication([])

    data = {}
    method = 'Resource.get_list'
    content={'order':{'id':'asc'}}
    result = lib_post(method,content)
    rows = int(result['content']['record_count'])
    for i in range(0,rows-1):
        key = result['content']['list'][i]['source_name']
        id  = result['content']['list'][i]['id']
        data[key] = id
        pass
    window = MulCheckedBox(None,data)
    window.show()
    sys.exit(app.exec_())