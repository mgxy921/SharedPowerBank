import socketserver
import time
import Woshi
import MyServerTest
import Controler
import asyncio
import threading
    
    
if __name__ == '__main__':
    
    
    Woshi._init()
    
    # 从文件中获取机柜数据
    
    
    
    
    threadTest = Controler.Controler(1,'Thread-1',1)
    threadTest.start()
    print('启动中')
    

    loop = asyncio.get_event_loop()
    tasks = [MyServerTest.MyServer('0.0.0.0',9233)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
        


