# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

'''
一个text文本框和一个按钮
列表中包含删除项目
'''
class TextButton(QtGui.QWidget):
    def __init__ (self, parent = None):
        super(TextButton, self).__init__(parent)
        self.setWindowTitle("weather")
        self.resize(1000, 200)
        girdLayout = QtGui.QGridLayout()

        #按钮
        button1 = QtGui.QPushButton('+')
        girdLayout.addWidget ( button1 , 0, 1)
        #列表
        list = QtGui.QListView()
        girdLayout.addWidget(list,0,0)
        '''
        #文本条
        textFile = QtGui.QLineEdit()
        girdLayout.addWidget( textFile, 0, 2 )
        #密码条
        passwordFile = QtGui.QLineEdit()
        passwordFile.setEchoMode( QtGui.QLineEdit.Password )
        girdLayout.addWidget( passwordFile, 1, 2)
        #编辑框
        textArea = QtGui.QTextEdit()
        girdLayout.addWidget(textArea , 2, 2 )
        #单选框&复选框
        self.radio1 = QtGui.QRadioButton('radio1')
        self.radio2 = QtGui.QRadioButton('radio2')
        self.radio3 = QtGui.QRadioButton('radio3')
        girdLayout.addWidget( self.radio1 , 3 ,0)
        girdLayout.addWidget( self.radio2 , 3 ,1)
        girdLayout.addWidget( self.radio3 , 3 ,2)
        checkbox1 = QtGui.QCheckBox('checkbox1')
        checkbox2 = QtGui.QCheckBox('checkbox2')
        checkbox3 = QtGui.QCheckBox('checkbox2')
        girdLayout.addWidget( checkbox1 , 4, 0)
        girdLayout.addWidget( checkbox2 , 4, 1)
        girdLayout.addWidget( checkbox3 , 4, 2)

        self.button = QtGui.QPushButton('ok')
        girdLayout.addWidget( self.button, 5 , 0)

        self.connect(self.button ,QtCore.SIGNAL('clicked()'),self.OnButton )
        '''
        self.setLayout( girdLayout)

    def OnButton(self ):
        if self.radio2.isChecked():
            self.radio2.setText('haha')

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = List()
    window.show()
    sys.exit(app.exec_())

