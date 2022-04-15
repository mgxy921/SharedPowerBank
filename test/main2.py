import socketserver
import Woshi
import threading

class MyServer(socketserver.BaseRequestHandler):
    
    # 登录后返回给机柜的报文
    # login = b'\x00\x08\x60\x01\x00\x11\x22\x33\x44\x01'
    # 查询机柜库存及响应
    # selectCabinet=b'\x00\x07\x64\x01\x00\x11\x22\x33\x44'
    

    
    def handle(self):

        SN = ''
        # 解析命令
        def ParseData(self,data,conn,addr):
            print('解析命令')
            nonlocal SN
            if len(data) == 0:
                return '',''
            
            # 备注：带*的命令在老机柜不支持，
            # 2019.4月份出去的新机柜支持，为增强型维护用途，不应高频率使用。
            if data[2] == 0x60:
                
                try:
                    conn.send(Woshi.login)
                    SN = data[17:33]
                    # 输出登录信息
                    # print('login:',addr,"SN:",str(data[17:33],"utf-8"))
                    CabinetList[data[17:33]] = addr
                    
                    # 按照CabinetList长度获取连接设备数量
                    #print(CabinetList,'已连接设备数量：',len(CabinetList))
                    
                    # 要求机柜查询库存
                    # Command = []
                    # CommandList.append(self.selectCabinet)
                    
                    return 'login',str(data[17:33])

                except:
                    # print('登录时连接断开:',addr[0])
                    return 'login error',''
                
            elif data[2] == 0x61:
                try:
                    conn.send(recv_data)
                    # print('收到心跳包,地址:',addr[0])
                    return 'heartbeat',''
                except:
                    # print('发送心跳包失败，地址:'+str(addr[0]))
                    return 'heartbeat error',''
                
            elif data[2] == 0x62:
                print('查询机柜软件版本号及响应')
            elif data[2] == 0x63:
                print('设置机柜服务器地址及响应')
            elif data[2] == 0x64:
                print('查询机柜库存及响应')
            elif data[2] == 0x65:
                print('借充电宝及响应')
            elif data[2] == 0x66:
                print('还充电宝及响应')
                
                return 'return',''
            elif data[2] == 0x67:
                print('远程重启机柜及响应')
            elif data[2] == 0x68:
                print('远程升级及响应')
            elif data[2] == 0x69:
                print('查询ICCID')
            elif data[2] == 0x6A:
                print('*查询服务器地址及响应')
            elif data[2] == 0x80:
                print('*强制弹出充电宝')
                return 'force',''
            elif data[2] == 0x77:
                print('*查询机柜语音播报音量')
            elif data[2] == 0x70:
                print('*设置机柜语音播报音量')
            elif data[2] == 0x72:
                print('*查询机柜网络信息')
                
            else :
                print('未知指令',data[2])
                return 'unknown',''
        
        # 执行命令
        def ExecuteCommand(conn):
            print('执行命令')
            # print(CommandList)
            if len(CommandList) == 0:
                # print('commandlist lenth is 0')
                return 'commandlist lenth is 0'
            
            for comm in CommandList:
                if len(comm) == 0:
                    print('command lenth is null')
                    CommandList.remove(comm)
                    return 'command lenth is null'

                # 如果有命令
                if comm[0] == SN :
                    
                    # 如果是强制弹出命令
                    if comm[2] == b'\x80':
                        
                        command = b''
                        # 命令长度
                        PacketLen = b'\x08'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x01'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        # 槽位
                        if comm[3] == '1':
                            slot = b'\x01'
                        elif comm[3] == '2':
                            slot = b'\x02'
                        elif comm[3] == '3':
                            slot = b'\x03'
                        elif comm[3] == '4':
                            slot = b'\x04'
                        elif comm[3] == '5':
                            slot = b'\x05'
                        elif comm[3] == '6':
                            slot = b'\x06'

                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token + slot 
                        
                        print('command:',command)
                        
                        conn.sendall(command)
                        print('强制弹出充电宝')
                        CommandList.remove(comm)
                        return 'command success'
                    
                    
                    elif comm[2] == b'\x64':
                        conn.sendall(Woshi.selectCabinet)
                        
                    elif comm[2] == b'\x65':
                        conn.sendall(Woshi.borrowpb)
                    
            return 'no command'
        
        
        while True:
            # CabinetSN = ''
            # powerbankList = []
            
            
            
            conn = self.request
            addr = self.client_address
            
            ExecuteCommand(conn)
            
            try:
                print('连接中')
                recv_data = conn.recv(1024)
            except:
                print('连接断开:',addr)
                break
            
            
            if len(recv_data) != 0:
                ParseData(self,recv_data,conn,addr)
            
            
            
            
            
        conn.close()
        
        
class Controler(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        
        while True:
            instr = input()
            
            # comm是用空格分割好的命令
            comm = list(instr.split())
            command = []
            # print(comm)
            try:
                if len(comm) == 0:
                    continue
                
                if comm[0] == 'exit':
                    exit()
                
                elif comm[0] == 'list':
                    if len(comm) <= 1:
                        continue
                    if comm[1] == 'cabinet':
                        print(CabinetList)
                    
                elif comm[0] == 'eject':
                    if len(comm) == 3:
                        command = [comm[1].encode(),0,b'\x80',comm[2]]
                        CommandList.append(command)
                    else:
                        print('eject error')
                    
                    
                    # print('comm:',comm)
                    # print('CommandList:',CommandList)
                    
                elif comm[0] == 'select' and comm[1] == 'cabinet':
                    if comm[2] in CabinetList:
                        print('选择机柜成功')
                        SN = comm[2]
                    else:
                        print('机柜不存在')
                    
                elif comm[0] == 'borrow' and len(comm) == 2:
                    command = [comm[1].encode(),0,b'\x65']
                    CommandList.append(command)
                        
                elif comm[0] == 'commandlist':
                    print(CommandList)
                    
            except:
                print('输入错误 2')
            

    
    
if __name__ == '__main__':
    
    
    # 存储机柜数据 Cabinet.SN : ip
    global CabinetList
    CabinetList = {}
    
    # 存储充电宝数据 ID : Cabinet.SN
    global PowerbankList
    PowerbankList = {}
    
    # 存储ICCID数据 Cabinet.SN : ICCID
    global ICCIDList
    ICCIDList = {}
    
    # 全局命令变量
    global CommandList
    CommandList = []
    
    # 从文件中获取机柜数据
    
    
    
    
    threadTest = Controler(1,'Thread-1',1)
    threadTest.start()
    
    try:
    # 第一步
    #实例化server对象，传入本机ip，以及监听的端口号，还有新建的继承socketserver模块下的BaseRequestHandler类
        server = socketserver.ThreadingTCPServer(('0.0.0.0',9233),MyServer)  
    #激活服务端
        server.serve_forever()
    except:
        print('服务器被占用')
        exit()
