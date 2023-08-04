import serial.tools.list_ports

ports= serial.tools.list_ports.comports()
ser_int=serial.Serial()
portList=[]

for port in ports:
    portList.append(port)
    print(str(port))
    
    
    
#val= input("select port: COM")

#for x in range(0, len(portList)):
    #if portList[x].startswith("COM"+str(val)):
portvar=ports
        
        
        
ser_int.baudrate=9600
ser_int.port=str(portvar)
ser_int.open()

while True:
    if ser_int.in_waiting:
        packet=ser_int.readline
        print(packet.decode('utf'))
    