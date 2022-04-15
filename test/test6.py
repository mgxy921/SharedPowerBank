
t = [32,83,81]


# 有个大聪明把16进制数字当成10进制发过来了，要想办法把它转换成10进制

def hexlisttostr(hexlist):
    
    str1=''
    
    
    for a in hexlist:
        t1 = hextoint(a)
        t2 = str(t1)
        str1 = str1+t2
        #num.append(bytes(str(hextoint(a))))
        
        
    return str1
        
    

def hextoint(a):
    if int(a)>=16:
        a = a - 6*int(a%256/16)
    return a




#for i in range(154):
#    print(i,'   ',hexlisttobytes(i))

#print(hextoint(t))
print(hexlisttostr(t))