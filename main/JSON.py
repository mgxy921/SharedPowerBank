import json

data = [ { 'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5 } ]

class Cabinet:
    SN = b'WSTD061622706665'.decode('utf-8')
    ICCID = 1589860492192080601554

    # 信号强度（0到 31）
    CSQ = 31
    
    # 误码率
    SER = 0

    Mode = 4

    network= [CSQ,SER,Mode]

    addr = ('127.0.0.1','9233')

    powerbankList = {'WSBA20547': [1, 4], 'WSBA205368': [2, 4], 'WSBA205416': [3, 4], 'WSBA205351': [5, 4], 'WSBA205350': [6, 4]}

    
    volume = 0

    CabinetData = [SN,addr[0],ICCID,network,powerbankList,volume]


    CabinetList = { CabinetData[0] : CabinetData[1:] }
    CabinetJSON = {
        'SN' : CabinetData[0],
        'addr': CabinetData[1],
        'ICCID' : CabinetData[2],
        'network' : CabinetData[3],
        'powerbankList' : CabinetData[4],
        'volume' : CabinetData[5]
        
    }


data2 = json.dumps(Cabinet.CabinetJSON)
print(data2)