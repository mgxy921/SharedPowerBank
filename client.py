import socket
import time

login = b'\x00\x20\x60\x01\xfd\x11\x22\x33\x44\x55\x66\x77\x88\x02\x33\x00\x11\x57\x53\x54\x44\x30\x36\x31\x36\x32\x32\x37\x30\x36\x36\x36\x36\x00'
ping = b'\x00\x07\x61\x01\x00\x11\x22\x33\x44'

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        while True:
            try:
                clientsocket.connect(('localhost', 9233))
                print('connected')
                
                try:
                    clientsocket.send(login)
                    print('loginning')
                    while True:
                        
                        time.sleep(30)
                        try:
                            clientsocket.send(ping)
                            print('ping')
                        except:
                            print('心跳包 error')
                            clientsocket.close()
                            break
                except:
                    print('loginning error')
                
                finally:
                    clientsocket.close()
                    time.sleep(5)
                
            except:
                print('connect error')
                
                time.sleep(5)
                break
                
            finally:
                clientsocket.close()
                




    