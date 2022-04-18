class Cabinet:
    SN = ''
    pb = []
    
    def __init__(self,SN) -> None:
        self.SN =SN
    
    def addpb(self,newpb) -> None:
        self.pb = self.pb.append(newpb)
    
    class PowerBank:
        ID = ''
        power = 0
        slot = 0
        
        def __init__(self,ID,power,slot) -> None:
            self.ID = ID
            self.power = power
            self.slot = slot


class Command:
    LOGIN = b'\x60'
    HEART_BEAT = b'\x61'
    SOFT_VERSION = b'\x62'
    SERVER_ADDR = b'\x63'
    SELECT_CABINET = b'\x64'
    BORROW =  b'\x65'
    RETURN = b'\x66'
    REBOOT = b'\x67'
    UPDATE_SOFT = b'\x68'
    SELECT_ICCID = b'\x69'
    SELECT_SERVER = b'\x6a'
    FORCE_EJECT = b'\x80'
    SELECT_VOLUME = b'\x77'
    SET_VOLUME = b'\x70'
    SELECT_NETWORK = b'\x72'
