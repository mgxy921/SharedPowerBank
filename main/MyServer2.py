import socketserver
import Woshi
import ParseData2
import ExecuteCommand


class MyServer(socketserver.BaseRequestHandler):

    def setup(self):
        self.request.settimeout(1)

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

        network = [CSQ, SER, Mode]

        # 机柜SN码
        SN = b''

        powerbankList = {}

        volume = 0

        conn = self.request
        addr = self.client_address

        serveraddr = ()
        #version
        CabinetData = [
            SN, addr[0], ICCID, network, powerbankList, volume, serveraddr
        ]

        while True:

            #if comm == 0:
            #print(Emessage)

            try:
                Ecomm, Emessage = ExecuteCommand.ExecuteCommand(conn)
                Pcomm, Pmessage = ParseData2.ParseData(conn, addr, SN)

                if Pcomm == 0:
                    print('Pcomm == 0')
                    break

                # 取出机柜SN码
                elif Pcomm == 0x60:
                    SN = Pmessage

                # 取出机柜库存信息
                elif Pcomm == 0x64:
                    powerbankList = Pmessage

                elif Pcomm == 0x65 and Pmessage != 'error':
                    TerminalID = Pmessage

                # 取出机柜ICCID
                elif Pcomm == 0x69:
                    ICCID = Pmessage

                # 取出机柜网络信息
                elif Pcomm == 0x71:
                    network = Pmessage

                # 取出机柜语音播报音量
                elif Pcomm == 0x77:
                    volume = Pmessage

                elif Pcomm == 0x6A:
                    serveraddr = Pmessage

                # 更新机柜数据
                CabinetData = [
                    SN, addr[0], ICCID, network, powerbankList, volume,
                    serveraddr
                ]
                # 把机柜数据存到全局变量
                Woshi.CabinetList = {CabinetData[0]: CabinetData[1:]}

            except:
                # print('连接断开:',addr)
                continue
