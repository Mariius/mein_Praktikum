/*
  Example of code to emulate a 1-Wire Dual Switch with 1K-bit memory (DS2406) on the Arduino Nano as a slave.  
  tested with the Maxim DS9481R-3C7+ USB-to-1-Wire adapter and OneWireViewer (compatible with the USB-to-1-Wire adapter)
  
 Used library : OneWireHub
   - the original OneWireHub library does not support the DS2406 chip
   to enulate the DS2406 using the OneWireHub library , we have forked the original repository https://github.com/orgua/OneWireHub 
   to https://github.com/bauergeorg/OneWireHub and extend the folder "src" by the files DS2406.h and DS2406.cpp where the functionnatities of the DS2406-Chip are implemented.

     * the original OneWireHub can be downloaded in the library manager
     * the extended OneWireHub library (with support for DS2406) can be used by cloning the repository 
       https://github.com/bauergeorg/OneWireHub and saving the folder under Arduino\libraries, where the other arduino libraries are. 

 Connection of the DS2406_Slave (Arduino Nano) to the Master device:
  * Connect the 1-wire pin of the Arduino Nano (can be programmed in any digital pin: here pin 3) to the data pin of the master.
  * Ground from Arduino Nano with Ground from Master Connect

 the following code simulates a DS2406 chip as a 1-Wire slave  and writes data into the main memory    

*/


#include <OneWireHub.h>
#include <DS2406.h>


constexpr uint8_t pin_onewire  {10 };

auto hub = OneWireHub(pin_onewire);
auto ds2406 = DS2406(DS2406::family_code, 0xD5, 0x59, 0xE9, 0x00, 0x00, 0x00);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("OneWire-Hub DS2406");
  Serial.println("Write Hex Data to the DS2406-Slave");

  Serial.println("Write Hex Data to page 0");
  constexpr uint8_t memory[] = {0xD1, 0xA8, 0x42, 0xB6, 0xC7, 0x70, 0x58, 0x0A, 0xDA, 0xE2, 0x7E, 0x12, 0x83, 0x86, 0x9A, 0x62,
                                0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x00, 0x00, 0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x5F };
  ds2406.writeMemory(memory,sizeof(memory),0x00);

  Serial.println("Write Hex Data to page 1");
  constexpr uint8_t mem_1[] = {0x52, 0x6F, 0x74, 0x6F, 0x72, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x0D,
                               0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
  ds2406.writeMemory(mem_1, sizeof(mem_1), 1*32);

  Serial.println("Write Hex Data to page 2");
  constexpr uint8_t mem_2[] = {0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                               0x00, 0x00, 0x00, 0x0A, 0x00, 0x0A, 0x88, 0x13, 0x10, 0x27, 0xE8, 0x03, 0x64, 0x00, 0xC8, 0x00};
  ds2406.writeMemory(mem_2, sizeof(mem_2), 2*32);

  Serial.println("Write Hex Data to page 3");
  constexpr uint8_t mem_3[] = { 0x0A, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF,
                                0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
 ds2406.writeMemory(mem_3, sizeof(mem_3), 3*32);  

 hub.attach(ds2406);
 Serial.println("config done");
}

void loop() {
  // put your main code here, to run repeatedly:
   hub.poll();
}
