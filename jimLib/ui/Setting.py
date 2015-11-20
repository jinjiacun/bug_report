# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from jimLib.lib.io import Db_Connector

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Setting(QtGui.QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8(u"设置"))
        Dialog.resize(672, 425)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(290, 380, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setText(u"确定")
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setText(u'取消')
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok)
        self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 671, 371))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(20, 20, 54, 12))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 54, 12))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 54, 12))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit = QtGui.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(110, 14, 231, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.tabWidget_2 = QtGui.QTabWidget(self.tab)
        self.tabWidget_2.setGeometry(QtCore.QRect(-10, -20, 671, 371))
        self.tabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.widget = QtGui.QWidget(self.tab_4)
        self.widget.setGeometry(QtCore.QRect(100, 50, 441, 271))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.txt_mqtt_host = QtGui.QLineEdit(self.widget)
        self.txt_mqtt_host.setObjectName(_fromUtf8("txt_mqtt_host"))
        self.horizontalLayout.addWidget(self.txt_mqtt_host)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.txt_mqtt_port = QtGui.QLineEdit(self.widget)
        self.txt_mqtt_port.setObjectName(_fromUtf8("txt_mqtt_port"))
        self.horizontalLayout_2.addWidget(self.txt_mqtt_port)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.txt_mqtt_topic = QtGui.QLineEdit(self.widget)
        self.txt_mqtt_topic.setObjectName(_fromUtf8("txt_mqtt_topic"))
        self.horizontalLayout_3.addWidget(self.txt_mqtt_topic)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tabWidget_2.addTab(self.tab_4, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.tabWidget_2.addTab(self.tab_5, _fromUtf8(""))
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6"))
        self.tabWidget_2.addTab(self.tab_6, _fromUtf8(""))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.widget1 = QtGui.QWidget(self.tab_2)
        self.widget1.setGeometry(QtCore.QRect(111, 51, 421, 271))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_7 = QtGui.QLabel(self.widget1)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_4.addWidget(self.label_7)
        self.txt_api_host = QtGui.QLineEdit(self.widget1)
        self.txt_api_host.setObjectName(_fromUtf8("txt_api_host"))
        self.horizontalLayout_4.addWidget(self.txt_api_host)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_8 = QtGui.QLabel(self.widget1)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_5.addWidget(self.label_8)
        self.txt_api_port = QtGui.QLineEdit(self.widget1)
        self.txt_api_port.setObjectName(_fromUtf8("txt_api_port"))
        self.horizontalLayout_5.addWidget(self.txt_api_port)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_9 = QtGui.QLabel(self.widget1)
        #self.label_9.setEnabled(False)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_9.setFixedWidth(30)
        self.horizontalLayout_6.addWidget(self.label_9)
        self.cmb_api_debug = QtGui.QComboBox(self.widget1)
        self.cmb_api_debug.setObjectName(_fromUtf8("cmb_api_debug"))
        self.horizontalLayout_6.addWidget(self.cmb_api_debug)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.layoutWidget_2 = QtGui.QWidget(self.tab_3)
        self.layoutWidget_2.setGeometry(QtCore.QRect(120, 50, 441, 271))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_10 = QtGui.QLabel(self.layoutWidget_2)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_7.addWidget(self.label_10)
        self.txt_edit_url = QtGui.QLineEdit(self.layoutWidget_2)
        self.txt_edit_url.setObjectName(_fromUtf8("txt_edit_url"))
        self.horizontalLayout_7.addWidget(self.txt_edit_url)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_11 = QtGui.QLabel(self.layoutWidget_2)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_8.addWidget(self.label_11)
        self.txt_edit_pic_url = QtGui.QLineEdit(self.layoutWidget_2)
        self.txt_edit_pic_url.setObjectName(_fromUtf8("txt_edit_pic_url"))
        self.horizontalLayout_8.addWidget(self.txt_edit_pic_url)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget_2.setCurrentIndex(0)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.setWindowTitle(u'系统设置')
        self.get_setting()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "TextLabel", None))
        self.label_2.setText(_translate("Dialog", "TextLabel", None))
        self.label_3.setText(_translate("Dialog", "TextLabel", None))
        self.label_4.setText(_translate("Dialog", "主机:", None))
        self.label_5.setText(_translate("Dialog", "端口:", None))
        self.label_6.setText(_translate("Dialog", "主题:", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("Dialog", "推送服务", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("Dialog", "接口服务", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("Dialog", "编辑服务", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "推送服务", None))
        self.label_7.setText(_translate("Dialog", "主机:", None))
        self.label_8.setText(_translate("Dialog", "端口:", None))
        self.label_9.setText(_translate("Dialog", "调试:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "接口服务", None))
        self.label_10.setText(_translate("Dialog", "网页url:", None))
        self.label_11.setText(_translate("Dialog", "网页图片url:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "编辑服务", None))

    def get_setting(self):
        import os
        my_connector = Db_Connector(os.getcwd()+'/config.ini')
        mqtt_host    = my_connector.get_value('serverconf','host')
        print 'mqtt_host:%s'%mqtt_host
        mqtt_port    = my_connector.get_value('serverconf','port')
        mqtt_topic   = my_connector.get_value('serverconf','topic')
        api_host     = my_connector.get_value('serverconf','api_host')
        api_port     = my_connector.get_value('serverconf','api_port')
        api_debug    = my_connector.get_value('serverconf','api_debug')
        edit_url     = my_connector.get_value('serverconf','edit_url')
        edit_pic_url = my_connector.get_value('serverconf','edit_pic_url')
        self.txt_mqtt_host.setText(mqtt_host)
        self.txt_mqtt_port.setText(mqtt_port)
        self.txt_mqtt_topic.setText(mqtt_topic)

        self.txt_api_host.setText(api_host)
        self.txt_api_port.setText(api_port)
        self.cmb_api_debug.addItem(u'是',QtCore.QVariant(1))
        self.cmb_api_debug.addItem(u'否',QtCore.QVariant(0))
        index = self.cmb_api_debug.findData(QtCore.QVariant(int(api_debug)))
        self.cmb_api_debug.setCurrentIndex(index)

        self.txt_edit_url.setText(edit_url)
        self.txt_edit_pic_url.setText(edit_pic_url)

    def set_setting(self):
        import os
        my_connector = Db_Connector(os.getcwd()+'/config.ini')
        mqtt_host    = my_connector.get_value('serverconf','host')
        print 'mqtt_host:%s'%mqtt_host

        mqtt_host = self.txt_mqtt_host.text()
        mqtt_port = self.txt_mqtt_port.text()
        mqtt_topic = self.txt_mqtt_topic.text()

        api_host = self.txt_api_host.text()
        api_port = self.txt_api_port.text()
        api_debug = self.cmb_api_debug.itemData(self.cmb_api_debug.currentIndex())

        edit_url = self.txt_edit_url.text()
        edit_pic_url = self.txt_edit_pic_url.text()

        my_connector.set_value('serverconf','host',mqtt_host)
        my_connector.set_value('serverconf','port',mqtt_port)
        my_connector.set_value('serverconf','topic',mqtt_topic)
        my_connector.set_value('serverconf','api_host',api_host)
        my_connector.set_value('serverconf','api_port',api_port)
        my_connector.set_value('serverconf','api_debug',api_debug)
        my_connector.set_value('serverconf','edit_url',edit_url)
        my_connector.set_value('serverconf','edit_pic_url',edit_pic_url)



    def ok(self):
        print 'ok'
        pass



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = Setting()
    mainWindow.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
