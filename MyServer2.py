import socketserver
import Woshi
import ParseData
import ExecuteCommand


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
        
        # 机柜SN码
        SN = b''
        
        powerbankList = {}
        
        
        conn = self.request
        addr = self.client_address
        
        while True:
            # CabinetSN = ''
            # powerbankList = []
            
            
            
            
            
            comm , Emessage = ExecuteCommand.ExecuteCommand(conn)
            
            if comm == 0:
                print(Emessage)
                
                
                
            try:
                print('连接中')
                recv_data = conn.recv(1024)
                if not recv_data:
                    break
                else:
                    print(recv_data)
                    print(hex(recv_data[2]))
                    ParseData.ParseData(self,recv_data,conn,addr,SN)
            except:
                print('连接断开:',addr)
                break
            
            
            
            
            
            
            
        conn.close()
        