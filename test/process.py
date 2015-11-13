import multiprocessing
import time
from multiprocessing import Process, Pipe, Queue
import paho.mqtt.client as mqtt

class ClockProcess(multiprocessing.Process):
	def __init__(self, q):
		multiprocessing.Process.__init__(self)
		self.q = q


	def on_connect(self,client, userdata, flags, rc):
		client.subscribe('bug/#')
		pass

	def on_message(self,client, userdata, msg):
		#print msg.payload
		self.q.put(msg.payload)
		pass

	def run(self):
		c = mqtt.Client()
		c.connect("192.168.1.131", 1883, 60)
		c.on_connect = self.on_connect
		c.on_message = self.on_message
		c.loop_forever()


if __name__ == "__main__":
	q = Queue()
	p = ClockProcess(q)
	p.start()
	#p.join()
	print 'begin\n'
	i = 0
	while True:
		print 'i am pareng\n'
		print q.get()
		time.sleep(1)
		i += 1
		if i>1000:
			sys.exit()
	