#coding=utf-8
import threading
from time import ctime,sleep

import paho.mqtt.client as mqtt

class my_mosquitto():
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("192.168.1.131", 1883, 60)
        '''
        while True:
            client.loop()
        '''
        client.loop_forever()
    
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("bug/#")
    
    def on_message(self,client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        my_msg = msg.payload


def music(func):
    my_mosquitto()


threads = []
t1 = threading.Thread(target=music,args=(u'爱情买卖',))
threads.append(t1)

if __name__ == '__main__':
    global my_msg
    for t in threads:
        t.setDaemon(True)
        t.start()

   # print "all over %s" %ctime()
    while 1:
        i = 1