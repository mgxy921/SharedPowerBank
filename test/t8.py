data = b'\x00\x1dj\x015\x00\x00\x124\x00\x091.4.9.79\x00\x00\x04933\x00\x1e'


import re

def check_ip(ipAddr):

    compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')

    if compile_ip.match(ipAddr):

        return True

    else:

        return False


AddressLen = data[10]
PortLen = data[AddressLen + 12]

Heartbeat = data[-1]

Address = data[11:10+AddressLen].decode('utf-8')
Port = data[13+AddressLen:-2].decode('utf-8')

serveraddr = (Address,Port,Heartbeat)


print(serveraddr)
ip = '1.1.1.'
print(check_ip(ip))