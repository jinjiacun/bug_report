# -*- coding: utf-8 -*-
#!/usr/bin/env python
from jimLib.lib.util import lib_post
import urllib
from jimLib.lib.util import Dict
from jimLib.lib.util import lib_log
from jimLib.lib.util import lib_post_file
from jimLib.lib.util import file_extension

class business():
    def __init__(self):
        pass

    #登录
    def login(self,user_name='',passwd=''):
        if ''==user_name or '' == passwd:
            return ('',False,0)

        method = 'Admin.login'
        content = {'admin_name':urllib.quote(user_name.encode('utf-8')),'passwd':urllib.quote(passwd.encode('utf-8'))}
        result  = lib_post(method, content)
        if 500 == result['status_code']:
            return (result['content'],False,0)
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            admin_id = result['content']['id']
            role_id  = result['content']['role_id']
            part_id  = result['content']['part_id']
            return (u'成功登录',True,admin_id,role_id,part_id)

        return (u'用户名或者密码错误!',False,0)

    #查询属于当前用户的bug
    '''
    return status,is_success,message
           500,,参数错误
           200,0,严重错误
           200,1,一般错误
           200,-1,没有错误
           其他查询失败
    '''
    def get_my_bug(self,admin_id=0):
        if 0 == admin_id:
            return (500,None,u'参数不正确')

        method = 'Bug.get_self_bug'
        content = {'admin_id':urllib.quote(admin_id.encode('utf-8'))}
        result = lib_post(method, content)
        if 500 == result['status_code']:
            return (500,None,result['content'])
        elif 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (200,0,u'严重错误')
        elif 200 == result['status_code'] and 1 == result['content']['is_success']:
            return (200,1,u'一般错误')
        elif 200 == result['status_code'] and -1 == result['content']['is_success']:
            return (200,-1,u'没有错误')
        else:
            return (200,None,u'查询失败')

        pass

    #接受消息
    def receive_message(self,messge=''):
        pass

    #-----------------------添加-----------------------
    #添加项目
    '''data={'number':'','name':'','description':'','create':0}
       mem_data={'project_id':0,'admin_id':[]}
       mod_data={'project_id':0,'name':[]}
   '''
    def add_proejct(self,data={},mem_data={},mod_data={}):
        project_id = 0
        #添加项目
        method = 'Project.add'
        content = data
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            project_id = result['content']['id']
        else:
            return (False,u'项目添加失败')


        #添加项目成员
        #{'project_id':0,'admin_id':0}
        if 0<len(mem_data['admin_id']):
            for admin_id in mem_data['admin_id']:
                method = 'Projectmem.add'
                content = {'project_id':project_id,'admin_id':admin_id}
                result = lib_post(method,content)
                if 500 == result['status_code']:
                    return (False,result['content'])
                if 200 == result['status_code'] and 0 == result['content']['is_success']:
                    pass
                else:
                    return (False,u'添加项目成员失败')


        #添加项目模块
        if 0<len(mod_data['name']):
            for name in mod_data['name']:
                mod_data['project_id'] = project_id
                method  = 'Projectmodule.add'
                content = {'project_id':project_id,'name':name}
                result = lib_post(method, content)
                if 500 == result['status_code']:
                    return (False,result['content'])
                if 200 == result['status_code'] and 0 == result['content']['is_success']:
                    pass
                else:
                    return (False,u'添加项目模块失败')

        return (True,u'添加成功')

    #添加bug
    '''data={'number':'','title':'','level':0,'status':0,'project_id':0,'project_mod_id':0,
            'get_member':0,'description':'','put_member':0}
    '''
    def add_bug(self,data={}):
        method = 'Bug.add'
        content = data
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'添加成功')

        return (False,u'添加失败')


    #添加用户
    '''data={'number':0,'admin_name':'','passwd':'','name':'','status':0,'part':0,'role':0}
    '''
    def add_admin(self,data={}):
        method = 'Admin.add'
        content = data
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'添加成功')

        return (False,u'添加失败')

    #添加角色
    '''data={'number':0,'name':'','resource':''}
    '''
    def add_role(self,data={}):
        method = 'Role.add'
        content = data
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'添加成功')

        return (False,u'添加失败')

    #添加部门
    '''data={'number':'','name':'','create':0}
    '''
    def add_part(self,data={}):
        method = 'Part.add'
        content = data
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'添加成功')

        return (False,u'添加失败')

    #添加简历
    '''data={'number':'','candidates':'','telephone':'','position_id':0,'part_id':0,
            'accessories':0,'remartk':'','create':0}
    '''
    def add_resume(self,data={}):
        method = 'Resume.add'
        content = data
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'添加成功')

        return (False,u'添加失败')

    #添加简历岗位
    '''data={'part_id':0,'name':'','status':0,'description':'','start_time':0,'create':0}
    '''
    def add_positionhr(self,data={}):
        method = 'Positionhr.add'
        content = data
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'添加成功')

        return (False,u'添加失败')

    #上传文件
    '''
    '''
    def file_upload(self,path=''):
        method = 'Media.upload'
        f_ext = file_extension(path)
        f_ext = f_ext.replace('.','')
        content = "{'field_name':'my','file_name':'normal','file_ext':'%s','module_sn':'011001'}"%f_ext
        debug = 1
        (status,content) = lib_post_file(method,content,debug,path)
        if status:
            return (True,content)
        return (False, content)

    #-----------------------查询一条信息-----------------------
    #查询项目
    def get_project_one_by_id(self,id=0):
        method = 'Project.get_info'
        content={'id':id}
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询异常')
        if 200 == result['status_code']:
            return (True,result['content'])

        return (False,u'查询失败')

    #查询项目成员
    def get_project_mem_by_project_id(self,project_id=0):
        method = 'Projectmem.get_list'
        content={'where':{'project_id':project_id}}
        re_list = []
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询失败')
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0< result['content']['record_count']:
            rows = int(str(result['content']['record_count']))
            for row in range(0,rows):
                re_list.append(result['content']['list'][row]['admin_id'])
            return (True,re_list)
        return (False,[])

    #查询项目模块
    def get_project_mod_by_project_id(self,project_id=0):
        method = 'Projectmodule.get_list'
        content={'where':{'project_id':project_id}}
        re_list = {}
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询失败')
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0< result['content']['record_count']:
            rows = int(str(result['content']['record_count']))
            for row in range(0,rows):
                key = str(result['content']['list'][row]['name'])
                id = result['content']['list'][row]['id']
                re_list[key] = id
            return (True,re_list)
        return (False,{})
        pass

    def get_project_mod_name_by_project_id(self,project_id=0):
        method = 'Projectmodule.get_list'
        content = {'where':{'project_id':project_id}}
        re_list = []
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询失败')
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0<result['content']['record_count']:
            rows = int(str(result['content']['record_count']))
            for row in (0,rows-1):
                re_list.append(result['content']['list'][row]['name'])
        return (True,re_list)


    #查询bug
    def get_bug_one_by_id(self,id):
        method = 'Bug.get_info'
        content={'id':id}
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询异常')
        if 200 == result['status_code']:
            return (True,result['content'])

        return (False,u'查询失败')

    #查询用户
    def get_admin_one_by_id(self,id):
        method = 'Admin.get_info'
        content={'id':id}
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询异常')
        if 200 == result['status_code']:
            return (True,result['content'])

        return (False,u'查询失败')

    #查询角色
    def get_role_one_by_id(self,id):
        method = 'Role.get_info'
        content={'id':id}
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询异常')
        if 200 == result['status_code']:
            return (True,result['content'])

        return (False,u'查询失败')

    #查询部门
    def get_part_one_by_id(self,id):
        method = 'Part.get_info'
        content={'id':id}
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询异常')
        if 200 == result['status_code']:
            return (True,result['content'])

        return (False,u'查询失败')

    #查询简历
    def get_resume_one_by_id(self,id):
        method = 'Resume.get_info'
        content={'id':id}
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询异常')
        if 200 == result['status_code']:
            return (True,result['content'])

        return (False,u'查询失败')

    #查询招聘岗位
    def get_positionhr_one_by_id(self,id):
        method = 'Positionhr.get_info'
        content={'id':id}
        try:
            result = lib_post(method,content)
        except:
            return (False,u'查询异常')
        if 200 == result['status_code']:
            return (True,result['content'])

        return (False,u'查询失败')

    #-----------------------修改:begin-----------------------
    #更新项目
    '''
    data={'number':'','name':'','description':'','create':0}
    where={'id':0}
    mem_data={'project_id':0,'admin_id':[]}
    mod_data={'project_id':0,'name':[]}
    '''
    def update_project(self,data={},where={},mem_data={},mod_data={}):
        method = 'Project.update'
        content = {}
        content['data'] = data
        content['where'] = where
        try:
            result = lib_post(method,content)
        except:
            return (False,u'更新异常')

        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            pass
        else:
            return (False,u'修改项目失败')
        #    return (True,u'成功修改')

        #检查项目成员
        ##查询旧的项目成员数据
        status,old_project_mem = self.get_project_mem_by_project_id(mem_data['project_id'])
        if status:
            #获取新旧列表的交集,此集合为不变元素
            inersection = list(set(mem_data['admin_id']).intersection(set(old_project_mem)))
            #获取旧集合和交集的差集(所得结果删除的项目成员)
            need_delete = list(set(old_project_mem).difference(set(inersection)))
            #调用删除
            if 0 < len(need_delete):
                if 1 == len(need_delete):
                    where_str = str(need_delete[0])
                else:
                    tmp_list = need_delete
                    need_delete = []
                    for item in tmp_list:
                        need_delete.append(str(item))
                    where_str = ','.join(need_delete)
                method = 'Projectmem.delete'
                content={'admin_id':['in',where_str],'project_id':mem_data['project_id']}
                result = lib_post(method,content)
                if 500 == result['status_code']:
                    return (False,result['content'])
                if 200 == result['status_code'] and 0 == result['content']['is_success']:
                    pass
                else:
                    return (False,u'删除项目成员失败')

            #获取新集合与交集的差集(所得结果为要新增的项目成员)
            need_add = list(set(mem_data['admin_id']).difference(set(inersection)))
            if 0 < len(need_add):
                method = 'Projectmem.add'
                for item in need_add:
                    content = {'project_id':mem_data['project_id'],'admin_id':item}
                    result = lib_post(method, content)
                    if 500 == result['status_code']:
                        return (False,result['content'])
                    if 200 == result['status_code'] and 0 == result['content']['is_success']:
                        pass
                    else:
                        return (False,u'添加项目成员失败')

        #检查项目模块
        ##查询旧的项目模块
        status,old_project_mod = self.get_project_mod_name_by_project_id(mod_data['project_id'])
        if status:
            tmp_list = []
            for item in old_project_mod:
                tmp_list.append(urllib.quote(str(item)))
            old_project_mod = tmp_list
            #获取新旧列表的交集,此集合为不变元素
            inersection = list(set(mod_data['name']).intersection(set(old_project_mod)))
            #获取旧集合和交集的差集(所得结果删除的项目模块)
            need_delete = list(set(old_project_mod).difference(set(inersection)))
            #调用删除
            if 0 < len(need_delete):
                if 1 == len(need_delete):
                    where_str = str(need_delete[0])
                else:
                    tmp_list = need_delete
                    need_delete = []
                    for item in tmp_list:
                        need_delete.append(str(item))
                    where_str = ','.join(need_delete)
                method = 'Projectmodule.delete'
                content={'name':['in',where_str],'project_id':mod_data['project_id']}
                result = lib_post(method,content)
                if 500 == result['status_code']:
                    return (False,result['content'])
                if 200 == result['status_code'] and 0 == result['content']['is_success']:
                    pass
                else:
                    return (False,u'删除项目模块失败')

            #获取新集合与交集的差集(所得结果为要新增的项目模块)
            need_add = list(set(mod_data['name']).difference(set(inersection)))
            content = {'project_id':mem_data['project_id'],'name':item}
            if 0 < len(need_add):
                method = 'Projectmodule.add'
                for item in need_add:
                    result = lib_post(method, content)
                    if 500 == result['status_code']:
                        return (False,result['content'])
                    if 200 == result['status_code'] and 0 == result['content']['is_success']:
                        pass
                    else:
                        return (False,u'添加项目模块失败')

        return (True,u'成功修改')

    #更新bug
    def update_bug(self,data={},where={}):
        method = 'Bug.update'
        content = {}
        content['data'] = data
        content['where'] = where
        try:
            result = lib_post(method,content)
        except:
            return (False,u'更新异常')

        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功修改')

        return (False,u'修改失败')

    #更新用户
    def update_admin(self,data={},where={}):
        method = 'Admin.update'
        content = {}
        content['data'] = data
        content['where'] = where
        try:
            result = lib_post(method,content)
        except:
            return (False,u'更新异常')

        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功修改')

        return (False,u'修改失败')

    #修改密码
    '''
    data={'admin_name':'','passwd':''}
    '''
    def update_admin_passwd(self,data={}):
        method = 'Admin.update_passwd'
        content = {}
        content = data
        try:
            result = lib_post(method,content)
        except:
            return (False,u'更新异常')

        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功修改')

        return (False,u'修改失败')

    #更新角色
    def update_role(self,data={},where={}):
        method = 'Role.update'
        content = {}
        content['data'] = data
        content['where'] = where
        try:
            result = lib_post(method,content)
        except:
            return (False,u'更新异常')

        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功修改')

        return (False,u'修改失败')

    #更新部门
    def update_part(self,data={},where={}):
        method = 'Part.update'
        content = {}
        content['data'] = data
        content['where'] = where
        try:
            result = lib_post(method,content)
        except:
            return (False,u'更新异常')

        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功修改')

        return (False,u'修改失败')

    #更新简历
    def update_resume(self,data={},where={}):
        method = 'Resume.update'
        content = {}
        content['data'] = data
        content['where'] = where
        try:
            result = lib_post(method,content)
        except:
            return (False,u'更新异常')

        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功修改')

        return (False,u'修改失败')

    #更新招聘
    def update_positionhr(self,data={},where={}):
        method = 'Positionhr.update'
        content = {}
        content['data'] = data
        content['where'] = where
        try:
            result = lib_post(method,content)
        except:
            return (False,u'更新异常')

        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功修改')

        return (False,u'修改失败')

    #-----------------------删除:begin-----------------------
    #删除项目
    def delete_proejct(self,where={}):
        method = 'Project.delete'
        content = {}
        content['where'] = where

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功删除')

        return (False,u'删除失败')
        pass

    #删除bug
    def delete_bug(self,where={}):
        method = 'Bug.delete'
        content = {}
        content['where'] = where

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功删除')

        return (False,u'删除失败')

    #删除用户
    def delete_admin(self,where={}):
        method = 'Admin.delete'
        content = {}
        content['where'] = where

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功删除')

        return (False,u'删除失败')

    #删除角色
    def delete_role(self,where={}):
        method = 'Role.delete'
        content = {}
        content['where'] = where

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功删除')

        return (False,u'删除失败')

    #删除部门
    def delete_part(self,where={}):
        method = 'Part.delete'
        content = {}
        content['where'] = where

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功删除')

        return (False,u'删除失败')

    #删除简历
    def delete_resume(self,where={}):
        method = 'Resume.delete'
        content = {}
        content['where'] = where

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功删除')

        return (False,u'删除失败')

    #删除招聘岗位
    def delete_positionhr(self,where={}):
        method = 'Positionhr.delete'
        content = {}
        content['where'] = where

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0 == result['content']['is_success']:
            return (True,u'成功删除')

        return (False,u'删除失败')

    #-----------------------删除:end-----------------------

    #查询项目

    #查询bug


    #查询资源
    def get_resource(self):
        method = 'Resource.get_list'
        content = {'order':{'id':'asc'}}
        re_list = []

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code']:
            if 0< int(str(result['content']['record_count'])):
                return (True,result['content'])
        return (False,'')

    def get_resource_where(self,where={}):
        method = 'Resource.get_list'
        content = {'where':where}
        re_list = []

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code']:
            if 0< int(str(result['content']['record_count'])):
                return (True,result['content'])
        return (False,'')

    #查询项目成员,返回[admin_id,admin_id,admin_id,...]
    def get_project_mem(self,project_id=0):
        re_list = []
        method = 'Projectmem.get_list'
        content={'where':{'project_id':project_id},'page_size':20}
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0<result['content']['record_count']:
            rows = result['content']['record_count']
            for row in range(0, rows-1):
                re_list.append(result['content']['list'][row]['admin_id'])

        return re_list

    #查询项目模块
    def get_project_mod(self,project_id=0):
        re_list = []
        method = 'Projectmodule.get_list'
        content={'where':{'project_id':project_id},'page_size':20}
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code'] and 0<result['content']['record_count']:
            rows = result['content']['record_count']
            for row in range(0, rows-1):
                re_list.append(result['content']['list'][row]['name'])

        return re_list

    def get_resource_name(self):
        method = 'Resource.get_list'
        content = {'order':{'id':'asc'}}
        re_list = []

        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,result['content'])
        if 200 == result['status_code']:
            if 0< int(str(result['content']['record_count'])):
                rows = int(str(result['content']['record_count']))
                for i in range(0,rows-1):
                    re_list.append(result['content']['list'][i]['source_name'])
            return (True,re_list)
        return (False,'')
        pass
    def get_resource_id_name_map(self):
        pass

    #查询

    #新增

    #修改

    #删除

    #获取编号
    '''
    通过获取当前要求模块的最大的id，在此基础上加一已返回
    '''
    def get_number(self,module_index=0):
        cur_prefix = Dict.prefix_list[module_index]
        number = ''
        max_num = 1

        method = '%s.get_list'%Dict.module_list[module_index]
        content={'page_size':1}
        result = lib_post(method,content)
        if 500 == result['status_code']:
            lib_log(0,result['content'])
            return 'error'
        if 200 == result['status_code']:
            if 0 < int(result['content']['record_count']):
                max_num = int(result['content']['list'][0]['id'])
                max_num += 1

        number = '%06d'%max_num
        return '%s%s'%(cur_prefix,number)

    #获取字典
    def get_dict(self):
        method = 'Map.get_map'
        content = {}
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,'参数错误')
        elif 200 == result['status_code']:
            return (True,result['content'])

        return (False,'其他错误')

    #获取权限
    def get_right(self,role_id):
        method = 'Role.get_info'
        content = {'id':role_id}
        result = lib_post(method,content)
        if 500 == result['status_code']:
            return (False,'参数错误')
        elif 200 == result['status_code']:
            return (True,result['content'])

        return (False,'其他错误')