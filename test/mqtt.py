import paho.mqtt.client as mqtt
import time
import sys

def my_on_connect(client, userdata, flags, rc):
	client.subscribe('bug/#')
	pass

def my_on_message(client, userdata, msg):
	print msg.payload
	pass

c = mqtt.Client()
c.connect("192.168.1.131", 1883, 60)
c.on_connect = my_on_connect
c.on_message = my_on_message
#c.loop_forever()

if __name__ == "__main__":
	c.loop_start()
	i =0 
	while i<10:
		print 'i am parent\n'
		i += 1
		time.sleep(1)
	c.loop_stop()
	sys.exit(0)