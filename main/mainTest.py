import socketserver
import time
import Woshi
import MyServerTest
import Controler
import asyncio
import threading
import asyncioTest
    
    
if __name__ == '__main__':
    Woshi._init()
    
    threadTest = Controler.Controler(1,'Thread-1',1)
    threadTest.start()
    print('启动中')
    while True:
        
        try:
            asyncio.run(asyncioTest.main())
        except:
            print('服务器启动失败')
            time.sleep(5)
            continue