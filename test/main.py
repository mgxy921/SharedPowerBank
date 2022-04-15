import socket
# import Cabinet

from threading import Thread

def main():
    
    # 存储机柜数据 Cabinet.SN : ip
    global CabinetList
    CabinetList = {}
    
    # 存储充电宝数据 ID : Cabinet.SN
    PowerbankList = {}
    
    # 存储ICCID数据 Cabinet.SN : ICCID
    ICCIDList = {}
    
    # 全局命令变量
    CommandList = {}
    
    
    
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0',9233))
        print('bind')
        s.listen(5)
        print('listen')
        try:
            
            while True:
                
                connection,address=s.accept()
                print('客户端(%s)已成功连接。。'%str(address[0]))
                
                # 由于线程创建是在循环里创建和启动的
                # 因此每循环一次就会产生一个线程
                thread = Thread(target = work,args = (connection,address))
                thread.start()
                
        finally:
            s.close()


def work(sock,addr):
        
    # 登录后返回给机柜的报文
    login = b'\x00\x08\x60\x01\x00\x11\x22\x33\x44\x01'
    
    # 查询机柜库存及响应
    selectCabinet=b'\x00\x07\x64\x01\x00\x11\x22\x33\x44'

    while True:
        try:
            data = sock.recv(1024)
            print('接收到报文')
        except:
            print('连接断开')
        
        
        if len(data) == 0:
            break
        
        # 备注：带*的命令在老机柜不支持，
        # 2019.4月份出去的新机柜支持，为增强型维护用途，不应高频率使用。
        if data[2] == 0x60:
            
            print('login:',addr,"SN:",str(data[17:33],"utf-8"))
            CabinetList[data[17:33]] = addr[0]
            try:
                sock.send(login)
            except:
                print('登录时连接断开:',addr)
            print('查询机柜库存:',addr)
            try:
                sock.send(selectCabinet)
            except:
                print('连接断开')
            print(CabinetList,'已连接设备数量：',len(CabinetList))
            data = ''
        elif data[2] == 0x61:
            try:
                sock.send(data)
            except:
                print('心跳,连接断开:'+str(addr))
            print('心跳,地址:',addr)
            data = ''
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
        elif data[2] == 0x77:
            print('*查询机柜语音播报音量')
        elif data[2] == 0x70:
            print('*设置机柜语音播报音量')
        elif data[2] == 0x72:
            print('*查询机柜网络信息')
            
        else :
            print('未知指令',data[2])
            
            
if __name__ == '__main__':
        main()