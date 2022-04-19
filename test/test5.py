


# 解析 0x64 命令：查询机柜库存
# 有个大聪明把16进制数字当成10进制发过来了，要想办法把它转换成10进制，再转换成字符串

def hexlisttostr(hexlist):
    
    str1=''
    for a in hexlist:
        t1 = hextoint(a)
        if t1<10:
            
            t2 = '0' + str(t1)
        else:
            t2 = str(t1)
        
        str1 = str1+t2
    return str1
    
def hextoint(a):
    if int(a)>=16:
        a = a - 6*int(a%256/16)
    return a


a = b'\x00:d\x01\xc1\x11"3D\x05\x01WSBA Sh6\x04\x02WSBA T\x07\x17\x04\x03WSBA T\x16g\x04\x05WSBA SQ\x18\x04\x06WSBA SP\x91\x04'

# 剩余充电宝个数
# num= a[9]



def getpbdata(a):
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
            SN2 = hexlisttostr(pb[5:9])
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


b = getpbdata(a)
print(b)