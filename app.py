# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

try:
    import diagramscene_rc3
except ImportError:
    import diagramscene_rc2

from PyQt4 import QtGui
from jimLib.ui.App import MainWindow

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 500)
    mainWindow.showMaximized()

    sys.exit(app.exec_())
