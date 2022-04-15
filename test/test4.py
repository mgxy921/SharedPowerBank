import imp
import threading
import time

class Testthreading(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        while True:
            print("开始线程：" + self.name)
            time.sleep(1)
            
        
if __name__ == '__main__':
    thread1 = Testthreading(1,"Thread-1",1)
    thread1.start()
    while True:
        s=input()
        print(s)