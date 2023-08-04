/*
  Example of code to emulate two 1-Wire Dual Switch with 1K-bit memory (DS2406) on the Arduino Nano as a slave.  
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

 the following code simulates a DS2406 chip as a 1-Wire slave  and writes data into the main memory of one of the Slave,
 the oder one ist empty.
*/


#include <OneWireHub.h>
#include <DS2406.h>

constexpr uint8_t pin_onewire  { 3 };

auto hub = OneWireHub(pin_onewire);
auto DS2406_1 = DS2406(DS2406::family_code, 0xC8, 0xD1, 0xD4, 0x00, 0x00, 0x00);
auto DS2406_2 = DS2406(DS2406::family_code, 0xD6, 0x10, 0x8C, 0xB0, 0x57, 0x4D);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("OneWire-Hub DS2406");
  Serial.println("Write Hex Data to the first DS2406 (DS2406_1)");

  Serial.println("Write Hex Data to page 0");
  constexpr uint8_t memory[] = { 0x08, 0x0C, 0xB0, 0x00, 0xCA, 0xD4, 0x01, 0x44, 0x06, 0x08, 0xE9, 0x09, 0xA8, 0x00, 0x10, 0x0A,
                                0x41, 0x42, 0x43, 0x44, 0x30, 0x34, 0x00, 0x00, 0x40, 0x20, 0x44, 0x21, 0x31, 0x24, 0x30, 0x11};
  DS2406_1.writeMemory(memory,sizeof(memory),0x00);

  Serial.println("Write Hex Data to page 1");
  constexpr uint8_t mem_1[] = {  0x04, 0x31, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01 , 0x00, 0x00, 0x0B,
                                 0x40, 0x44, 0x40, 0x21, 0x31, 0x20, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
  DS2406_1.writeMemory(mem_1, sizeof(mem_1), 1*32);

  Serial.println("Write Hex Data to page 2");
  constexpr uint8_t mem_2[] = {0x40, 0x25, 0x22, 0x21, 0x34, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x08, 0x00, 0x10, 0x21, 0x02, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF   };
  DS2406_1.writeMemory(mem_2, sizeof(mem_2), 2*32);

  Serial.println("Write Hex Data to page 3");
  constexpr uint8_t mem_3[] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF,
                                0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
  DS2406_1.writeMemory(mem_3, sizeof(mem_3), 3*32);  

  hub.attach(DS2406_1);
  hub.attach(DS2406_2);  
  Serial.println("config done");
}

void loop() {
  // put your main code here, to run repeatedly:
   hub.poll();
}
