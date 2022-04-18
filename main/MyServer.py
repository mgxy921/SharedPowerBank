import socketserver
import Woshi
import ParseData


class MyServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        
        # 查询机柜中SIM卡对应的ICCID，便于对SIM卡的维护管理。
        ICCID = b''
        
        # 信号强度（0到 31）
        CSQ = 0
        
        # 误码率
        SER = 0
        
        # 网络制式：2：GSM/GPRS/EDGE网络
        #          3：WCDMA网络
        #          7：LTE网络
        #          5: WI-FI
        Mode = 0
        
        SN = b''
        
        powerbankList = {}
        
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
                    
                    # 向机柜发送已登录报文
                    conn.send(Woshi.login)
                    
                    # 存储机柜SN号
                    SN = data[17:33]
                    # 输出登录信息
                    # print('login:',addr,"SN:",str(data[17:33],"utf-8"))
                    Woshi.CabinetList[data[17:33]] = addr
                    
                    # 要求机柜返回机柜库存数据
                    conn.send(Woshi.selectCabinet)
                    print('登录后查询机柜库存')
                    # 按照CabinetList长度获取连接设备数量
                    #print(CabinetList,'已连接设备数量：',len(CabinetList))
                    
                    # 要求机柜查询库存
                    # Command = []
                    # CommandList.append(self.selectCabinet)
                    
                    return data[2],SN
                    
                except:
                    # print('登录时连接断开:',addr[0])
                    return data[2],'error'
                
            elif data[2] == 0x61:
                
                if SN == b'':
                    return data[2],'SN not found'
                
                try:
                    conn.send(data)
                    # print('发送心跳包,地址:',addr[0])
                    return data[2],'success'
                except:
                    # print('发送心跳包失败，地址:'+str(addr[0]))
                    return data[2],'error'
                
            elif data[2] == 0x62:
                
                
                # 存储机柜软件版本号
                print('查询机柜软件版本号及响应')
                
            elif data[2] == 0x63:
                # 存储机柜服务器地址
                print('响应设置机柜服务器地址')
                
                
            # 解析机柜发送给服务器的库存数据
            elif data[2] == 0x64:
                # 判断SN是否为空
                if SN == b'':
                    return 'SN not found',''
                # 剩余充电宝个数
                RemainNum = data[9]
                if RemainNum == 0:
                    return 'No powerbank',''
                # 解析充电宝数据
                powerbankList = Woshi.getpbdata(data)
                
                # print('0x64:收到机柜库存数据')
                # 存储机柜库存
                # print(powerbankList)
                return 0x64,powerbankList
                
            # 借充电宝
            elif data[2] == 0x65:
                
                # 存储弹出的充电包ID 和借用结果
                print('借充电宝及响应')
                
                return data[2],''
                
            # 还充电宝
            elif data[2] == 0x66:
                # 判断是否有机柜SN码
                
                if SN == '':
                    return 0x66,'SN not found'
                
                # 返回归还结果 归还成功或失败
                print('还充电宝及响应')
                Woshi.CommandList.append(data)
                
                return data[2],'success'
            
            # 远程重启机柜
            elif data[2] == 0x67:
                
                # 存储机柜已重启
                print('远程重启机柜及响应')
                print(data)
                
                #return data[2],''
                
            # 远程升级
            elif data[2] == 0x68:
                # 存储机柜已确认
                print('远程升级及响应')
                print(data)
                
                #return data[2],''
                
                
            #
            elif data[2] == 0x69:
                # 存储机柜ICCID
                print('查询ICCID')
                print(data)
                
                #return data[2],''
                
            #
            elif data[2] == 0x6A:
                # 存储服务器地址
                print('*查询服务器地址及响应')
                print(data)
                
                #return data[2],''
            
            #
            elif data[2] == 0x80:
                # 确认已弹出充电包
                print('*强制弹出充电宝')
                print(data)
                
                #return data[2],''
            
            # 
            elif data[2] == 0x77:
                # 存储机柜音量
                print('*查询机柜语音播报音量')
                print(data)
                
                #return data[2],''
            
            #
            elif data[2] == 0x70:
                
                # 确认机柜音量已改变
                print('*设置机柜语音播报音量')
                print(data)
                
                #return data[2],''
            
            #
            elif data[2] == 0x72:
                # 存储机柜网络信息
                print('*查询机柜网络信息')
                print(data)
                
                #return data[2],''
            
            
            else :
                print('未知指令',data[2])
                return data[2],'unknown'
            
            
            return data[2],''
        
        
        
        
        # 执行命令
        def ExecuteCommand(conn):
            def getCheckSum(a):
                b = 0
                for i in range(len(a)):
                    
                    
                    if i==0:
                        b = a[i]
                    else :
                        b ^= a[i]
                        
                return b
            
            
            
            # 初始化要执行的命令
            command = b''
            print('执行命令')
            print(Woshi.CommandList)
            if len(Woshi.CommandList) == 0:
                # print('commandlist lenth is 0')
                return 'commandlist lenth is 0'
            
            
            for comm in Woshi.CommandList:
                command = b''
                if len(comm) == 0:
                    # print('command lenth is null')
                    Woshi.CommandList.remove(comm)
                    return 'command lenth is null'

                # 一个线程对应一个机柜连接，如果有这个机柜的命令就执行
                if comm[0] == SN :
                    
                    # 如果是强制弹出命令
                    if comm[2] == b'\x80':
                        
                        
                        # 命令长度
                        PacketLen = b'\x08'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x01'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        # 槽位
                        slot = b''
                        slot = bytes([comm[3]])
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token + slot 
                        
                        print('command:',command)
                        
                        conn.sendall(command)
                        print('强制弹出充电宝')
                        Woshi.CommandList.remove(comm)
                        return 'command success'
                    
                    
                    # 查询机柜软件版本号
                    elif comm[2] == b'\x62':
                        # 查询机柜软件版本号
                        
                        # 命令长度
                        PacketLen = b'\x07'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x00'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token 
                        
                        print('command:',command)
                        
                        conn.sendall(command)
                        Woshi.CommandList.remove(comm)
                        return 'command 62 success'
                    
                    # 设置服务器地址
                    elif comm[2] == b'\x63':
                        
                        return 'command 63 success'
                    
                    #查询机柜库存
                    elif comm[2] == b'\x64':
                        
                        # 命令长度
                        PacketLen = b'\x07'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x00'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token 
                        
                        conn.sendall(command)
                        
                        return 'command 64 success'
                        
                    # 借充电宝
                    elif comm[2] == b'\x65':
                        
                        # 命令长度
                        PacketLen = b'\x07'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x00'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token 
                        
                        conn.sendall(command)
                        return 'command 65 success'
                        
                    #还充电宝
                    elif comm[2] == b'\x66':
                        
                        # 命令长度
                        PacketLen = b'\x09'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x01'
                        
                        
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        # 槽位
                        slot = b''
                        Slot = bytes([comm[3]])
                        
                        Result = b'\x01'
                        
                        CheckSum = getCheckSum([slot+Result])
                        
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token + Slot + Result
                        
                        conn.sendall(command)
                        print(command)
                        return 'command 66 success'
                        
                    # 远程重启机柜
                    elif comm[2] == b'\x67':
                        # 命令长度
                        PacketLen = b'\x07'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x00'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
                        
                        return 'command 67 success'
                        
                    # 远程升级
                    elif comm[2] == b'\x68':
                        
                        return 'command 68 success'
                    
                    # 查询ICCID
                    elif comm[2] == b'\x69':
                        # 命令长度
                        PacketLen = b'\x07'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x01'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
                        return 'command 69 success'
                    
                    
                    # 查询服务器地址
                    elif comm[2] == b'\x6A':
                        
                        return 'command 6A success'
                    
                    #查询机柜语音播报音量
                    elif comm[2] == b'\x77':
                        
                        # 命令长度
                        PacketLen = b'\x08'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x01'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
                        
                        
                        return 'command 77 success'
                    
                    # 设置机柜语音播报音量
                    elif comm[2] == b'\x70':
                        
                        # 命令长度
                        PacketLen = b'\x08'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x01'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        # 音量大小 (0到 15)
                        Lvl = bytes(comm[3])
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token + Lvl
                        
                        
                    # 查询机柜网络信息
                    elif comm[2] == b'\x72':
                        
                        # 命令长度
                        PacketLen = b'\x07'
                        # 版本
                        VSN = b'\x01'
                        # 有效数据的字节异或
                        CheckSum = b'\x01'
                        # 会话令牌
                        Token = b'\x11\x22\x33\x44'
                        
                        command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
                        
                        
            
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
        