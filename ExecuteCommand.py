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
    
    
    for comm in Woshi.CommandList:
        command = b''
        if len(comm) == 0:
            # print('command lenth is null')
            Woshi.CommandList.remove(comm)
            return 0,'command lenth is null'

        # 一个线程对应一个机柜连接，如果有这个机柜的命令就执行
        #if comm[0] == SN :
            
            # 如果是强制弹出命令
        if comm[2] == b'\x80':
            print('ExecuteCommand','强制弹出命令')
            
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
            
            conn.send(command)
            print('强制弹出充电宝')
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
        
        
        # 查询机柜软件版本号
        elif comm[2] == b'\x62':
            # 查询机柜软件版本号
            print('ExecuteCommand','查询机柜软件版本号')
            
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
            
            conn.send(command)
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
        
        # 设置服务器地址
        elif comm[2] == b'\x63':
            print('ExecuteCommand','设置服务器地址')
            
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
        
        #查询机柜库存
        elif comm[2] == b'\x64':
            print('ExecuteCommand','查询机柜库存')
            
            # 命令长度
            PacketLen = b'\x07'
            # 版本
            VSN = b'\x01'
            # 有效数据的字节异或
            CheckSum = b'\x00'
            # 会话令牌
            Token = b'\x11\x22\x33\x44'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token 
            
            conn.send(command)
            
            
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
            
        # 借充电宝
        elif comm[2] == b'\x65':
            print('ExecuteCommand','借充电宝')
            
            # 命令长度
            PacketLen = b'\x07'
            # 版本
            VSN = b'\x01'
            # 有效数据的字节异或
            CheckSum = b'\x00'
            # 会话令牌
            Token = b'\x11\x22\x33\x44'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token 
            
            conn.send(command)
            
            
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
            
        #还充电宝
        elif comm[2] == b'\x66':
            print('ExecuteCommand','还充电宝')
            
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
            
            conn.send(command)
            print(command)
            
            # 命令执行完要删除此命令
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
            
        # 远程重启机柜
        elif comm[2] == b'\x67':
            print('ExecuteCommand','远程重启机柜')
            
            # 命令长度
            PacketLen = b'\x07'
            # 版本
            VSN = b'\x01'
            # 有效数据的字节异或
            CheckSum = b'\x00'
            # 会话令牌
            Token = b'\x11\x22\x33\x44'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            
            conn.send(command)
            # 命令执行完要删除此命令
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
            
        # 远程升级
        elif comm[2] == b'\x68':
            print('ExecuteCommand','远程升级')
            
            return comm[0],'success'
        
        # 查询ICCID
        elif comm[2] == b'\x69':
            
            print('ExecuteCommand','查询ICCID')
            # 命令长度
            PacketLen = b'\x07'
            # 版本
            VSN = b'\x01'
            # 有效数据的字节异或
            CheckSum = b'\x01'
            # 会话令牌
            Token = b'\x11\x22\x33\x44'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            conn.send(command)
            # 命令执行完要删除此命令
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
        
        
        # 查询服务器地址
        elif comm[2] == b'\x6A':
            print('ExecuteCommand','查询服务器地址')
            # 命令执行完要删除此命令
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
        
        #查询机柜语音播报音量
        elif comm[2] == b'\x77':
            print('ExecuteCommand','查询机柜语音播报音量')
            # 命令长度
            PacketLen = b'\x08'
            # 版本
            VSN = b'\x01'
            # 有效数据的字节异或
            CheckSum = b'\x01'
            # 会话令牌
            Token = b'\x11\x22\x33\x44'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            conn.send(command)
            # 命令执行完要删除此命令
            Woshi.CommandList.remove(comm)
            
            return comm[0],'success'
        
        # 设置机柜语音播报音量
        elif comm[2] == b'\x70':
            print('ExecuteCommand','设置机柜语音播报音量')
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
            conn.send(command)
            # 命令执行完要删除此命令
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
            
        # 查询机柜网络信息
        elif comm[2] == b'\x72':
            print('ExecuteCommand','查询机柜网络信息')
            # 命令长度
            PacketLen = b'\x07'
            # 版本
            VSN = b'\x01'
            # 有效数据的字节异或
            CheckSum = b'\x01'
            # 会话令牌
            Token = b'\x11\x22\x33\x44'
            
            command = b'\x00' + PacketLen + comm[2] + VSN + CheckSum + Token
            
            conn.send(command)
            # 命令执行完要删除此命令
            Woshi.CommandList.remove(comm)
            return comm[0],'success'
            
    
    return 0,'no command'
