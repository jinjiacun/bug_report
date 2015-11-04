#!/usr/bin/env python
import os, sys
import win32api,win32con

'''
class AutoTask(object):
    def __init__(self,path):
        self.path = path
        
    def work(self):
        runpath = 'Software\Microsoft\Windows\CurrentVersion\Run'
        hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_SET_VALUE)
        print hKey
        path = os.path.abspath(self.path)
        print path
        if False == os.path.isfile(path):
            return False
        (filepath, filename) = os.path.split(path)
        win32api.RegSetValueEx(hKey, filename, 0, win32con.REG_SZ, path)
        win32api.RegCloseKey(hKey)
        return True
'''

class AutoTask(object):
    def __init__(self, path):
        self.path = path

    def work(self):
        runpath = 'Software\Microsoft\Windows\CurrentVersion\Run'
        hKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, runpath, 0, win32con.KEY_SET_VALUE)
        path = os.path.abspath(self.path)
        print path
        if False == os.path.isfile(path):
            return False
        (filepath, filename) = os.path.split(path)
        win32api.RegSetValueEx(hKey, filename, 0, win32con.REG_SZ, path)
        win32api.RegCloseKey(hKey)
        return True