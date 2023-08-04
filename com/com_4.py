import serial
import time 

ser = serial.Serial("COM5", 9600)
ser.timeout=1

     
f= open("report.txt","w")
count=1


while True:
    
        ser.write("write memory".encode().strip())
        # time.sleep(0.5)
        # res=ser.readline().decode().strip() 
        res=ser.read_until("\n").decode().strip() 
        # time.sleep(0.05)
        print(res)         
        f.writelines(res+ "\n")
        count+=1
        if count==4 :
         break 
   
time.sleep(1)  
while True:
    
        ser.write("32".encode().strip())
        time.sleep(0.5)
        # res=ser.readline().decode().strip() 
        res=ser.read_until("\n").decode().strip() 
        # time.sleep(0.05)
        print(res)         
        f.writelines(res+ "\n")
        count+=1
        break 
     
while True:
    
        ser.write("16 12 45 87 78 45 45 45".encode().strip())
        time.sleep(0.5)
        # res=ser.readline().decode().strip() 
        res=ser.read_until("\n").decode().strip() 
        # time.sleep(0.05)
        print(res)         
        f.writelines(res+ "\n")
        count+=1
        break 
     
    
         
ser.close()   
