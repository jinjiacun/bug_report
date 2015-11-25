# -*- coding: utf-8 -*-
import urllib2
import urllib
import json
import sys
import time
import re
from htmlentitydefs import entitydefs

#post模拟提交数据
def lib_post(method,content):
    data = {}
    data['method'] = method
    data['content'] = content
    data['token']   = '123'
    data['debug']   = 1
    url = 'http://192.168.1.131/yms_api/index.php/Bugapi'
    post_data = urllib.urlencode(data)
    req = urllib2.urlopen(url, post_data)
    content = req.read()
    print content
    try:
        result = json.loads(content)
    except:
        print 'json error'
        sys.exit()
    return result

#post上传文件
def lib_post_file(method, content,debug,path):
    path = unicode(path,"utf-8")
    #buld post body data
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'username')
    data.append('jack')
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'mobile')
    data.append('13800138000')
    data.append('--%s' % boundary)

    #fr=open(r'F:\PHPnow-1.5.6\htdocs\jim_project\bug_report\images\normal.png','rb')
    fr=open(path,'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename="my"' % 'my')
    data.append('Content-Type: %s\r\n' % 'image/png')
    data.append(fr.read())
    fr.close()
    data.append('--%s--\r\n' % boundary)

    #http_url="http://192.168.1.131/yms_api/index.php/Bugapi?method=Media.upload&content={'field_name':'my','file_name':'normal','file_ext':'png','module_sn':'011001'}"
    http_url="http://192.168.1.131/yms_api/index.php/Bugapi?method=%s&content=%s&debug=%d"%(method,content,debug)
    http_body='\r\n'.join(data)
    try:
        #buld http request
        req=urllib2.Request(http_url, data=http_body)
        #header
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        req.add_header('User-Agent','Mozilla/5.0')
        req.add_header('Referer','http://192.168.1.131/')
        #post data to server
        resp = urllib2.urlopen(req, timeout=5)
        #get response
        qrcont=resp.read()
        return (True,json.loads(qrcont))
    except Exception,e:
        print e.message
        return (False,'http error')
    return (False,u'错误')


#上传剪切板图片
def upload_clipboard_pic():
    #path = r'F:\PHPnow-1.5.6\htdocs\jim_project\bug_report\images\error.png'
    cur_dir = os.getcwd()
    path = cur_dir+'/clipboard.png'
    #buld post body data
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'username')
    data.append('jack')
    data.append('--%s' % boundary)

    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'mobile')
    data.append('13800138000')
    data.append('--%s' % boundary)

    #fr=open(r'F:\PHPnow-1.5.6\htdocs\jim_project\bug_report\images\normal.png','rb')
    fr=open(path,'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ('upfile','upfile.png'))
    data.append('Content-Type: %s\r\n' % 'image/png')
    data.append(fr.read())
    fr.close()
    data.append('--%s--\r\n' % boundary)

    #http_url="http://192.168.1.131/yms_api/index.php/Bugapi?method=Media.upload&content={'field_name':'my','file_name':'normal','file_ext':'png','module_sn':'011001'}"
    http_url="http://192.168.1.131/bug/Public/ueditor/php/controller.php?action=uploadimage"
    http_body='\r\n'.join(data)
    try:
        #buld http request
        req=urllib2.Request(http_url, data=http_body)
        #header
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
        req.add_header('User-Agent','Mozilla/5.0')
        req.add_header('Referer','http://192.168.1.131/')
        #post data to server
        resp = urllib2.urlopen(req, timeout=5)
        #get response
        qrcont=resp.read()
        print qrcont
        return (True,json.loads(qrcont))
    except Exception,e:
        print e.message
        return (False,'http error')
    return (False,u'错误')

#保存剪切板图片
def save_clipboard_image():
    from  PythonMagick import Image
    try:
        Image('clipboard:').write("PNG32:clipboard.png")
    except:
        print 'except'
    '''
    im = ImageGrab.grabclipboard()
    im.save('somefile.png','PNG')
    '''
    pass


#文件下载
def file_down(url,path):
    print "downloading with urllib2"
    #url = 'http://www.pythontab.com/test/demo.zip'
    f = urllib2.urlopen(url)
    data = f.read()
    #with open("demo2.zip", "wb") as code:
    with open(path, "wb") as code:
        code.write(data)
    print 'down file finish'
    pass

import os.path
#获取文件后缀名
def file_extension(path):
  return os.path.splitext(path)[1]
  #return path[path.rfind('.'):]

#日志文件
def lib_log(type,message):
    return null

#unix时间戳格式化显示
def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

#自定义格式化
'''
0-数字,
1-字符串
2-日期
3-人员
4-角色
5-项目
6-模块
7-优先级
8-bug状态
9-部门
10-用户状态
11-资源替换
12-人事岗位
13-简历进度
14-base64解码
'''
def lib_format(type, value,my_dict):
    if 0 == type:
        return "%d"%value
    elif 1 == type:
        return "%s"%value
    elif 2 == type:
        if 0 == value:
            return '----'
        else:
            return timestamp_datetime(value)
    elif 3 == type:
        if 0 == value:
            return '----'
        else:
            try:
                return my_dict['admin'][str(value)]
            except:
                return '----'
    elif 4 == type and my_dict.has_key('role'):
        return my_dict['role'][str(value)]
    elif 5 == type and my_dict.has_key('project'):
        return my_dict['project'][str(value)]
    elif 6 == type and my_dict.has_key('mod'):
        return my_dict['mod'][str(value)]
    elif 7 == type:
        if str(1) == str(value):
            return u'超高'
        elif str(2) == str(value):
            return u'高'
        elif str(3) == str(value):
            return u'一般'
    elif 8 == type:
        if str(1) == str(value):
            return u'待解决'
        elif str(2) == str(value):
            return u'已解决'
        elif str(3) == str(value):
            return u'已关闭'
    elif 9 == type:
        if 0 == value:
            return '----'
        try:
            return my_dict['part'][str(value)]
        except:
            return '----'
    elif 10 == type:
        if str(0) == str(value):
            return u"正常"
        elif str(1) == str(value):
            return u'禁用'
    elif 11 == type:
        tmp = str(value)
        tmp = tmp.replace('1',u'项目列表')
        tmp = tmp.replace('2',u'项目列表')
        tmp = tmp.replace('3',u'问题列表')
        tmp = tmp.replace('4',u'问题列表')
        tmp = tmp.replace('5',u'用户管理')
        tmp = tmp.replace('6',u'角色管理')
        tmp = tmp.replace('7',u'部门管理')
        tmp = tmp.replace('8',u'岗位管理')
        tmp = tmp.replace('9',u'简历列表')
        tmp = tmp.replace('10',u'简历列表')
        tmp = tmp.replace('11',u'招聘管理')
        return tmp
    elif 12 == type:
        if 0 == value:
            return '----'
        try:
            return my_dict['positionhr'][str(value)]
        except:
            return '----'
    elif 13 == type:
        if 1 == value:
            return u'未筛选'
        elif 2 == value:
            return u'未预约'
        elif 3 == value:
            return u'已预约'
        elif 4 == value:
            return u'面试'
        elif 5 == value:
            return u'复试'
        elif 6 == value:
            return u'入职'
        elif 7 == value:
            return u'废弃'
    elif 14 == type:
       return htmlspecialchars_decode(decode_base64(value))
    return value

import base64
def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'='* missing_padding
    return base64.decodestring(data)


import re
try:
    from htmlentitydefs import entitydefs
except ImportError:  # Python 3
    from html.entities import entitydefs


def htmlspecialchars_decode_func(m, defs=entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)  # use as is


def htmlspecialchars_decode(string):
    pattern = re.compile("&(\w+?);")
    return pattern.sub(htmlspecialchars_decode_func, string)

#我的字典
class Dict():
    #项目列表
    title_list  = [u'添加项目',u'添加bug',u'添加用户',u'添加角色',u'添加部门',u'添加简历',u'添加招聘']
    module_list = ['Project' ,'Bug'      ,'Admin'    ,'Role'     ,'Part'     ,'Resume'   ,'Positionhr']
    prefix_list = ['XM-'     ,'WT-','YH-'  ,'JS-' ,'BM-' ,'JL-'    ,''        ]
    name_list = []
    number_prefix_list = []
    def __init__(self):
        pass

#获取当前用户id
def get_cur_admin_id():
    pass
    return 1

def htmlspecialchars_decode_func(m, defs=entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)  # use as is


def htmlspecialchars_decode(string):
    pattern = re.compile("&(\w+?);")
    return pattern.sub(htmlspecialchars_decode_func, string)

if __name__ == '__main__':
    #test post
    '''
    method = 'admin.login'
    content = {'admin_name':'admin','passwd':'admin'}
    if lib_post(method, content):
        print 'success'
    else:
        print 'fail'
    '''
    #test post
    #upload_clipboard_pic()

    save_clipboard_image()
    upload_clipboard_pic()