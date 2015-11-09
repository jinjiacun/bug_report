#coding=utf-8
import sys
from PyQt4 import QtGui,QtCore
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.resize(250,150)
        self.setWindowTitle('toolbar')
        self.exit=QtGui.QAction(u'退出',self)
        self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.exit)

        #新增
        self.add = QtGui.QAction(u'新增',self)
        self.connect(self.add, QtCore.SIGNAL('triggered()'), self.handle_add)
        self.toolbar.addAction(self.add)

    def handle_add(self):
        print 'add'

    def handle_delete(self):
        print 'delete'


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())