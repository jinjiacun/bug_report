# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
import notify1

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    #加载托盘
    import itertools, glob
    icons = itertools.cycle(glob.glob('*.ico'))
    hover_text = "SysTrayIcon.py Demo"
    
    def login(sysTrayIcon):
        import login
         #登录界面
        app = QtGui.QApplication(sys.argv)
        form = QtGui.QWidget()
        ui = login.Ui_login()
        ui.setupUi(form)
        form.show()
        sys.exit(app.exec_())
        
    def message():
        sys.exit()
    
        
    def simon(sysTrayIcon): print "Hello Simon."
    def switch_icon(sysTrayIcon):
        sysTrayIcon.icon = icons.next()
        sysTrayIcon.refresh_icon()
        
    menu_options = ((u'登录', icons.next(), login),
                    (u'消息', icons.next(), message)
                    #('Switch Icon', None, switch_icon),
                   # ('A sub-menu', icons.next(), (('Say Hello to Simon', icons.next(), simon),
                   #                               ('Switch Icon', icons.next(), switch_icon),
                   #                              ))
                   )
    def bye(sysTrayIcon): print 'Bye, then.'
    
    notify1.SysTrayIcon(icons.next(), hover_text, menu_options, on_quit=bye, default_menu_index=1)
