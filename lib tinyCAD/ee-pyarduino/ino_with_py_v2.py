import os
import subprocess
import threading
import argparse
import platform
import serial.tools.list_ports
import time
import datetime


def hex_str_to_int(value:str) -> int:
    ''' Convert hexadecimal string to integer
    
    # Parameter
    - value: 
      - string with hex characters 'a' or 'b', e.g. 'abc'

    # Examples
    >>> hex_str_to_int('a')
    10
    >>> hex_str_to_int('0xa')
    10
    >>> hex_str_to_int('ff')
    255
    >>> hex_str_to_int('0xFF')
    255
    '''
    if value.startswith('0x'):
        return int(value,16)
    else:
        return int('0x'+value,16)



class runIno:
    
    
    def __init__(self, file:str, port:str, FQBN:str) -> None:
        
        self.file=file
        self.port=port
        self.FQBN=FQBN
        
        current_platform=platform.system()
        
        if current_platform == "Linux" :
            self.program ="arduino-cli"             # for running on Linux.
        elif current_platform == "Windows":
            self.program ="arduino-cli.exe"         # for running on windows.
        # sre is the serial communication
        self.ser = serial.Serial(port, 9600)
   
    def close(self):    
        self.ser.close() 
        
    def  compile_and_upload(self):
        """compiles a sketch and loads it onto an Aduino board using arduino CLI
           !! make sure arduino CLI is installed on the computer !!

        Raises:
            Raise a value error if the sketch is not define or if the skrtch can't be found
        """
        if self.file == None:
            raise ValueError("Sketch not defined!")
        if not os.path.isfile(self.file):
            raise ValueError("Sketch '{}' does not exist!".format(self.file))
        #close the serial communication to allow the upload of a new sketch
        self.ser.close()  
        #compilation
        compile=[self.program, "compile", "--fqbn", self.FQBN,self.file]
        subprocess.run(compile)
        #upload
        upload=[self.program, "upload","--port",self.port, "--fqbn",self.FQBN,self.file] 
        subprocess.run(upload)
        #re-oppen the serial communication
        self.ser = serial.Serial(self.port, 9600)
      
        
    def read_memory(self, position:int, length:int, data:list[int])-> list[int]:
        """read data of a One wiredevice an return as a list

        Args:
            position (int): start position where the data should be read.the position must be between 0 and 127
            length (int):Length of the data to be read. the leng must be between 1 and 128
            data (list[int]): empty list in which the read data are stored

        Returns:
            list[int]: return a list with the read data 
        """
        
        if position not in range(0,128):
            raise ValueError ("Your position '{}' muss be from 0 to 127!".format(position))
        if length not in range(1,129):
            raise ValueError ("Your length '{}' muss be from 1 to 128!".format(length))
        if (position +length ) > 128:
            raise ValueError ("Your length '{}'is longer than the available memory space!".format(length))
        self.ser.timeout=1
        space=" "
        cmd="01"+space + str(hex(position)) + space +str(hex(length))

        count=0
        while True:
            self.ser.write(cmd.encode())
            time.sleep(1.5)
            res=self.ser.read_until("\n").decode().strip()  
            count+=1
            if count==3 :
                break
        #Save read content in data    
        listRes=res.split()
        data = [hex_str_to_int(x) for x in listRes]
        
        return data
  
       
    def write_memory(self, position:int, data:list[int], check:bool=True) -> bool:   
        """write data to one-wire device

        Args:
            position (int): start position where the data should be written. the position must be between 0 and 127
            data (list[int]):data to be written in a list of int. the list schould have the format [0x01, 0x02, 0x8C, 0xB0, 0x57, 0x4D] for example
            check (bool, optional): Activates or deactivates checking the result. Defaults to True.

        Raises:
            ValueError: raise an error if the written data differs from the data in the memory

        Returns:
            list[int]: return a list of teh written data
        """
        length = len(data)
        if position not in range(0,128):
            raise ValueError ("Your position '{}' muss be from 0 to 127!".format(position))
        if length not in range(1,129):
            raise ValueError ("Your length '{}' muss be from 1 to 128!".format(length))
        if (position + length ) > 128:
            raise ValueError ("Your length '{}'is longer than the available memory space!".format(length))
        
        self.ser.timeout=1
        check_error=[]
        space=" "
        dat =""
        cont=" ".join(format(value, '02X') for value in data).split()
        for d in cont:
            dat += str(d)+space
        cmd="00"+space+ str(hex(position))+ space +str(hex(length))+ space + dat
        
        count=0
        while(True):
            self.ser.write(cmd.encode())
            time.sleep(2)
            # res=self.ser.read_until("\n").decode().strip()    
            count+=1
            if count==3:
                break
            
        # Read the data to check whether exactly the written data is in the memory.
        err = self.read_memory(position, length,check_error)
       
        if check==True:
            if(err!=data):
                raise Exception("something went wrong while writing, please check the command and try again!")
            elif (err==data):
                return True
        else:
            return True
            
       
    def clear_memory(self,check:bool=True)->bool:
        
        """clear all the memory content of a one wire-device

        Args:
            check(bool, optional): Activates or deactivates checking the result. Defaults to True.

        Returns:
            success(bool): return "True" if the checking succesful and "False" otherwise        
        """
        self.ser.timeout=1
        success=False
        count=0
        cmd="02"
        while True:
            self.ser.write(cmd.encode())
            time.sleep(0.1)
            res=self.ser.readline().decode().strip()
            count+=1
            if count==3:
                break
        if check==True:
            if "success" in res:
                return not success
            else:
                raise Exception("something went wrong while clearing, please check the command and try again!")
        else:
            return not success        
       
       
      

# run_file=runIno("C:/Users/Praktikant1/Documents/Arduino/test_com2/test_com2.ino","COM5", "arduino:avr:nano")
# run_file.compile_and_upload()

# # content=[0x01, 0x02, 0x8C, 0xB0, 0x57, 0x4D, 0x74, 0x67, 0x2E, 0xEE, 0x3E, 0x15, 0x42, 0xA3, 0x01, 0xCB]
# run_file.write_memory(0,content)
# run_file.write_memory(0,content,False)

# data=[] 
# print(run_file.read_memory(0,32,data))

# run_file.clear_memory()

# run_file.close()
       




