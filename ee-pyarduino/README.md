# ee-pyarduino
Python arduino interface to upload ino files and communcate with serial interfacte

# How to use ino_with_py.py to compile and upload a sketch to a board?
the program take two parameter:
+ --sketch: for the path to the sketch you wannt to run
+ --port: port to which the board is connected
+ --fqbn: Fully Qualified Board Name

the program can work on all operating system, the prerequisite is the installation of arduino-cli 

## Installation of Arduino CLI
+ Linux <br>
to install Arduino CLI follow the instructions in the following URL <br>
https://rohmann.atlassian.net/wiki/spaces/EPL600/pages/394625025/Arduino+CLI <br>
or https://siytek.com/arduino-cli-raspberry-pi/
+ Windows<br>
to install Arduino Cli on windows, go to https://arduino.github.io/arduino-cli/0.31/installation/
and download the appropriate version


## port designation depending on the operating system
+ Windows: COM1, COM2, ..., COMn
+ Linux: /dev/ttyUSB0, /dev/ttyACM0, ...
+ Linux subsystem on windows: /dev/ttyS0, /dev/ttyS1, ..., /dev/ttySn <br>

to know the ports to which your arduino board are connected, type the following command in the terminal:<br>
```shell 
arduino-cli board list
```


### examples: 
to run the program enter the following command in the terminal: 

+ On Windows: <br>
to use this program on windows, the arduino-cli program (arduino-cli.exe) should be in the same folder with the Python code<br>

```shell
py ino_with_py.py --sketch C:\Users\path\to\sketch\sketch.ino --port COM8 -- fqbn arduino:avr:nano
```

+ on Linux: (ubuntu, Raspberry pi, etc.) <br>
```shell
python3 ino_with_py.py --sketch /path/to/sketch/sketch.ino --port /dev/ttyUSB0 -- fqbn arduino:avr:nano
````

+ Linux subsystem on windows: <br>
```shell
python3 ino_with_py.py --sketch /path/to/sketch/sketch.ino --port /dev/ttyS0 -- fqbn arduino:avr:nano
```

### connection to serial communication: 
no further configuration to the system is required for this.<br>
the serial_minitor() method reads the serial communication output on the serial port and outputs it

