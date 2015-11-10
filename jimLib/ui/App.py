# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

import math
import os
from jimLib.ui.List import MyDialog
from PyQt4 import QtCore, QtGui
import jimLib.ui.Add

try:
    import diagramscene_rc3
except ImportError:
    import diagramscene_rc2


class Arrow(QtGui.QGraphicsLineItem):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        super(Arrow, self).__init__(parent, scene)

        self.arrowHead = QtGui.QPolygonF()

        self.myStartItem = startItem
        self.myEndItem = endItem
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.myColor = QtCore.Qt.black
        self.setPen(QtGui.QPen(self.myColor, 2, QtCore.Qt.SolidLine,
                QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

    def setColor(self, color):
        self.myColor = color

    def startItem(self):
        return self.myStartItem

    def endItem(self):
        return self.myEndItem

    def boundingRect(self):
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return QtCore.QRectF(p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)

    def shape(self):
        path = super(Arrow, self).shape()
        path.addPolygon(self.arrowHead)
        return path

    def updatePosition(self):
        line = QtCore.QLineF(self.mapFromItem(self.myStartItem, 0, 0), self.mapFromItem(self.myEndItem, 0, 0))
        self.setLine(line)

    def paint(self, painter, option, widget=None):
        if (self.myStartItem.collidesWithItem(self.myEndItem)):
            return

        myStartItem = self.myStartItem
        myEndItem = self.myEndItem
        myColor = self.myColor
        myPen = self.pen()
        myPen.setColor(self.myColor)
        arrowSize = 20.0
        painter.setPen(myPen)
        painter.setBrush(self.myColor)

        centerLine = QtCore.QLineF(myStartItem.pos(), myEndItem.pos())
        endPolygon = myEndItem.polygon()
        p1 = endPolygon.first() + myEndItem.pos()

        intersectPoint = QtCore.QPointF()
        for i in endPolygon:
            p2 = i + myEndItem.pos()
            polyLine = QtCore.QLineF(p1, p2)
            intersectType = polyLine.intersect(centerLine, intersectPoint)
            if intersectType == QtCore.QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QtCore.QLineF(intersectPoint, myStartItem.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrowP1 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = line.p1() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)

        self.arrowHead.clear()
        for point in [line.p1(), arrowP1, arrowP2]:
            self.arrowHead.append(point)

        painter.drawLine(line)
        painter.drawPolygon(self.arrowHead)
        if self.isSelected():
            painter.setPen(QtGui.QPen(myColor, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            myLine.translate(0, 4.0)
            painter.drawLine(myLine)
            myLine.translate(0,-8.0)
            painter.drawLine(myLine)


class DiagramTextItem(QtGui.QGraphicsTextItem):
    lostFocus = QtCore.pyqtSignal(QtGui.QGraphicsTextItem)

    selectedChange = QtCore.pyqtSignal(QtGui.QGraphicsItem)

    def __init__(self, parent=None, scene=None):
        super(DiagramTextItem, self).__init__(parent, scene)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            self.selectedChange.emit(self)
        return value

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lostFocus.emit(self)
        super(DiagramTextItem, self).focusOutEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == QtCore.Qt.NoTextInteraction:
            self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        super(DiagramTextItem, self).mouseDoubleClickEvent(event)


class DiagramItem(QtGui.QGraphicsPolygonItem):
    Step, Conditional, StartEnd, Io = range(4)

    def __init__(self, diagramType, contextMenu, parent=None, scene=None):
        super(DiagramItem, self).__init__(parent, scene)

        self.arrows = []

        self.diagramType = diagramType
        self.contextMenu = contextMenu

        path = QtGui.QPainterPath()
        if self.diagramType == self.StartEnd:
            path.moveTo(200, 50)
            path.arcTo(150, 0, 50, 50, 0, 90)
            path.arcTo(50, 0, 50, 50, 90, 90)
            path.arcTo(50, 50, 50, 50, 180, 90)
            path.arcTo(150, 50, 50, 50, 270, 90)
            path.lineTo(200, 25)
            self.myPolygon = path.toFillPolygon()
        elif self.diagramType == self.Conditional:
            self.myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(-100, 0), QtCore.QPointF(0, 100),
                    QtCore.QPointF(100, 0), QtCore.QPointF(0, -100),
                    QtCore.QPointF(-100, 0)])
        elif self.diagramType == self.Step:
            self.myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(-100, -100), QtCore.QPointF(100, -100),
                    QtCore.QPointF(100, 100), QtCore.QPointF(-100, 100),
                    QtCore.QPointF(-100, -100)])
        else:
            self.myPolygon = QtGui.QPolygonF([
                    QtCore.QPointF(-120, -80), QtCore.QPointF(-70, 80),
                    QtCore.QPointF(120, 80), QtCore.QPointF(70, -80),
                    QtCore.QPointF(-120, -80)])

        self.setPolygon(self.myPolygon)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

    def removeArrow(self, arrow):
        try:
            self.arrows.remove(arrow)
        except ValueError:
            pass

    def removeArrows(self):
        for arrow in self.arrows[:]:
            arrow.startItem().removeArrow(arrow)
            arrow.endItem().removeArrow(arrow)
            self.scene().removeItem(arrow)

    def addArrow(self, arrow):
        self.arrows.append(arrow)

    def image(self):
        pixmap = QtGui.QPixmap(250, 250)
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 8))
        painter.translate(125, 125)
        painter.drawPolyline(self.myPolygon)
        return pixmap

    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        #self.myContextMenu.exec_(event.screenPos())

    def itemChange(self, change, value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            for arrow in self.arrows:
                arrow.updatePosition()

        return value


class DiagramScene(QtGui.QGraphicsScene):
    InsertItem, InsertLine, InsertText, MoveItem  = range(4)

    itemInserted = QtCore.pyqtSignal(DiagramItem)

    textInserted = QtCore.pyqtSignal(QtGui.QGraphicsTextItem)

    itemSelected = QtCore.pyqtSignal(QtGui.QGraphicsItem)

    def __init__(self, itemMenu, parent=None):
        super(DiagramScene, self).__init__(parent)

        self.myItemMenu = itemMenu
        self.myMode = self.MoveItem
        self.myItemType = DiagramItem.Step
        self.line = None
        self.textItem = None
        self.myItemColor = QtCore.Qt.white
        self.myTextColor = QtCore.Qt.black
        self.myLineColor = QtCore.Qt.black
        self.myFont = QtGui.QFont()

    def setLineColor(self, color):
        self.myLineColor = color
        if self.isItemChange(Arrow):
            item = self.selectedItems()[0]
            item.setColor(self.myLineColor)
            self.update()

    def setTextColor(self, color):
        self.myTextColor = color
        if self.isItemChange(DiagramTextItem):
            item = self.selectedItems()[0]
            item.setDefaultTextColor(self.myTextColor)

    def setItemColor(self, color):
        self.myItemColor = color
        if self.isItemChange(DiagramItem):
            item = self.selectedItems()[0]
            item.setBrush(self.myItemColor)

    def setFont(self, font):
        self.myFont = font
        if self.isItemChange(DiagramTextItem):
            item = self.selectedItems()[0]
            item.setFont(self.myFont)

    def setMode(self, mode):
        self.myMode = mode

    def setItemType(self, type):
        self.myItemType = type

    def editorLostFocus(self, item):
        cursor = item.textCursor()
        cursor.clearSelection()
        item.setTextCursor(cursor)

        if item.toPlainText():
            self.removeItem(item)
            item.deleteLater()

    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != QtCore.Qt.LeftButton):
            return

        if self.myMode == self.InsertItem:
            item = DiagramItem(self.myItemType, self.myItemMenu)
            item.setBrush(self.myItemColor)
            self.addItem(item)
            item.setPos(mouseEvent.scenePos())
            self.itemInserted.emit(item)
        elif self.myMode == self.InsertLine:
            self.line = QtGui.QGraphicsLineItem(QtCore.QLineF(mouseEvent.scenePos(),
                                        mouseEvent.scenePos()))
            self.line.setPen(QtGui.QPen(self.myLineColor, 2))
            self.addItem(self.line)
        elif self.myMode == self.InsertText:
            textItem = DiagramTextItem()
            textItem.setFont(self.myFont)
            textItem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            textItem.setZValue(1000.0)
            textItem.lostFocus.connect(self.editorLostFocus)
            textItem.selectedChange.connect(self.itemSelected)
            self.addItem(textItem)
            textItem.setDefaultTextColor(self.myTextColor)
            textItem.setPos(mouseEvent.scenePos())
            self.textInserted.emit(textItem)

        super(DiagramScene, self).mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        if self.myMode == self.InsertLine and self.line:
            newLine = QtCore.QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(newLine)
        elif self.myMode == self.MoveItem:
            super(DiagramScene, self).mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        if self.line and self.myMode == self.InsertLine:
            startItems = self.items(self.line.line().p1())
            if len(startItems) and startItems[0] == self.line:
                startItems.pop(0)
            endItems = self.items(self.line.line().p2())
            if len(endItems) and endItems[0] == self.line:
                endItems.pop(0)

            self.removeItem(self.line)
            self.line = None

            if len(startItems) and len(endItems) and \
                    isinstance(startItems[0], DiagramItem) and \
                    isinstance(endItems[0], DiagramItem) and \
                    startItems[0] != endItems[0]:
                startItem = startItems[0]
                endItem = endItems[0]
                arrow = Arrow(startItem, endItem)
                arrow.setColor(self.myLineColor)
                startItem.addArrow(arrow)
                endItem.addArrow(arrow)
                arrow.setZValue(-1000.0)
                self.addItem(arrow)
                arrow.updatePosition()

        self.line = None
        super(DiagramScene, self).mouseReleaseEvent(mouseEvent)

    def isItemChange(self, type):
        for item in self.selectedItems():
            if isinstance(item, type):
                return True
        return False


class MainWindow(QtGui.QMainWindow):
    InsertTextButton = 10

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

        #托盘
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        icon_path = os.getcwd()
        icon = QtGui.QIcon(os.path.join(icon_path+'./images/un_load.png'))
        self.trayIcon.setIcon(icon)
        self.trayIcon.show()

        layout.addWidget(self.scene)

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


    #工具栏处理
    def handle_add(self):
        self.add_dialog = jimLib.ui.Add.Add()
        self.add_dialog.exec_()
        pass

    def handle_edit(self):
        print 'edit'
        pass

    def handle_delete(self):
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
        #acttion触发
        if text == u"项目列表":
            self.scene.change_table('Project')
        elif text == u"问题列表":
            self.scene.change_table('Bug')
        elif text == u"用户管理":
            self.scene.change_table('Admin')
        elif text == u"角色管理":
            self.scene.change_table('Role')
        elif text == u"部门管理":
            self.scene.change_table('Part')
        elif text == u"简历列表":
            self.scene.change_table('Resume')
        elif text == u"招聘管理":
            self.scene.change_table('Positionhr')
        elif text == u"日志列表":
            self.scene.change_table('Buglog')
        else:
            pass


        #self.scene.update()
        #self.view.update()

    def deleteItem(self):
        for item in self.scene.selectedItems():
            if isinstance(item, DiagramItem):
                item.removeArrows()
            self.scene.removeItem(item)

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

         #########项目管理
         self.backgroundButtonGroup = QtGui.QButtonGroup()
         self.backgroundButtonGroup.buttonClicked.connect(self.backgroundButtonGroupClicked)

         backgroundLayout = QtGui.QGridLayout()
         backgroundLayout.addWidget(self.createBackgroundCellWidget(u"项目列表",
                ':/images/background1.png'), 0, 0)
         backgroundLayout.addWidget(self.createBackgroundCellWidget(u"问题列表",
                ':/images/background2.png'), 1, 0)

         backgroundLayout.setRowStretch(2, 10)
         backgroundLayout.setColumnStretch(2, 10)

         backgroundWidget = QtGui.QWidget()
         backgroundWidget.setLayout(backgroundLayout)

         self.toolBox = QtGui.QToolBox()
         self.toolBox.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Ignored))
         self.toolBox.addItem(backgroundWidget, u"项目管理")
         #########项目管理

         #########系统管理
         #self.backgroundButtonGroup = QtGui.QButtonGroup()
         #self.backgroundButtonGroup.buttonClicked.connect(self.backgroundButtonGroupClicked)

         backgroundLayout = QtGui.QGridLayout()
         backgroundLayout.addWidget(self.createBackgroundCellWidget(u"用户管理",
                ':/images/background1.png'), 0, 0)
         backgroundLayout.addWidget(self.createBackgroundCellWidget(u"角色管理",
                ':/images/background2.png'), 1, 0)
         backgroundLayout.addWidget(self.createBackgroundCellWidget(u"部门管理",
                ':/images/background2.png'), 2, 0)

         backgroundLayout.setRowStretch(3, 10)
         backgroundLayout.setColumnStretch(2, 10)

         backgroundWidget = QtGui.QWidget()
         backgroundWidget.setLayout(backgroundLayout)

         self.toolBox.addItem(backgroundWidget, u"系统管理")
         #########系统管理
         backgroundLayout = QtGui.QGridLayout()
         backgroundLayout.addWidget(self.createBackgroundCellWidget(u"简历列表",
                ':/images/background1.png'), 0, 0)
         backgroundLayout.addWidget(self.createBackgroundCellWidget(u"招聘管理",
                ':/images/background2.png'), 1, 0)

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

