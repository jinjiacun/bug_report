#!/usr/bin/env python
from multiprocessing import Process, Pipe, Queue
import paho.mqtt.client as mqtt


class c_mosquitto():

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        #client.connect("192.168.1.131", 1883, 60)
        self.client.connect_async("192.168.1.131", 1883, 60)
        self.client.loop_start()
        #self.client.loop()
        #while True:
         #   client.loop()
            #client.loop_forever()
        pass


    def on_connect(self,client, userdata, flags, rc):
        #print("Connected with result code "+str(rc))
        client.subscribe("bug/#")
    
    def on_message(self,client, userdata, msg):        
        print(msg.topic+" "+str(msg.payload))
        pass


    def begin(self,q):
        q.put(1)

def work(q):
    my_mosquitto = c_mosquitto()
    

if __name__ == '__main__':
    q = Queue()
    global my_mosquitto
    my_mosquitto = c_mosquitto()
    print 'hello'
    '''
    p = Process(target=work, args=(q))
    p.start()
    p.join()
    while True:
        my_mosquitto.client.loop()
        print q.get()
    '''