# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
from multiprocessing import Process,Pipe

reload(sys)
sys.setdefaultencoding('utf-8')

#启动app
'''
消息格式:{'command':'xxx','params':{},'message':'xxx'}
{'command':'restart','params':{},'message':'重启app'}
{'command':'start','params':{'app':'master',function:{'name':'start_app_mqtt','param':''}},'message':'启动app'}
{'command':'send','params':{'app':'xxx','content':''},'message':'发送消息'}--mqtt接收到消息后发送给app界面解析
{'command':'recive','params':{'app':'xxx','content':''},'message':'接受消息'}--接受app重启要求|接受mqtt接受推送消息后发送的消息
实例:
功能:mqtt接受消息发送给主服务
消息格式:{'command':'send','params':{'app':'master','content':'xxx'},'message':'发送消息'}

功能:app成功登录发送消息启动mqtt推送
消息格式:{'command':'start','params':{'app':'master',function:{'name':'start_app_mqtt','param':''}}},'message':'启动app_mqtt'}
'''
def start_app(conn):
    from app import app
    my_app = app(conn)
    my_app.start()

#启动app_mqtt
def start_app_mqtt(topic,conn):
    from app_mqtt import CMqtt
    my_app_mqtt = CMqtt(topic,conn)

if __name__ == '__main__':
    #启动app
    parent_conn,child_conn=Pipe()
    ctl_app = True
    p_app = Process(target=start_app,args=(child_conn,))
    p_app.start()
    p_app.join()
    while ctl_app:
        message = parent_conn.recv()
        print 'recv message'
        print  message
        '''
        if 'send' == message['command']:
            params = message['params']
            if 'master' == params['app']:
                if params['function']:
                    print 'start sub app'
                    p_app_mqtt = Process(target=params['function']['name'],args=(child_conn,params['function']['param']))
                    p_app_mqtt.start()
                    p_app_mqtt.join()
      '''

