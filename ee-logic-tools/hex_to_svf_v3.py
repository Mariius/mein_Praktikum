import os
import fnmatch
import argparse as arg

"""
This program is used to convert hexadecimal files into svf files.
(more about the conversion in the convert() function)

How to run the script?

The script can be run in different ways using differents parameters:

>> py hex_to_svf_v3.py --path path\to\the\folder --dest new_file.svf -- frep 1000000
>> py hex_to_svf_v3.py --source file.hex --dest new_file.svf -- frep 1000000
>> py hex_to_svf_v3.py --path path\to\the\folder
>> py hex_to_svf_v3.py --path ..\..\folder
>> py hex_to_svf_v3.py --source file.hex
>> py hex_to_svf_v3.py --source ..\..\file.hex 

if the destinations file and/or the frequency is not specified in the call, the destination file will receive the same name as the source file
and the frequency is set to 10000000 Hz by default
"""
parser=arg.ArgumentParser()
parser.add_argument('--source', type=str, required=False)
parser.add_argument('--dest', type=str, required=False)
parser.add_argument('--freq', type=str, required=False)
parser.add_argument('--path', type=str, required=False)
argument=parser.parse_args()

countHexFiles=0

if argument.path!=None:
 for foundfiles in os.listdir(argument.path):
  #  print(foundfiles)
    if fnmatch.fnmatch(foundfiles, "*.hex"):
        print("hexfile: " + foundfiles)
        countHexFiles+=1
        argument.source = foundfiles
        name, typ=os.path.splitext(foundfiles)
        argument.dest=os.path.join(argument.path, name + ".svf")
        
 print("there are " + str(countHexFiles) + " Hex files  in this directory")    
            
                                                   
def convert(source, destination,freq):
       
   """
   This function opens the source file "source" in read mode  and reads out the data, the data is converted into bytes and then to binary string.
   The order of bits in each byte is inverted (from last to first) and stored in a new list.
   
   then each byte in the batBin list is first converted to decimal and then converted to hex. The hex values will be saved in a new list
   called datHex .
  
   The list of hex values ​​is reversed, newlines are added , and the data is saved in the .svf file
  
   parameters:
  
   - source = File to be converted, of data type .hex
   - destination = File in which the converted data is written, of data type .svf
   - freq= frequency
   
   """
       
   datbin=[]
   datHex=[]
   print("Hex file found...")
   print("conversion...")
   
   #inputs handling
   if source == None:
       raise ValueError("Source not defined!")
   if not os.path.isfile(source):
       raise ValueError("Source file '{}' does not exist!".format(source))
   if freq==None:
       freq="10000000"
   if destination==None:
       destination=source[:-4] + ".svf"                                   # name the destinations file with the same name as the source file and change the data type


   with open(source,"rb") as file:                                        # Open hex file in read mode
      hex_str=file.read()                                                 # Read hex data from file
    
   hex_byte=bytes.fromhex(hex_str.decode())                               # convert hex data to byte
                                                                          # decode--> convert byte to string object
   

   for b in hex_byte:
      bin_str=format(b, "08b")    
      #reverse="{:08b}".format(b)[::-1]                                   # byte TO binary string ("{:08b}.format(b)") or format(b, "08b") , order of each bit in byte is inverted ([::-1])
      reverse=format(b, "08b")[::-1]
      datbin.append(reverse)
        

   endFile=open(destination,"w")                      

   #convertion
   
   for i in datbin:
     dec=int(i,2)                                                        # each byte is first converted into a decimal number
     hex_s=hex(dec)                                                      # from decimal to hexadecimal
     hex_s=hex_s[2:] 
     if len(hex_s)==1:
        hex_s="0"+ hex_s
     datHex.append(hex_s.upper())                                        # hex values ​​are stored in the list "datHex" and Llowercase letters are written in capitals
   cutDatHex=[]
   datHex1=datHex[::-1]                                                  # The list is read from the last character to the first and saved in the new list

   a=0
   while  a < len(datHex1):
     cutDatHex.append(str(datHex1[a]))
     if a>0:
      if a % 12500 == 0 :
        cutDatHex.append("\n    ") 
     a+=1
 
   endFile.write("TRST OFF;")
   endFile.write("\nENDIR IDLE;")
   endFile.write("\nENDDR IDLE;")
   endFile.write("\nSTATE RESET;")
   endFile.write("\nSTATE IDLE;")
   endFile.write("\nFREQUENCY " + freq + " HZ; ")
   endFile.write("\n")
   endFile.write("\nSIR 4 TDI (4);")
   endFile.write("\n")
   endFile.write("\nSDR " + str(len(datHex)*8) +" TDI ")
   endFile.write("(")
   endFile.write("".join(cutDatHex))                                  
   endFile.write(");")
   endFile.write("\n")
   endFile.write("\n// Extra clock ticks in SDR state")
   endFile.write("\nSDR 2000 TDI (00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000);")
   endFile.write("\n")
   endFile.write("\n// Enter user mode")
   endFile.write("\nSIR 4 TDI (7);")
   endFile.write("\nRUNTEST 100 TCK;")
   print("Done!!")
   print("your svf file ist "+ destination)


if countHexFiles==1:
   convert(argument.source, argument.dest, argument.freq)

elif argument.source != None :
    convert(argument.source, argument.dest, argument.freq)
else:
    
    print("There is either more than one hex file or no hex file in this directory ")
    print("please give the name of the file you want to convert as argument ")
  




