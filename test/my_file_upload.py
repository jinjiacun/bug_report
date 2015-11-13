from jimLib.lib.util import lib_post_file
from jimLib.lib.util import file_extension
import sys

if __name__ == '__main__':
    method = 'Media.upload'
    path = r'F:\PHPnow-1.5.6\htdocs\Prentice.Hall.Rapid.GUI.Programming.with.Python.and.Qt.the.definitive.guide.to.PyQt.programming.2008.pdf'
    f_ext = file_extension(path)
    f_ext = f_ext.replace('.','')
    content = "{'field_name':'my','file_name':'normal','file_ext':'%s','module_sn':'011001'}"%f_ext

    print lib_post_file(method,content,path)
    pass
