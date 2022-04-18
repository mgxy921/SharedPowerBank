



def getCheckSum(a):
    b = 0
    for i in range(len(a)):
        if i==0:
            b = a[i]
        else :
            b ^= a[i]
            
    return b