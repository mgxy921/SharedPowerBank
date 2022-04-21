import socketserver
import time
import Woshi
import MyServer2
import Controler
import webAPI
    

if __name__ == '__main__':
    
    
    Woshi._init()
    
    # 从文件中获取机柜数据
    
    
    
    
    threadControler = Controler.Controler(1,'Controler',1)
    threadControler.start()
    print('控制台已启动')
    
    threadwebAPI = webAPI.webAPI(2,'webAPI',1)
    threadwebAPI.start()
    print('webAPI已启动')
    
    
    
    while True:
        print('建立与机柜连接')
        try:
        # 第一步
        #实例化server对象，传入本机ip，以及监听的端口号，还有新建的继承socketserver模块下的BaseRequestHandler类
            server = socketserver.ThreadingTCPServer(('0.0.0.0',9233),MyServer2.MyServer)  
            # 将重用端口设置成 True
            server.allow_reuse_address = True
            
        #激活服务端
            server.serve_forever()
            print('启动成功')
        except:
            print('连接中断')
            time.sleep(5)
            continue
    



