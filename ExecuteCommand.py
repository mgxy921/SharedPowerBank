import Woshi


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
    # print(Woshi.CommandList)
    if len(Woshi.CommandList) == 0:
        # print('commandlist lenth is 0')
        return 0,'commandlist lenth is 0'
    
    # 版本
    VSN = b'\x01'
    # 会话令牌
    Token = b'\x11\x22\x33\x44'
    
    for comm in Woshi.CommandList:
        command = b''
        # 一个线程对应一个机柜连接，如果有这个机柜的命令就执行
        if len(comm) == 0:
            Woshi.CommandList.remove(comm)
            return 0,'commandlist lenth is 0'
        #if comm[0] == SN :
            
            # 如果是强制弹出命令
        if comm[2] == b'\x80':
            print('ExecuteCommand','强制弹出命令')
            
            # 命令长度
            PacketLen = b'\x08'
            
            
            # 有效数据的字节异或
            CheckSum = b'\x01'
            
            
            # 槽位
            slot = b''
            slot = bytes([comm[3]])
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token + slot 
            
            
            
        
        
        # 查询机柜软件版本号
        elif comm[2] == b'\x62':
            # 查询机柜软件版本号
            print('ExecuteCommand','查询机柜软件版本号')
            
            # 命令长度
            PacketLen = b'\x07'
            
            # 有效数据的字节异或
            CheckSum = b'\x00'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token 
            
            
            
        
        # 设置服务器地址
        elif comm[2] == b'\x63':
            print('ExecuteCommand','设置服务器地址')
            
            # 命令长度
            PacketLen = b'\x07'
            
            # 有效数据的字节异或
            CheckSum = b'\x00'
            
            
            
            
        
        #查询机柜库存
        elif comm[2] == b'\x64':
            print('ExecuteCommand','查询机柜库存')
            
            # 命令长度
            PacketLen = b'\x07'
            
            # 有效数据的字节异或
            CheckSum = b'\x00'
            
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token 
            
            
            
        # 借充电宝
        elif comm[2] == b'\x65':
            print('ExecuteCommand','借充电宝')
            
            # 命令长度
            PacketLen = b'\x07'
            
            # 有效数据的字节异或
            CheckSum = b'\x00'
            
            
            slot = bytes([comm[3]])
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token + slot
            
            
            
        #还充电宝
        elif comm[2] == b'\x66':
            print('ExecuteCommand','还充电宝')
            
            # 命令长度
            PacketLen = b'\x09'
            
            # 有效数据的字节异或
            CheckSum = b'\x01'
            
            # 槽位
            Slot = bytes([comm[3]])
            
            Result = b'\x01'
            
            CheckSum = getCheckSum(slot+Result)
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token + Slot + Result
            
            
            
        # 远程重启机柜
        elif comm[2] == b'\x67':
            print('ExecuteCommand','远程重启机柜')
            
            # 命令长度
            PacketLen = b'\x07'
            
            # 有效数据的字节异或
            CheckSum = b'\x00'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            
            
            
        # 远程升级
        elif comm[2] == b'\x68':
            print('ExecuteCommand','远程升级')
            
            
        
        # 查询ICCID
        elif comm[2] == b'\x69':
            
            print('ExecuteCommand','查询ICCID')
            # 命令长度
            PacketLen = b'\x07'
            
            # 有效数据的字节异或
            CheckSum = b'\x01'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            
        
        
        # 查询服务器地址
        elif comm[2] == b'\x6A':
            print('ExecuteCommand','查询服务器地址')
            # 命令执行完要删除此命令
            
            # 命令长度
            PacketLen = b'\x07'
            # 有效数据的字节异或
            CheckSum = b'\x01'
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            
            
        
        #查询机柜语音播报音量
        elif comm[2] == b'\x77':
            print('ExecuteCommand','查询机柜语音播报音量')
            # 命令长度
            PacketLen = b'\x08'
            
            # 有效数据的字节异或
            CheckSum = b'\x00'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            
            
            
            
        
        # 设置机柜语音播报音量
        elif comm[2] == b'\x70':
            print('ExecuteCommand','设置机柜语音播报音量')
            # 命令长度
            PacketLen = b'\x08'
            
            # 有效数据的字节异或
            CheckSum = b'\x01'
            
            # 音量大小 (0到 15)
            Lvl = bytes([comm[3]])
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token + Lvl
            
            
            
            
        # 查询机柜网络信息
        elif comm[2] == b'\x71':
            print('ExecuteCommand','查询机柜网络信息')
            # 命令长度
            PacketLen = b'\x07'
            
            # 有效数据的字节异或
            CheckSum = b'\x01'
            
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            
            
            
        else:
            print('？？？？？')
            Woshi.CommandList.remove(comm)
            return 0,'no command'
        
        print('发送的报文：',command)
        # 发送命令
        conn.send(command)
        # 命令执行完要删除此命令
        Woshi.CommandList.remove(comm)
        
    
    return comm[0],'success'
    
