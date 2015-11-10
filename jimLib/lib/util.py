# -*- coding: utf-8 -*-
import urllib2
import urllib
import json
import sys
import time

#post模拟提交数据
def lib_post(method,content):
    data = {}
    data['method'] = method
    data['content'] = content
    data['token']   = '123'
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

#日志文件
def lib_log():
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
    elif 4 == type:
        return my_dict['role'][str(value)]
    elif 5 == type:
        return my_dict['project'][str(value)]
    elif 6 == type:
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
