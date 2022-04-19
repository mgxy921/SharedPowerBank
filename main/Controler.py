import threading
import Woshi


    
class Controler(threading.Thread):
    
    
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        
        while True:
            try:
                instr = input()
            except:
                
                continue
            
            # comm是用空格分割好的命令
            comm = list(instr.split())
            #command 是要添加进全局命令
            command = []
            # print(comm)
            try:
                if len(comm) == 0:
                    continue
                
                if comm[0] == 'exit':
                    exit()
                
                # 查询已连接设备数据
                elif comm[0] == 'cabinetlist' :
                    
                    print(Woshi.CabinetList)
                    continue
                    
                # 0x80 强制弹出充电宝  判断命令长度
                elif comm[0] == 'eject' and len(comm) == 3:
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        try:
                            # 判断是否是数字
                            slot = int(comm[2])
                            
                        except:
                            print('槽位输入错误')
                            continue
                        command = [comm[1].encode(),0,b'\x80',slot]
                        
                        
                        
                        
                        
                        
                    else:
                        print('cabinet not found')
                    
                # 0x64 查询机柜库存
                elif comm[0] == 'select' and comm[1] == 'cabinet':
                    
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        SN = comm[1]
                        
                        command = [SN.encode(),0,b'\x64']
                        
                        
                        
                        
                        
                    else:
                        print('cabinet not found')
                    
                    
                # 0x65 借出充电宝
                elif comm[0] == 'borrow' and len(comm) == 3:
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    
                    if SN in Woshi.CabinetList:
                        
                        try:
                            # 判断是否是数字
                            slot = int(comm[2])
                            command = [SN,0,b'\x65',slot]
                            
                        except:
                            print('槽位输入错误')
                            continue
                    else:
                        print('cabinet not found')
                        
                # 0x67 远程重启
                elif comm[0] == 'reboot' and len(comm) == 2:
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        
                        command = [SN,0,b'\x67']
                        
                        
                        
                        
                    else:
                        print('cabinet not found')
                
                # 0x69 查询ICCID
                elif comm[0] == 'iccid':
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x69']
                        
                        
                        
                        
                    else:
                        print('cabinet not found')
                        
                # 0x77 查询机柜语音播报音量
                elif comm[0] == 'getvolume' :
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x77']
                        
                        
                        
                        
                    else:
                        print('cabinet not found')
                    
                        
                # 0x70 设置机柜语音播报音量
                elif comm[0] == 'setvolume' :
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        try:
                            lvl = int(comm[2])
                        except:
                            print('音量输入错误')
                        command = [SN,0,b'\x70',lvl]
                        
                        
                        
                        
                    else:
                        print('cabinet not found')
                        
                
                # 查询机柜网络信息
                elif comm[0] == 'network' and len(comm) == 2:
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x71']
                        
                        
                        
                        
                    else:
                        print('cabinet not found')
                
                # 查询服务器地址
                elif comm[0] == 'server' and len(comm) == 2:
                
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x6A']
                
                # 设置服务器地址
                elif comm[0] == 'setserver' and len(comm) == 4:
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        
                        if Woshi.check_ip(comm[2]) == True:
                            
                            try:
                                # 判断是否是数字
                                port = int(comm[3])
                                
                            except:
                                print('端口输入错误')
                                continue
                                    # 判断端口是否在0-65535
                            if port > 65535:
                                print('端口范围输入错误')
                                continue
                            
                            else:
                                command = [SN,0,b'\x63',comm[2],comm[3]]
                                
                            
                            
                            print()
                            
                            
                        else:
                            print('ip error')
                            continue
                            
                        
                
                
                # 查询机柜软件版本号
                elif comm[0] == 'version' and len(comm) == 2:
                
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x62']
                
                # 查看命令列表
                elif comm[0] == 'commandlist':
                    print(Woshi.CommandList)
                    continue
                
                #print(command)
                print(command)
                Woshi.CommandList.append(command)
                
            except:
                print('输入错误 2')
                
                
                
                
                