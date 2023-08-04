import subprocess
import serial.tools.list_ports
import os
import argparse

parser =argparse.ArgumentParser()

parser.add_argument('--sketch', type=str, required=True)
parser.add_argument('--port', type=str, required=True)

arg=parser.parse_args()

if arg.sketch == None:
    raise ValueError("Source not defined!")
if not os.path.isfile(arg.sketch ):
    raise ValueError("Source file '{}' does not exist!".format(arg.sketch ))
program="arduino-cli"

#sketch= "Blink/Blink.ino"
#portvar="/dev/ttyS6"

compile=[program, "compile", "--fqbn", "arduino:avr:nano", arg.sketch]
subprocess.run(compile)

upload=[program, "upload","--port",arg.port, "--fqbn", "arduino:avr:nano", arg.sketch] 
subprocess.run(upload)


serAnzeige=serial.Serial(arg.port,9600)

while True:
    if serAnzeige.in_waiting>0:
     anz=serAnzeige.readline()
    
     print(anz.decode().strip())
    
    
serAnzeige.close()

