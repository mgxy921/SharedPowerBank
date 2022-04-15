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
                    continue
                
                if comm[0] == 'exit':
                    exit()
                
                # 查询已连接设备数据
                elif comm[0] == 'list':
                    if len(comm) <= 1:
                        continue
                    if comm[1] == 'cabinet':
                        print(Woshi.CabinetList)
                    
                # 0x80 强制弹出充电宝
                elif comm[0] == 'eject':
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        # 判断命令长度
                        if len(comm) == 3:
                            try:
                                # 判断是否是数字
                                slot = int(comm[2])
                                
                            except:
                                print('槽位输入错误')
                                continue
                            command = [comm[1].encode(),0,b'\x80',slot]
                            Woshi.CommandList.append(command)
                            
                        else:
                            print('eject command error')
                        
                    else:
                        print('cabinet not found')
                    
                # 0x64 查询机柜库存
                elif comm[0] == 'select' and comm[1] == 'cabinet':
                    
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        SN = comm[1]
                        
                        command = [SN.encode(),0,b'\x64']
                        continue
                        
                    else:
                        print('cabinet not found')
                    
                    
                # 0x65 借出充电宝
                elif comm[0] == 'borrow' and len(comm) == 3:
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    
                    if SN in Woshi.CabinetList:
                        
                        command = [SN,0,b'\x65',comm[2].encode()]
                        
                    Woshi.CommandList.append(command)
                        
                        
                # 0x67 远程重启
                elif comm[0] == 'reboot' and len(comm) == 2:
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        
                        command = [SN,0,b'\x67']
                        Woshi.CommandList.append(command)
                
                # 0x69 查询ICCID
                elif comm[0] == 'select' and comm[1] == 'iccid':
                    # 查询有没有这个机柜
                    SN = comm[2].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x69']
                
                # 0x77 查询机柜语音播报音量
                elif comm[0] == 'volume' and comm[1] == 'get':
                    # 查询有没有这个机柜
                    SN = comm[2].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x77']
                
                # 0x70 设置机柜语音播报音量
                elif comm[0] == 'volume' and comm[1] == 'set':
                    # 查询有没有这个机柜
                    SN = comm[2].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x70']
                
                
                elif comm[0] == 'network':
                    # 查询有没有这个机柜
                    SN = comm[1].encode()
                    if SN in Woshi.CabinetList:
                        command = [SN,0,b'\x72']
                
                
                # 查看命令列表
                elif comm[0] == 'commandlist':
                    print(Woshi.CommandList)
                    
            except:
                print('输入错误 2')
                
                
                
                
                