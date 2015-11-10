# -*- coding: utf-8 -*-
#!/usr/bin/env python
from jimLib.lib.util import lib_post
import urllib

class business():
    def __init__(self):
        pass

    #登录
    def login(self,user_name='',passwd=''):
        if ''==user_name or '' == passwd:
            return ('',False)

        method = 'Admin.login'
        content = {'admin_name':urllib.quote(user_name),'passwd':urllib.quote(passwd)}
        result  = lib_post(method, content)
        if 500 == result['status_code']:
            return (result['content'],False)
        if 200 == result['status_code'] and 1 == result['content']['is_success']:
            return ('成功登录',True)

        return ('用户名或者密码错误!',False)

    #接受消息
    def receive_message(self,messge=''):
        pass

    #查询项目

    #查询bug

    #查询
