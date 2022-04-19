import asyncio
import time
import Woshi
import ParseData2
import ExecuteCommand2
import Controler


async def handle_echo(reader, writer):
    
    
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
    serveraddr = ()
    
    addr = writer.get_extra_info('peername')
    # conn = self.request
    # addr = self.client_address
    
    
    CabinetData = [SN,addr[0],ICCID,network,powerbankList,volume,serveraddr]

    
    
    while True:
        try:
            reader_data = await reader.read(1024)
            
        except:
            print('连接断开:',addr)
        # message = data.decode()
        # addr = writer.get_extra_info('peername')
        
        comm , Emessage = ExecuteCommand2.ExecuteCommand(writer)
        
        # print('addr:',addr)
        
        if not reader_data:
            break
        
        else:
            # print(reader_data)
            # print(hex(reader_data[2]))
            comm , Pmessage = ParseData2.ParseData(reader_data,writer,addr,SN)
            # 取出机柜库存信息
            if comm == 0x64:
                powerbankList = Pmessage
            
            # 取出机柜SN码
            elif comm == 0x60:
                SN = Pmessage
            
            # 取出机柜ICCID
            elif comm ==0x69:
                ICCID = Pmessage
            
            # 取出机柜网络信息
            elif comm == 0x71:
                network = Pmessage
                
            # 取出机柜语音播报音量
            elif comm == 0x77:
                volume = Pmessage
                
            elif comm == 0x6A:
                serveraddr = Pmessage
                
            # 更新机柜数据
            CabinetData = [SN,addr[0],ICCID,network,powerbankList,volume,serveraddr]
            # 把机柜数据存到全局变量
            Woshi.CabinetList = { CabinetData[0] : CabinetData[1:]}
        
            # print(f"Received {message!r} from {addr!r}")
            # print(f"Send: {message!r}")
            # writer.write(data)
            # await writer.drain()

    # print("Close the connection")
    # writer.close()

async def main():
    while True:
        try:
            server = await asyncio.start_server(
                handle_echo, '0.0.0.0', 9233)
        
        except:
            print('服务器启动失败')
            
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    Woshi._init()
    
    threadTest = Controler.Controler(1,'Thread-1',1)
    threadTest.start()
    print('启动中')
    while True:
        
        try:
            asyncio.run(main())
        except:
            print('服务器启动失败')
            time.sleep(5)
            continue
            