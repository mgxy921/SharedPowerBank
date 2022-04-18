

    
    # 初始化全局变量
def _init():
    # 存储机柜数据 CabinetData.SN :  [SN,addr,ICCID,network,powerbankList]
    global CabinetList
    CabinetList = {}
    
    # 存储充电宝数据 ID : Cabinet.SN
    global PowerbankList
    PowerbankList = {}
    
    # 存储ICCID数据 Cabinet.SN : ICCID
    global ICCIDList
    ICCIDList = {}
    
    # 全局命令变量
    global CommandList
    CommandList = []
        

# 解析 0x64 命令：查询机柜库存
def getpbdata(a):
    
    
    # 有个大聪明把16进制数字当成10进制发过来了，要想办法把它转换成10进制，再转换成字符串
    def hexlisttostr(hexlist):
        
        str1=''
        for a in hexlist:
            t1 = hextoint(a)
            t2 = str(t1)
            str1 = str1+t2
        return str1
    
    # 假16进制转换成10进制
    def hextoint(a):
        if int(a)>=16:
            a = a - 6*int(a%256/16)
        return a
    
    # b 充电宝数据 从第11位到结束
    b = a[10:]
    #print('b:',b,'len:',len(b))
    #最终返回的数据为字典类型
    pblist = {}
    
    #存储单个充电宝数据
    pbdata = []
    #存储临时数据
    pb = b''
    for i in b:
        
        
        pb = pb + bytes([i])
        lenpb = len(pb)
        if len(pb) == 10:
            
            # 充电宝ID字母部分
            SN1 = pb[1:5].decode('utf-8')
            
            # 充电宝ID数字部分
            SN2 = hexlisttostr(pb[5:8])
            # 拼接充电宝ID再添加进pbdata
            pbdata.append(SN1+SN2)
            # pbdata.append(pb[1:4])
            
            # pbdata.append(test6.hexlisttoint(pb[5:8]))
            
            # 充电宝在机柜中的位置 添加进pbdata
            pbdata.append(pb[0])
            
            # 充电宝电量 添加进pbdata
            pbdata.append(pb[9])
            
            # 把充电宝ID和槽位电量添加进字典
            pblist[str(pbdata[0])] = pbdata[1:]
            
            pb = b''
            pbdata =[]
            
            
    return pblist


# 登录后返回给机柜的报文
login = b'\x00\x08\x60\x01\x00\x11\x22\x33\x44\x01'

# 查询机柜库存及响应
selectCabinet=b'\x00\x07\x64\x01\x00\x11\x22\x33\x44'

# 还充电宝，服务器固定发送给机柜的上行报文
#returnpb= b'\x00\x09\x66\x01\x01\x11\x22\x33\x44'


#borrowpb =b'\x00\x07\x66\x01\x00\x11\x22\x33\x44'


# 命令类型: 机柜登录及相应
# 机柜-->服务器
LOGIN = b'\x60'

# 命令类型: 心跳包    
# 机柜-->服务器
HEART_BEAT = b'\x61'

# 命令类型: 查询软件软件版本号
# 服务器-->机柜
SOFT_VERSION = b'\x62'

# 命令类型: 设置服务器地址
# 服务器-->机柜
SERVER_ADDR = b'\x63'

# 命令类型: 查询机柜库存
# 服务器-->机柜
SELECT_CABINET = b'\x64'

# 命令类型: 借出充电宝
# 服务器-->机柜
BORROW =  b'\x65'

# 命令类型: 归还充电宝
# 机柜-->服务器
RETURN = b'\x66'

# 命令类型: 重启机柜
# 服务器-->机柜
REBOOT = b'\x67'

# 命令类型: 更新软件
# 服务器-->机柜
UPDATE_SOFT = b'\x68'

# 命令类型: 查询ICCID
# 服务器-->机柜
SELECT_ICCID = b'\x69'

# 命令类型: 查询服务器地址
# 服务器-->机柜
SELECT_SERVER = b'\x6a'

# 命令类型: 强制弹出充电宝
# 服务器-->机柜
FORCE_EJECT = b'\x80'

# 命令类型: 查询音量
# 服务器-->机柜
SELECT_VOLUME = b'\x77'

# 命令类型: 设置音量
# 服务器-->机柜
SET_VOLUME = b'\x70'

# 命令类型: 查询机柜网络信息
# 服务器-->机柜
SELECT_NETWORK = b'\x72'
