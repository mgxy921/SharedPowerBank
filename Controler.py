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
            instr = input()
            
            # comm是用空格分割好的命令
            comm = list(instr.split())
            #command 是要添加进全局命令
            command = []
            # print(comm)
            try:
                if len(comm) == 0:
                    break
                
                if comm[0] == 'exit':
                    exit()
                
                # 查询已连接设备数据
                elif comm[0] == 'cabinetlist' :
                    
                    print(Woshi.CabinetList)
                    break
                    
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
                            break
                        command = [comm[1].encode(),0,b'\x80',slot]
                        
                        print(command)
                        Woshi.CommandList.append(command)
                        break
                            
                        
                    else:
                        print('cabinet not found')
                    
                # 0x64 查询机柜库存
                elif comm[0] == 'select' and comm[1] == 'cabinet':
                    
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        SN = comm[1]
                        
                        command = [SN.encode(),0,b'\x64']
                        
                        print(command)
                        Woshi.CommandList.append(command)
                        break
                        
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
                            
                            print(command)
                            Woshi.CommandList.append(command)
                            break
                            
                        except:
                            print('槽位输入错误')
                            break
                        
                        
                # 0x67 远程重启
                elif comm[0] == 'reboot' and len(comm) == 2:
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        
                        command = [SN,0,b'\x67']
                        
                        print(command)
                        Woshi.CommandList.append(command)
                        break
                
                # 0x69 查询ICCID
                elif comm[0] == 'select' and comm[1] == 'iccid':
                    # 查询有没有这个机柜
                    SN = comm[2].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x69']
                        
                        print(command)
                        Woshi.CommandList.append(command)
                        break
                        
                        
                # 0x77 查询机柜语音播报音量
                elif comm[0] == 'volume' and comm[1] == 'get':
                    # 查询有没有这个机柜
                    SN = comm[2].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x77']
                        
                        print(command)
                        Woshi.CommandList.append(command)
                        break
                        
                # 0x70 设置机柜语音播报音量
                elif comm[0] == 'volume' and comm[1] == 'set':
                    # 查询有没有这个机柜
                    SN = comm[2].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x70']
                        
                        print(command)
                        Woshi.CommandList.append(command)
                        break
                        
                        
                elif comm[0] == 'network':
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x72']
                        
                        print(command)
                        Woshi.CommandList.append(command)
                        break
                
                
                # 查看命令列表
                elif comm[0] == 'commandlist':
                    print(Woshi.CommandList)
                
                #print(command)
                
            except:
                print('输入错误 2')
                
                
                
                
                