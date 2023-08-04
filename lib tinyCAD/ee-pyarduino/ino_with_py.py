import os
import subprocess
import serial.tools.list_ports
import argparse
import platform

parser =argparse.ArgumentParser()

parser.add_argument('--sketch', type=str, required=True)
parser.add_argument('--port', type=str, required=True)
parser.add_argument('--fqbn', type=str, required=True)

arg=parser.parse_args()



class runIno:
    
    current_platform=platform.system()
    
    if current_platform == "Linux" :
       program="arduino-cli"             # for running on Linux.
    elif current_platform == "Windows":
       program="arduino-cli.exe"         # for running on windows.
       
          
    def  compile_and_upload(self, sketch, port, fqbn):
        if arg.sketch == None:
           raise ValueError("Sketch not defined!")
        if not os.path.isfile(sketch ):
           raise ValueError("Sketch '{}' does not exist!".format(arg.sketch ))

        compile=[self.program, "compile", "--fqbn", "arduino:avr:nano", sketch]
        subprocess.run(compile)
    
        upload=[self.program, "upload","--port",port, "--fqbn", fqbn, sketch] 
        subprocess.run(upload)
     
    def serial_monitor(self,port):
        
       serAnzeige=serial.Serial(port,9600)

       while True:
           if serAnzeige.in_waiting>0:
                anz=serAnzeige.readline()  
                print(anz.decode().strip())
    
    
       serAnzeige.close()
        
run_file=runIno()
run_file.compile_and_upload(arg.sketch, arg.port, arg.fqbn)  
# run_file.serial_monitor(arg.port) 

       




