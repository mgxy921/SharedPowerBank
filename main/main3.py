import socketserver
import time
import Woshi
import MyServer2
import Controler

    
    
if __name__ == '__main__':
    
    
    Woshi._init()
    
    # 从文件中获取机柜数据
    
    
    
    
    threadTest = Controler.Controler(1,'Thread-1',1)
    threadTest.start()
    print('启动中')
    
    while True:
        
        try:
        # 第一步
        #实例化server对象，传入本机ip，以及监听的端口号，还有新建的继承socketserver模块下的BaseRequestHandler类
            server = socketserver.ThreadingTCPServer(('0.0.0.0',9233),MyServer2.MyServer)  
        #激活服务端
            server.serve_forever()
            print('启动成功')
        except:
            print('连接中断')
            time.sleep(5)
            continue
        


