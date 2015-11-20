# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

import math
import os
from jimLib.ui.List import MyDialog
from PyQt4 import QtCore, QtGui
from jimLib.ui.Add import Add
from jimLib.ui.Edit import Edit
from jimLib.lib.io import Db_Connector

class MainWindow(QtGui.QMainWindow):
    InsertTextButton = 10
    emit_python_list = QtCore.pyqtSignal(object)
    def __init__(self):
        super(MainWindow, self).__init__()

        self.createActions()
        self.createMenus()
        self.createToolBar()
        self.createToolBox()

        #DiagramScene(self.itemMenu)
        #self.scene.setSceneRect(QtCore.QRectF(0, 0, 5000, 5000))#填充右半部分
        #import list
        #self.scene.setSceneRect(list.MyDialog(None))
        #self.scene.itemInserted.connect(self.itemInserted)
        #self.scene.textInserted.connect(self.textInserted)
        #self.scene.itemSelected.connect(self.itemSelected)


        self.scene = MyDialog()

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.toolBox)
        #self.view = QtGui.QGraphicsView(self.scene)
        #layout.addWidget(self.view)

        self.timer = QtCore.QTimer()

        #托盘
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        icon_path = os.getcwd()
        icon = QtGui.QIcon(os.path.join(icon_path+'./images/un_load.png'))
        self.trayIcon.setIcon(icon)
        self.trayIcon.show()

        layout.addWidget(self.scene)
        self.emit_python_list.connect(self.deal_sig)

        self.widget = QtGui.QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        self.setWindowTitle(u"bug客户端")

    #创建工具栏
    def createToolBar(self):
        #self.exit=QtGui.QAction(u'退出',self)
        #self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #self.toolbar.addAction(self.exit)

        #新增
        self.add = QtGui.QAction(QtGui.QIcon('images/tool_Add1.png'), u'新增',self)
        self.add.setIconText(u'新增')
        self.connect(self.add, QtCore.SIGNAL('triggered()'), self.handle_add)
        self.toolbar.addAction(self.add)

        #修改
        self.edit = QtGui.QAction(QtGui.QIcon('images/tool_edit1.png'), u'修改',self)
        self.connect(self.edit, QtCore.SIGNAL("triggered()"), self.handle_edit)
        self.toolbar.addAction(self.edit)

        #删除
        self.delete = QtGui.QAction(QtGui.QIcon('images/tool_del.png'), u'删除',self)
        self.connect(self.delete, QtCore.SIGNAL("triggered()"), self.handle_delete)
        self.toolbar.addAction(self.delete)

        #刷新
        self.refresh = QtGui.QAction(QtGui.QIcon('images/tool_MB_0015_reload.png'), u'刷新',self)
        self.connect(self.refresh, QtCore.SIGNAL("triggered()"), self.handle_refresh)
        self.toolbar.addAction(self.refresh)
        pass

    #设置消息
    def set_message(self,title,message):
        icon = QtGui.QSystemTrayIcon.MessageIcon(QtGui.QStyle.SP_MessageBoxInformation)
        self.trayIcon.showMessage(title,
                    message, icon,
                    15 * 1000)
        pass

    #切换托盘图片
    def set_tray(self,index):
        icon_path = os.getcwd()
        if 0 == index:#unload
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/un_load.png'))
        elif 1 == index:#load
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/normal.png'))
        elif 2 == index:#err
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/error.png'))
        elif 3 == index:#yellow warn
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/warn_yellow.png'))
        elif 4 == index:#red warn
            icon = QtGui.QIcon(os.path.join(icon_path+'/images/warn_red.png'))
        self.trayIcon.setIcon(icon)
        pass

    def my_time(self):
        #定义定时器
        self.timer.timeout.connect(self.flash)
        self.timer.start(500)
        self.flag = 0

     #定时闪烁
    def flash(self):
        icon_path = os.getcwd();
        icon = QtGui.QIcon(os.path.join(icon_path+'/images/warn_red.png'))
        if 0 == self.flag:
            self.flag = 1
            self.trayIcon.setIcon(QtGui.QIcon())
            #print 1
        else:
            self.flag = 0
            self.trayIcon.setIcon(icon)
            #print 0

    def touch_sig(self,msg):
        self.emit_python_list.emit(msg)

    def deal_sig(self, msg):
        if str(1) == str(msg):#高级警告
            self.set_message(u'严重警告',u'严重bug')
            self.set_tray(4)
            #定时
            self.timer.start()
        elif str(0) == str(msg):#取消高级警告
            self.set_tray(1)
            self.timer.stop()
        elif str(2) == str(msg):#一般警告
            self.set_message(u'警告',u'有bug')
            self.set_tray(3)
            self.timer.stop()

    #工具栏处理
    def handle_add(self):
        self.add_dialog = Add(self,self.scene.table_cur_index,self.scene.table_cur_index)
        if self.add_dialog.exec_() == QtGui.QDialog.Accepted:
            #梳理返回值
            if Add.status:
                self.scene.change_table(self.scene.table_cur_index)
            pass
        pass

    def handle_edit(self):
        #获取当前模块的id
        if -1 == self.scene.MyTable.currentRow():
            item = self.scene.MyTable.item(0,0)
            pass
        else:
            item = self.scene.MyTable.item(self.scene.MyTable.currentRow(),0)
            pass
        id = int(item.text())
        self.edit_dialog = Edit(self,self.scene.table_cur_index,self.scene.table_cur_index,id)
        if self.edit_dialog.exec_() == QtGui.QDialog.Accepted:
            #梳理返回值
            if Edit.status:
                self.scene.change_table(self.scene.table_cur_index)
            pass
        pass

    def handle_delete(self):
        reply = QtGui.QMessageBox.question(self, 'Message',\
        '你确定要删除吗?', QtGui.QMessageBox.Yes,\
        QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.yes:
            pass
        else:
            pass
        print 'del'
        pass

    def handle_refresh(self):
        print 'refresh'
        pass
    #工具栏处理

    def backgroundButtonGroupClicked(self, button):
        buttons = self.backgroundButtonGroup.buttons()
        for myButton in buttons:
            if myButton != button:
                button.setChecked(False)

        text = button.text()
        my_module_list = {'Project':0,
                          'Bug':1,
                          'Admin':2,
                          'Role':3,
                          'Part':4,
                          'Resume':5,
                          'Positionhr':6,
                          'Buglog':7}
        #acttion触发
        if text == u"项目列表":
            self.scene.change_table(my_module_list['Project'])
        elif text == u"问题列表":
            self.scene.change_table(my_module_list['Bug'])
        elif text == u"用户管理":
            self.scene.change_table(my_module_list['Admin'])
        elif text == u"角色管理":
            self.scene.change_table(my_module_list['Role'])
        elif text == u"部门管理":
            self.scene.change_table(my_module_list['Part'])
        elif text == u"简历列表":
            self.scene.change_table(my_module_list['Resume'])
        elif text == u"招聘管理":
            self.scene.change_table(my_module_list['Positionhr'])
        elif text == u"日志列表":
            self.scene.change_table(my_module_list['Buglog'])
        else:
            pass


        #self.scene.update()
        #self.view.update()

    def deleteItem(self):
        pass


    def pointerGroupClicked(self, i):
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def bringToFront(self):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() >= zValue and isinstance(item, DiagramItem)):
                zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    def sendToBack(self):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if (item.zValue() <= zValue and isinstance(item, DiagramItem)):
                zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)

    def itemInserted(self, item):
        self.pointerTypeGroup.button(DiagramScene.MoveItem).setChecked(True)
        self.scene.setMode(self.pointerTypeGroup.checkedId())
        self.buttonGroup.button(item.diagramType).setChecked(False)

    def textInserted(self, item):
        self.buttonGroup.button(self.InsertTextButton).setChecked(False)
        self.scene.setMode(self.pointerTypeGroup.checkedId())

    def currentFontChanged(self, font):
        self.handleFontChange()

    def fontSizeChanged(self, font):
        self.handleFontChange()

    def sceneScaleChanged(self, scale):
        newScale = scale.left(scale.indexOf("%")).toDouble()[0] / 100.0
        oldMatrix = self.view.matrix()
        self.view.resetMatrix()
        self.view.translate(oldMatrix.dx(), oldMatrix.dy())
        self.view.scale(newScale, newScale)

    def textColorChanged(self):
        self.textAction = self.sender()
        self.fontColorToolButton.setIcon(self.createColorToolButtonIcon(
                    ':/images/textpointer.png',
                    QtGui.QColor(self.textAction.data())))
        self.textButtonTriggered()

    def itemColorChanged(self):
        self.fillAction = self.sender()
        self.fillColorToolButton.setIcon(self.createColorToolButtonIcon(
                    ':/images/floodfill.png',
                    QtGui.QColor(self.fillAction.data())))
        self.fillButtonTriggered()

    def lineColorChanged(self):
        self.lineAction = self.sender()
        self.lineColorToolButton.setIcon(self.createColorToolButtonIcon(
                    ':/images/linecolor.png',
                    QtGui.QColor(self.lineAction.data())))
        self.lineButtonTriggered()

    def textButtonTriggered(self):
        self.scene.setTextColor(QtGui.QColor(self.textAction.data()))

    def fillButtonTriggered(self):
        self.scene.setItemColor(QtGui.QColor(self.fillAction.data()))

    def lineButtonTriggered(self):
        self.scene.setLineColor(QtGui.QColor(self.lineAction.data()))

    def handleSetting(self):
        from jimLib.ui.Setting import Setting
        my_setting = Setting(self)
        my_setting.setupUi(my_setting)
        if my_setting.exec_() == QtGui.QDialog.Accepted:
            pass
        pass

    def handleFontChange(self):
        font = self.fontCombo.currentFont()
        font.setPointSize(self.fontSizeCombo.currentText().toInt()[0])
        if self.boldAction.isChecked():
            font.setWeight(QtGui.QFont.Bold)
        else:
            font.setWeight(QtGui.QFont.Normal)
        font.setItalic(self.italicAction.isChecked())
        font.setUnderline(self.underlineAction.isChecked())

        self.scene.setFont(font)

    def itemSelected(self, item):
        font = item.font()
        color = item.defaultTextColor()
        self.fontCombo.setCurrentFont(font)
        self.fontSizeCombo.setEditText(str(font.pointSize()))
        self.boldAction.setChecked(font.weight() == QtGui.QFont.Bold)
        self.italicAction.setChecked(font.italic())
        self.underlineAction.setChecked(font.underline())

    def about(self):
        QtGui.QMessageBox.about(self, "About Diagram Scene",
                "The <b>Diagram Scene</b> example shows use of the graphics framework.")

    def createToolBox(self):
         self.buttonGroup = QtGui.QButtonGroup()
         self.buttonGroup.setExclusive(False)

         self.backgroundButtonGroup = QtGui.QButtonGroup()
         self.backgroundButtonGroup.buttonClicked.connect(self.backgroundButtonGroupClicked)

         self.toolBox = QtGui.QToolBox()
         self.toolBox.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Ignored))


    def createToolBoxEx(self):
        #查询菜单
         team_label  = {'项目管理':False,'系统管理':False,'简历管理':False,'日志管理':True}
         right_label = {'项目列表':False,'问题列表':False,'用户管理':False,'角色管理':False,'部门管理':False,'岗位管理':False,'简历列表':False,'招聘管理':False,'日志列表':True}

         #查询当前需要设置的权限
         cur_path = os.getcwd()
         my_connector = Db_Connector(cur_path+'/Config.ini')
         cur_team_label = my_connector.get_value_right_team()
         cur_team_label = cur_team_label.split(',')

         cur_right_label = my_connector.get_value_right_lab()
         cur_right_label = cur_right_label.split(',')

         cur_right = my_connector.get_value_right()
         cur_right = cur_right.split(',')

         if 0< len(cur_team_label):
             for item in cur_team_label:
                 if item in team_label:
                     team_label[item] = True

         if 0< len(cur_right_label):
             for item in cur_right_label:
                 if item in right_label:
                     right_label[item] = True

         print team_label
         print right_label
         #查询当前需要设置的权限

         if team_label['项目管理']:
             #########项目管理
             backgroundLayout = QtGui.QGridLayout()
             row = 0
             if right_label['项目列表']:
                backgroundLayout.addWidget(self.createBackgroundCellWidget(u"项目列表",
                        ':/images/background1.png'), row, 0)
                row += 1

             if right_label['问题列表']:
                backgroundLayout.addWidget(self.createBackgroundCellWidget(u"问题列表",
                        ':/images/background2.png'), row, 0)

             backgroundLayout.setRowStretch(2, 10)
             backgroundLayout.setColumnStretch(2, 10)

             backgroundWidget = QtGui.QWidget()
             backgroundWidget.setLayout(backgroundLayout)

             self.toolBox.addItem(backgroundWidget, u"项目管理")
             #########项目管理

         if team_label['系统管理']:
             #########系统管理
             backgroundLayout = QtGui.QGridLayout()
             row = 0
             if right_label['用户管理']:
                backgroundLayout.addWidget(self.createBackgroundCellWidget(u"用户管理",
                        ':/images/background1.png'), row, 0)
                row += 1

             if right_label['角色管理']:
                backgroundLayout.addWidget(self.createBackgroundCellWidget(u"角色管理",
                          ':/images/background2.png'), row, 0)
                row += 1

             if right_label['部门管理']:
                backgroundLayout.addWidget(self.createBackgroundCellWidget(u"部门管理",
                        ':/images/background2.png'), row, 0)

             backgroundLayout.setRowStretch(3, 10)
             backgroundLayout.setColumnStretch(2, 10)

             backgroundWidget = QtGui.QWidget()
             backgroundWidget.setLayout(backgroundLayout)

             self.toolBox.addItem(backgroundWidget, u"系统管理")
             #########系统管理

         if team_label['简历管理']:
             #########日志管理
             backgroundLayout = QtGui.QGridLayout()
             row = 0
             if right_label['简历列表']:
                backgroundLayout.addWidget(self.createBackgroundCellWidget(u"简历列表",
                        ':/images/background1.png'), row, 0)
                row += 1

             if right_label['招聘管理']:
                backgroundLayout.addWidget(self.createBackgroundCellWidget(u"招聘管理",
                        ':/images/background2.png'), row, 0)

             backgroundLayout.setRowStretch(2, 10)
             backgroundLayout.setColumnStretch(2, 10)

             backgroundWidget = QtGui.QWidget()
             backgroundWidget.setLayout(backgroundLayout)

             self.toolBox.addItem(backgroundWidget, u"简历管理")

        #########日志管理
         backgroundLayout = QtGui.QGridLayout()
         backgroundLayout.addWidget(self.createBackgroundCellWidget(u"日志列表",
                    ':/images/background1.png'), 0, 0)

         backgroundLayout.setRowStretch(2, 10)
         backgroundLayout.setColumnStretch(2, 10)

         backgroundWidget = QtGui.QWidget()
         backgroundWidget.setLayout(backgroundLayout)

         self.toolBox.addItem(backgroundWidget, u"日志管理")
         #########日志管理

    def createActions(self):
        self.toFrontAction = QtGui.QAction(
                QtGui.QIcon(':/images/bringtofront.png'), "Bring to &Front",
                self, shortcut="Ctrl+F", statusTip="Bring item to front",
                triggered=self.bringToFront)

        self.sendBackAction = QtGui.QAction(
                QtGui.QIcon(':/images/sendtoback.png'), "Send to &Back", self,
                shortcut="Ctrl+B", statusTip="Send item to back",
                triggered=self.sendToBack)

        self.deleteAction = QtGui.QAction(QtGui.QIcon(':/images/delete.png'),
                "&Delete", self, shortcut="Delete",
                statusTip="Delete item from diagram",
                triggered=self.deleteItem)

        self.exitAction = QtGui.QAction("E&xit", self, shortcut="Ctrl+X",
                statusTip="Quit Scenediagram example", triggered=self.close)

        self.settingAction = QtGui.QAction('S&etting',self, shortcut='Ctrl+S',
                statusTip=u"系统设置",triggered=self.handleSetting)

        self.boldAction = QtGui.QAction(QtGui.QIcon(':/images/bold.png'),
                "Bold", self, checkable=True, shortcut="Ctrl+B",
                triggered=self.handleFontChange)

        self.italicAction = QtGui.QAction(QtGui.QIcon(':/images/italic.png'),
                "Italic", self, checkable=True, shortcut="Ctrl+I",
                triggered=self.handleFontChange)

        self.underlineAction = QtGui.QAction(
                QtGui.QIcon(':/images/underline.png'), "Underline", self,
                checkable=True, shortcut="Ctrl+U",
                triggered=self.handleFontChange)

        self.aboutAction = QtGui.QAction("A&bout", self, shortcut="Ctrl+B",
                triggered=self.about)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.settingAction)
        self.fileMenu.addAction(self.exitAction)

        self.itemMenu = self.menuBar().addMenu("&Item")
        self.itemMenu.addAction(self.deleteAction)
        self.itemMenu.addSeparator()
        self.itemMenu.addAction(self.toFrontAction)
        self.itemMenu.addAction(self.sendBackAction)

        self.aboutMenu = self.menuBar().addMenu("&Help")
        self.aboutMenu.addAction(self.aboutAction)

    def createBackgroundCellWidget(self, text, image):
        button = QtGui.QToolButton()
        button.setText(text)
        button.setIcon(QtGui.QIcon(image))
        button.setIconSize(QtCore.QSize(50, 50))
        button.setCheckable(True)
        self.backgroundButtonGroup.addButton(button)

        layout = QtGui.QGridLayout()
        layout.addWidget(button, 0, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(QtGui.QLabel(text), 1, 0, QtCore.Qt.AlignCenter)

        widget = QtGui.QWidget()
        widget.setLayout(layout)

        return widget

    def createCellWidget(self, text, diagramType):
        item = DiagramItem(diagramType, self.itemMenu)
        icon = QtGui.QIcon(item.image())

        button = QtGui.QToolButton()
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(50, 50))
        button.setCheckable(True)
        self.buttonGroup.addButton(button, diagramType)

        layout = QtGui.QGridLayout()
        layout.addWidget(button, 0, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(QtGui.QLabel(text), 1, 0, QtCore.Qt.AlignCenter)

        widget = QtGui.QWidget()
        widget.setLayout(layout)

        return widget

    def createColorMenu(self, slot, defaultColor):
        colors = [QtCore.Qt.black, QtCore.Qt.white, QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.yellow]
        names = ["black", "white", "red", "blue", "yellow"]

        colorMenu = QtGui.QMenu(self)
        for color, name in zip(colors, names):
            action = QtGui.QAction(self.createColorIcon(color), name, self,
                    triggered=slot)
            action.setData(QtGui.QColor(color))
            colorMenu.addAction(action)
            if color == defaultColor:
                colorMenu.setDefaultAction(action)
        return colorMenu

    def createColorToolButtonIcon(self, imageFile, color):
        pixmap = QtGui.QPixmap(50, 80)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        image = QtGui.QPixmap(imageFile)
        target = QtCore.QRect(0, 0, 50, 60)
        source = QtCore.QRect(0, 0, 42, 42)
        painter.fillRect(QtCore.QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()

        return QtGui.QIcon(pixmap)

    def createColorIcon(self, color):
        pixmap = QtGui.QPixmap(20, 20)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtCore.Qt.NoPen)
        painter.fillRect(QtCore.QRect(0, 0, 20, 20), color)
        painter.end()

        return QtGui.QIcon(pixmap)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.showMaximized()

    sys.exit(app.exec_())

