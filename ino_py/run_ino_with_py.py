import subprocess
import serial.tools.list_ports
import serial



port= serial.tools.list_ports.comports()
bPort=None
portList=[]
for p in port:    
    bPort=p
    portList.append(str(p))
    print(p)


val= input("select port: COM")

for x in range(0,len(portList)):
    if  portList[x].startswith("COM"+str(val)):
        portvar="COM"+str(val)
if bPort is None:
    raise Exception("Arduino Board nicht gefunden")

path_arduinoCLI="arduino-cli.exe"

sketch= "ino_py.ino"

"""
serAnzeige=serial.Serial()
serAnzeige.baudrate=9600
serAnzeige.port=portvar
serAnzeige.open()"""

compile=[path_arduinoCLI, "compile", "--fqbn", "arduino:avr:nano", sketch]
subprocess.run(compile)

upload=[path_arduinoCLI, "upload","--port",str(portvar), "--fqbn", "arduino:avr:nano", sketch] #  """str(bPort)[:-26]"""
subprocess.run(upload, check=False)


serAnzeige=serial.Serial(str(portvar),9600)
#time.sleep(2)

while True:
    if serAnzeige.in_waiting>0:
     anz=serAnzeige.readline()
    
     print(anz.decode().strip())
    
    
serAnzeige.close()

