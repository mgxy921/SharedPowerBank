from flask import Flask
from flask import request, jsonify
import Woshi

# class Cabinet:
#     SN = b'WSTD061622706665'.decode('utf-8')
#     ICCID = 1589860492192080601554

#     # 信号强度（0到 31）
#     CSQ = 31
    
#     # 误码率
#     SER = 0

#     Mode = 4

#     network= [CSQ,SER,Mode]

#     addr = ('127.0.0.1','9233')

#     powerbankList = {'WSBA20540717': [1, 4], 'WSBA20536836': [2, 4], 'WSBA20541667': [3, 4], 'WSBA20535118': [5, 4], 'WSBA20535091': [6, 4]}

    
#     volume = 15

#     CabinetData = [SN,addr[0],ICCID,network,powerbankList,volume]


#     Woshi.CabinetList = { CabinetData[0] : CabinetData[1:] }
#     CabinetJSON = {
#         'SN' : CabinetData[0],
#         'addr': CabinetData[1],
#         'ICCID' : CabinetData[2],
#         'network' : CabinetData[3],
#         'powerbankList' : CabinetData[4],
#         'volume' : CabinetData[5]
        
#     }
    


app = Flask(__name__)
@app.route('/scan/shark/battery/<SN>', methods=['GET'])
def api_SN(SN):
    # if 'sn' in request.args:
    #     SN = request.args['sn']
    #     print(SN)
    # else:
    #     return 'Error: 没有SN字段，请提供一个SN'
    print(SN)
    SNb = SN.encode()
    if SNb in Woshi.CabinetList:
        results = Woshi.CabinetList[SNb]
        
        CabinetJSON = {
            'SN' : SN ,
            'addr': results[0],
            'ICCID' : results[1],
            'network' : results[2],
            'powerbankList' : results[3],
            'volume' : results[4]
            
        }
    
        return jsonify(CabinetJSON)
    else:
        return 'Error: 没有找到SN为' + SN + '的机柜'


def flaskRUN():
    app.debug = False # 设置调试模式，生产模式的时候要关掉debug
    app.run()
    
