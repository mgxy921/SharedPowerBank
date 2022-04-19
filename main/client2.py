import socket
import time
import threading
from webbrowser import get

login = b'\x00\x20\x60\x01\xfd\x11\x22\x33\x44\x55\x66\x77\x88\x02\x33\x00\x11\x57\x53\x54\x44\x30\x36\x31\x36\x32\x32\x37\x30\x36\x36\x36\x36\x00'
ping = b'\x00\x07\x61\x01\x00\x11\x22\x33\x44'
select = b'\x00:d\x01\xc1\x11"3D\x05\x01WSBA Sh6\x04\x02WSBA T\x07\x17\x04\x03WSBA T\x16g\x04\x05WSBA SQ\x18\x04\x06WSBA SP\x91\x04'

    
HOST = '127.0.0.1'  # 服务器的主机名或者 IP 地址
PORT = 9233        # 服务器使用的端口


def getData(socket):

        while True:
            data = socket.recv(1024)
            print(data)
            if data[2] == 0x64:
                socket.send(select)
                print('select')
        
def sendData(socket):
    while True:
        try:
            socket.send(login)
            print('loginning')
            while True:
                
                time.sleep(30)
                try:
                    socket.send(ping)
                    print('ping')
                except:
                    print('心跳包 error')
                    
                    break
        except:
            print('loginning error')
        
    
    
    
        
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        try:
            s.connect((HOST, PORT))
            thread = threading.Thread(target=getData, args=(s,))
            thread.setDaemon(True)
            thread.start()
            
            sendData(s)
            
        except:
            print('connect error')
            time.sleep(5)
        

