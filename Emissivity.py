import serial
import binascii  
import struct 
import time
# 创建serial实例
serialport = serial.Serial()
serialport.port = 'COM14'
serialport.baudrate = 115200
serialport.parity = 'N'
serialport.bytesize = 8
serialport.stopbits = 1
serialport.timeout = 0.5
#异或校验
def uchar_checkbcc(data, byteorder='little'):  
    ''''' 
    char_checkbcc 按字节计算异或校验。 
    @param data: 字节串 
    @param byteorder: 大/小端 
    '''  
    length = len(data)  
    checkbcc = 0  
    for i in range(0, length):  
        checkbcc ^= int.from_bytes(data[i:i+1], byteorder, signed=False)    
    checkbcc = hex(checkbcc)[2:]
    return checkbcc
#LRC校验
def uchar_checklrc(data, byteorder='little'):  
    ''''' 
    char_checksum 按字节计算校验和补码。
    @param data: 字节串 
    @param byteorder: 大/小端 
    '''  
    length = len(data)  
    checksum = 0  
    for i in range(0, length):  
        checksum += int.from_bytes(data[i:i+1], byteorder, signed=False)
        checksum &= 0xFF # 强制截断
    checklrc = hex(2**8-checksum)[2:]      #补码
    return checklrc   
i = 1000
while (i > 99):
    serialport.open()
    # 发送数据
    #d=bytes.fromhex('0d03ded0')
    value = hex(int(i))[2:]
    if len(value) % 2 != 0:
        value = '0d0' + value
    elif len(value) % 4 != 0:
        value = '0d00' + value
    xx = bytes.fromhex(value)
    yy = uchar_checkbcc(xx)
    if len(yy) % 2 != 0:
        yy = '0' + yy    
    d = value + yy
    d1 = bytes.fromhex(d)
    serialport.write(d1)
    print (d1)
    # 接收数据  
    str1 = serialport.read(2)
    print(str1)
    str2 = str1 + bytes(1)
    data2= binascii.b2a_hex(str2)
    if(int(data2,16) == 0):
        str1 = bytes([1])
    data= binascii.b2a_hex(str1)
    print(data)
    data1=str(int(data,16)/1000)
    print(data1)
    # 获取日期
    time1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #字符串合并
    data2 = time1 + ' ' + str(i) + ' '+ str(d) +' ' +data1
    print(data2)
    # 写入文件
    f1 = open('D:/temprecord.txt','a')
    f1.write(data2 + '\n')
    f1.close()
    i = i - 10
    time.sleep(3)
    serialport.close()
