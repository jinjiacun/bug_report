# -*- coding: utf-8 -*-
'''
处理.ini文件的读写操作
'''
#!/usr/bin/env python
import sys,os
import ConfigParser
import re
import codecs
from configobj import ConfigObj
import  xml.dom.minidom
from xml.dom.minidom import Document
reload(sys)
sys.setdefaultencoding('utf-8')


class Db_Connector:
  def __init__(self, config_file_path):
    '''
    content = open(config_file_path).read()
    #Window下用记事本打开配置文件并修改保存后，编码为UNICODE或UTF-8的文件的文件头
    #会被相应的加上\xff\xfe（\xff\xfe）或\xef\xbb\xbf，然后再传递给ConfigParser解析的时候会出错
    #，因此解析之前，先替换掉
    content = re.sub(r"\xfe\xff","", content)
    content = re.sub(r"\xff\xfe","", content)
    content = re.sub(r"\xef\xbb\xbf","", content)
    open(config_file_path, 'w').write(content)

    self.config_file_path = config_file_path
    cf = ConfigParser.ConfigParser()
    cf.readfp(codecs.open(config_file_path, "r", "utf-8"))
    '''
    self.config_file_path = config_file_path
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    s = cf.sections()
    print 'section:', s
    o = cf.options("serverconf")
    print 'options:', o
    v = cf.items("serverconf")
    print 'db:', v
    db_host = cf.get("serverconf", "host")
    db_port = cf.getint("serverconf", "port")

    db_user = cf.get("userconf", "user")
    db_pwd = cf.get("userconf", "password")
    self.cf = cf
    #cf.set("userconf","user", "admin")
    #cf.set("userconf", "password", "admin")
    #cf.write(open(config_file_path, "w"))

  def get_value(self, team, name):
    return self.cf.get(team, name)

  def set_value(self, team, name, value):
    self.cf.set(team, name, value)
    self.cf.write(open(self.config_file_path, "w"))

  def get_value_right_team(self):
      return self.cf.get('userconf','right_team')

  def get_value_right_lab(self):
      return self.cf.get('userconf','right_lab')

  def get_value_right(self):
      return self.cf.get('userconf','right')
'''
class Db_Connector:
  def __init__(self, config_file_path):
    if not os.path.exists(config_file_path):
        self.create_config_xml(config_file_path)
    my_xml = xml.dom.minidom.parse(config_file_path)
    cf = my_xml.documentElement
    self.cf = cf

  def get_value(self, name):
    cur_node = self.cf.getElementsByTagName(name)
    return cur_node[0].nodeValue


  def set_value(self, team, name, value):
    self.cf[team][name] = value
    self.cf.write()

  def create_config_xml(self, file_name):
    f = open(file_name, "w")
    doc = Document()  #创建DOM文档对象
    config = doc.createElement("config")
    #config.setAttribute('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")#设置命名空间
    #config.setAttribute('xsi:noNamespaceSchemaLocation','bookstore.xsd')#引用本地XML Schema
    doc.appendChild(config)

    user = doc.createElement("user")
    user.data = ''
    config.appendChild(user)

    passwd = doc.createElement("passwd")
    passwd.data = ''
    config.appendChild(passwd)

    f.write(doc.toprettyxml(indent = ''))
    f.close()
'''

if __name__ == "__main__":
  f = Db_Connector("./config.ini")
  print 'main:'
  print f.get_value("userconf", "user")