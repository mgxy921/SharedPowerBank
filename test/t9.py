

def getCheckSum(a):
    b = 0
    for i in range(len(a)):
        if i==0:
            b = a[i]
        else :
            b ^= a[i]
            
    return b
    
# 版本
VSN = b'\x01'
# 会话令牌
Token = b'\x11\x22\x33\x44'
comm =[0,0,b'\x63','1.22.33.44','9999']


# 命令长度
PacketLen = b'\x07'

# 有效数据的字节异或
CheckSum = b'\x00'

Address = comm[3].encode('utf-8')
AddressLen = (len(Address)+1).to_bytes(2,byteorder='big')

Port = comm[4].encode('utf-8')
PortLen = (len(Port)+1).to_bytes(2,byteorder='big')

Heartbeat = b'\x1e'

Payload = AddressLen + Address + b'\x00' + PortLen + Port + b'\x00' + Heartbeat
PacketLen = (len(Payload)+1).to_bytes(2,byteorder='big')
CheckSum = getCheckSum(Payload).to_bytes(1,byteorder='big')

print(type(CheckSum))
print(CheckSum)


command = PacketLen + comm[2] + VSN + CheckSum + Token + Payload

#print(command)

print(Payload)
print(command)
