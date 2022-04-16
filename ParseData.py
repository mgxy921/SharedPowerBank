import Woshi


    
def ParseData(self,data,conn,addr,SN):
    
    
    print('解析命令')
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
        
    # 收到心跳包
    elif data[2] == 0x61:
        
        # 判断SN是否为空
        if not SN:
            
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
        if not SN:
            return data[2],'SN not found'
        # 剩余充电宝个数
        RemainNum = data[9]
        if RemainNum == 0:
            return data[2],'No powerbank'
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
        print('机柜已重启')
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
    
    
    return data[2],'success'