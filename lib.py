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