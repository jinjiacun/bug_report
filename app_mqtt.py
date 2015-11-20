import paho.mqtt.client as mqtt
from multiprocessing import Process,Pipe

class CMqtt():
    def __init__(self,topic='#',conn=None):
        self.topic = topic
        self.my_client = mqtt.Client()
        self.my_client.on_connect = self.on_connect
        self.my_client.on_message = self.on_message
        self.my_client.connect("192.168.1.131", 1883, 60)
        self.my_client.loop_start()
        print 'start mqtt'

    def on_connect(self,client, userdata,flag, rc):
        client.subscribe(self.topic)

    def on_message(self,client, userdata, msg):
        #调用消息提示
        #mainWindow.touch_sig(str(msg.payload))
        message = {'command':'send','params':{'app':'master','content':'xxx'},'message':'发送消息'}
        message['params'] = str(msg.payload)
        self.send(message)
        print message

    def close(self):
        if self.conn:
            self.conn.close()

if __name__ == '__main__':
    my_app_mqtt = CMqtt()