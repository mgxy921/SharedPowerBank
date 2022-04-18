import socketserver
import Woshi
import ParseData
import ExecuteCommand


class MyServer(socketserver.BaseRequestHandler):
    
    def handle(self):

        # SN , addr , SN , ICCID , network , powerbankList
        # 0     1      2     3        4           5
        # CabinetData.SN :  [SN,addr,ICCID,network,powerbankList]
        # 查询机柜中SIM卡对应的ICCID，便于对SIM卡的维护管理。
        ICCID = ''
        
        # 信号强度（0到 31）
        CSQ = 0
        
        # 误码率
        SER = 0
        
        # 网络制式：2：GSM/GPRS/EDGE网络
        #          3：WCDMA网络
        #          7：LTE网络
        #          5: WI-FI
        Mode = 0
        
        network= [CSQ,SER,Mode]
        
        # 机柜SN码
        SN = b''
        
        powerbankList = {}
        
        volume = 0
        
        conn = self.request
        addr = self.client_address
        
        CabinetData = [SN,addr[0],ICCID,network,powerbankList]
        while True:
            
            comm , Emessage = ExecuteCommand.ExecuteCommand(conn)
            
            if comm == 0:
                print(Emessage)
                
            try:
                print('连接中')
                recv_data = conn.recv(1024)
                if not recv_data:
                    continue
                else:
                    print(recv_data)
                    print(hex(recv_data[2]))
                    comm , Pmessage = ParseData.ParseData(self,recv_data,conn,addr,SN)
                    
                    if comm == 0x64:
                        # 取出机柜库存信息
                        powerbankList = Pmessage
                        
                    elif comm == 0x60:
                        # 取出机柜SN码
                        SN = Pmessage
                        
                    elif comm ==0x69:
                        # 取出机柜ICCID
                        ICCID = Pmessage
                        
                    elif comm == 0x71:
                        # 取出机柜网络信息
                        network = Pmessage
                        
                    elif comm == 0x77:
                        volume = Pmessage
                        
                    # 更新机柜数据
                    CabinetData = [SN,addr[0],ICCID,network,powerbankList,volume]
                    # 把机柜数据存到全局变量
                    Woshi.CabinetList = { CabinetData[0] : CabinetData[1:]}
                
            except:
                print('连接断开:',addr)
                continue
            
            
            
            
            
            
            
        conn.close()
        