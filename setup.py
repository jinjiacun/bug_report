#-*-coding: UTF-8-*-
from distutils.core import setup
import py2exe
import os
# Powered by ***
INCLUDES = ["sip","PyQt4._qt","sys","decimal","PyQt4.QtSvg"]
my_data_files = [('images',[r'images/error.png',
                            r'images/normal.png',
                            r'images/un_load.png',
                            r'images/warn_red.png',
                            r'images/warn_yellow.png'])]
dlllist = [ "MSVCP90.dll", "mswsock.dll", "powrprof.dll","w9xpopen.exe","qsvg4.dll","qsvgicon4.dll"]
origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    if os.path.basename(pathname).lower() in dlllist:
        return 0
    return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL
options = {"py2exe" :  
    {"compressed" : 1,  
     "optimize" : 2,  
     "bundle_files" : 2,  
     "includes" : INCLUDES,  
     "dll_excludes":dlllist}}  
setup(
    options = options, 
    description = "bug管理系统",  
    zipfile=None,
    data_files=my_data_files,
    windows=[{"script": "systray.pyw", "icon_resources": [(1, "s.ico")]}],
    )

