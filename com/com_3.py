import serial
import time 

ser = serial.Serial("COM5", 9600)
ser.timeout=1
cmd=["write memory","32","16 12 45 87 78 45 45 45"]

     
f= open("report.txt","w")
count=1
anz=0
cmd="read memory".strip()
for c in range(0,3):
    ser.write(cmd[c].encode().strip())
    
   
    while True:
       
        time.sleep(0.5)
       
        res=ser.readline().decode().strip() 
        # res=ser.read_until("\n").decode().strip() 
        # time.sleep(0.05)
        print(res)         
        f.writelines(res+ "\n")
        count+=1
        if count==3 :
            # time.sleep(2)
            break  
       
