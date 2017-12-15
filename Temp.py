import serial
import binascii  
import struct 
import time

# 创建serial实例
serialport = serial.Serial()
serialport.port = 'COM3'
serialport.baudrate = 115200
serialport.parity = 'N'
serialport.bytesize = 8
serialport.stopbits = 1
serialport.timeout = 0.2

while 1:
    serialport.open()
    # 发送数据
    d=bytes.fromhex('0B 0B')
    serialport.write(d)
    #print (d)
    # 接收数据  
    str1 = serialport.read(2)
    data= binascii.b2a_hex(str1)
    data1=str((int(data,16)-1000)/10)
    print(data1)
    # 获取日期
    time1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #字符串合并
    data2 = time1 + ' ' + data1
    #print(data2)
    # 写入文件
    f1 = open('D:/temprecord.txt','a')
    f1.write(data2 + '\n')
    time.sleep(0.5)
    serialport.close()
