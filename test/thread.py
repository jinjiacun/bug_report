import threading  
import time  
import paho.mqtt.client as mqtt

class timer(threading.Thread): #The timer class is derived from the class threading.Thread  
    def __init__(self, num, interval):  
        threading.Thread.__init__(self)  
        #self.thread_num = num  
        #self.interval = interval

        self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put what you want the thread do here  
        '''
        while not self.thread_stop:  
            print 'Thread Object(%d), Time:%s\n' %(self.thread_num, time.ctime())  
            time.sleep(self.interval)  
        '''
        c = mqtt.Client()
        c.connect("192.168.1.131", 1883, 60)
        c.on_connect = self.on_connect
        c.on_message = self.on_message
        while not self.thread_stop:
            c.loop()
        #c.loop_forever()
        pass

    def stop(self):  
        self.thread_stop = True

    def on_connect(self,client, userdata, flags, rc):
        client.subscribe('bug/#')
        pass

    def on_message(self,client, userdata, msg):
        #print msg.payload
        #self.q.put(msg.payload)
        print msg.payload
        pass
         
   
def test():  
    thread1 = timer(1, 1)  
    #thread2 = timer(2, 2)  
    thread1.start()  
    #thread2.start()  
    #time.sleep(10)  
    i = 0
    while i<1000: 
        print 'i am parent\n'
        i += 1
        time.sleep(2)
    thread1.stop()  
    #thread2.stop()  
    return  
   
if __name__ == '__main__':  
    test()  