import paho.mqtt.client as mqtt

class CMqtt():
    def __init__(self,topic='#'):
        self.topic = topic
        self.my_client = mqtt.Client()
        self.my_client.on_connect = self.on_connect
        self.my_client.on_message = self.on_message
        self.my_client.connect("192.168.1.131", 1883, 60)
        self.my_client.loop_start()

    def on_connect(self,client, userdata,flag, rc):
        client.subscribe(CMqtt.topic)

    def on_message(self,client, userdata, msg):
        #调用消息提示
        #mainWindow.touch_sig(str(msg.payload))
        pass