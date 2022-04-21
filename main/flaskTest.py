from click import command
from flask import Flask
from flask import request, jsonify
import Woshi
'''
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

    powerbankList = {'WSBA20540717': [1, 4], 'WSBA20536836': [2, 4], 'WSBA20541667': [3, 4], 'WSBA20535118': [5, 4], 'WSBA20535091': [6, 4]}

    
    volume = 15

    CabinetData = [SN,addr[0],ICCID,network,powerbankList,volume]


    Woshi.CabinetList = { CabinetData[0] : CabinetData[1:] }
    CabinetJSON = {
        'SN' : CabinetData[0],
        'addr': CabinetData[1],
        'ICCID' : CabinetData[2],
        'network' : CabinetData[3],
        'powerbankList' : CabinetData[4],
        'volume' : CabinetData[5]
        
    }
'''

app = Flask(__name__)



# 传入数据返回JSON
def returnJSON(code, message, data):
    return jsonify({'code': code, 'message': message, 'data': data})


# 启动flask
def flaskRUN(host, port):
    # 设置调试模式，生产模式的时候要关掉debug
    app.debug = False
    app.run(host, port)


# 查询机柜所有数据
@app.route('/scan/shark/battery/selectCabinet/<SN>', methods=['GET'])
def selectCabinet(SN):
    # if 'sn' in request.args:
    #     SN = request.args['sn']
    #     print(SN)
    # else:
    #     return 'Error: 没有SN字段，请提供一个SN'
    #print(SN)

    SNb = SN.encode()
    #查找是否有这个机柜
    if SNb in Woshi.CabinetList:
        Cabinet = Woshi.CabinetList[SNb]

        JSON = {
            'SN': SN,
            'addr': Cabinet[0],
            'ICCID': Cabinet[1],
            'network': Cabinet[2],
            'powerbankList': Cabinet[3],
            'volume': Cabinet[4],
            'serveraddr': Cabinet[5],
        }

        return returnJSON('200', 'success', JSON)
    else:
        return returnJSON('404', 'Cabinet not found', {})


# 修改机柜连接服务器地址
@app.route('/scan/shark/battery/setServerAddr/<SN>', methods=['GET'])
def setServerAddr(SN):
    address = request.args.get('address')
    port = request.args.get('port')
    heartbeat = request.args.get('heartbeat')
    
    #检查ip地址端口心跳间隔是否合法
    if Woshi.check_ip(address) and Woshi.check_port(
            port) and Woshi.check_heartbeat(heartbeat):
        SNb = SN.encode()
        
        if SNb in Woshi.CabinetList:
            
            command = [SNb, 0, b'\x63', address, port, heartbeat]
            
            return returnJSON('200', 'success', {})
        else:
            return returnJSON('404', 'Cabinet not found', {})
    return returnJSON('400', 'bad request', {})


# 查询机柜库存
@app.route('/scan/shark/battery/selectStock/<SN>', methods=['GET'])
def selectStock(SN):
    SNb = SN.encode()
    if SNb in Woshi.CabinetList:
        Cabinet = Woshi.CabinetList[SNb]
        JSON = {
            'powerbankList': Cabinet[3],
        }
        return returnJSON('200', 'success', JSON)
    else:
        return returnJSON('404', 'Cabinet not found', {})


# 借充电宝
@app.route('/scan/shark/battery/borrowPowerBank/<SN>/<ID>', methods=['GET'])
def borrowPowerBank(SN, ID):
    SNb = SN.encode()
    # 如果有这个机柜
    if SNb in Woshi.CabinetList:
        Cabinet = Woshi.CabinetList[SNb]
        # 如果有这个充电宝
        if ID in Cabinet[3]:
            # powerbankList是一个字典，key是充电宝ID，value是一个列表，列表的第一个元素是充电宝的插槽位置（slot），第二个元素是充电宝的电量
            powerbankList = Cabinet[3][ID]

            slot = powerbankList[0]
            command = [SNb, 0, b'\x65', slot]
            Woshi.CommandList.append(command)

            return returnJSON('200', 'success', {})
        else:
            return returnJSON('404', 'powerbank ID not found', {})
    else:
        return returnJSON('404', 'Cabinet not found', {})
    # comm=
    # Woshi.CommandList.append(SN)


# 重启机柜
@app.route('/scan/shark/battery/rebootCabinet/<SN>', methods=['GET'])
def rebootCabinet(SN):
    SNb = SN.encode()
    # 如果有这个机柜
    if SNb in Woshi.CabinetList:
        command = [SNb, 0, b'\x67']
        Woshi.CommandList.append(SN)
        return returnJSON('200', 'success', {})
    else:
        return returnJSON('404', 'Cabinet not found', {})


# 查询ICCID
@app.route('/scan/shark/battery/selectICCID/<SN>', methods=['GET'])
def selectICCID(SN):
    SNb = SN.encode()
    # 如果有这个机柜
    if SNb in Woshi.CabinetList:
        ICCID = Woshi.CabinetList[SNb][1]
        JSON = {
            'ICCID': ICCID,
        }
        return returnJSON('200', 'success', JSON)
    else:
        return returnJSON('404', 'Cabinet not found', {})


# 查询机柜连接服务器地址
@app.route('/scan/shark/battery/selectServerAddr/<SN>', methods=['GET'])
def selectServerAddr(SN):
    SNb = SN.encode()
    # 如果有这个机柜
    if SNb in Woshi.CabinetList:
        serveraddr = Woshi.CabinetList[SNb][5]
        JSON = {
            'serveraddr': serveraddr,
        }
        return returnJSON('200', 'success', JSON)
    else:
        return returnJSON('404', 'Cabinet not found', {})


# 强制弹出充电宝
@app.route('/scan/shark/battery/ejectPowerBank/<SN>/<ID>', methods=['GET'])
def ejectPowerBank(SN, ID):
    SNb = SN.encode()
    # 如果有这个机柜
    if SNb in Woshi.CabinetList:
        Cabinet = Woshi.CabinetList[SNb]
        # 如果有这个充电宝
        if ID in Cabinet[3]:
            # powerbankList是一个字典，key是充电宝ID，value是一个列表，
            # 列表的第一个元素是充电宝的插槽位置（slot），第二个元素是充电宝的电量
            powerbankList = Cabinet[3][ID]

            slot = powerbankList[0]
            command = [SNb, 0, b'\x80', slot]
            Woshi.CommandList.append(command)

            return returnJSON('200', 'success', {})
        else:
            return returnJSON('404', 'powerbank ID not found', {})
    else:
        return returnJSON('404', 'Cabinet not found', {})


# 查询机柜音量
@app.route('/scan/shark/battery/getVolume/<SN>', methods=['GET'])
def getVolume(SN):
    SNb = SN.encode()
    if SNb in Woshi.CabinetList:
        Cabinet = Woshi.CabinetList[SNb]
        JSON = {
            'volume': Cabinet[4],
        }

        return returnJSON('200', 'success', JSON)
    else:
        return returnJSON('404', 'Cabinet not found', {})


# 设置机柜音量
@app.route('/scan/shark/battery/setVolume/<SN>/<lvl>', methods=['GET'])
def setVolume(SN, lvl):
    SNb = SN.encode()
    if SNb in Woshi.CabinetList:
        command = [SNb, 0, b'\x70', lvl]
        Woshi.CommandList.append(command)
        return returnJSON('200', 'success', {})
    else:
        return returnJSON('404', 'Cabinet not found', {})


# 查询机柜网络信息
@app.route('/scan/shark/battery/network/<SN>', methods=['GET'])
def network(SN):
    SNb = SN.encode()
    if SNb in Woshi.CabinetList:
        Cabinet = Woshi.CabinetList[SNb]
        JSON = {
            'network': Cabinet[2],
        }
        return returnJSON('200', 'success', JSON)
    else:
        return returnJSON('404', 'Cabinet not found', {})

