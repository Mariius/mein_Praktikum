/*
  Example of code to emulate two  1K-Bit protected 1-Wire EEPROM (DS2431) on the Arduino Nano as a slave.  
  tested with the Maxim DS9481R-3C7+ USB-to-1-Wire adapter and OneWireViewer (compatible with the USB-to-1-Wire adapter)
  
 Used library : OneWireHub
   - the original OneWireHub library does not support the DS2406 chip
   - the original OneWireHub can be downloaded in the library manager

 Connection of the DS2431_Slave (Arduino Nano) to the Master device:
  * Connect the 1-wire pin of the Arduino Nano (can be programmed in any digital pin: here pin 3) to the data pin of the master.
  * Ground from Arduino Nano with Ground from Master Connect

 the following code simulates a DS2431 chip as a 1-Wire slave  and writes data into the main memory of one of the Slave,
 the oder one ist empty.   
  
*/


#include <OneWireHub.h>
#include <DS2431.h>

constexpr uint8_t pin_onewire  { 3 };

auto hub = OneWireHub(pin_onewire);
auto ds2431_1 = DS2431(DS2431::family_code, 0x00, 0x00, 0x31, 0x24, 0xDA, 0x00);
auto ds2431_2 = DS2431(DS2431::family_code, 0x65, 0x00, 0x31, 0x24, 0x55, 0x00);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("OneWire-Hub ds2431_1");
  Serial.println("Write Hex Data to the first ds2431_1 (ds2431_1)");

  Serial.println("Write Hex Data to page 0");
  constexpr uint8_t memory[] = { 0xD6, 0x10, 0x8C, 0xB0, 0x57, 0x4D, 0x74, 0x67, 0x2E, 0xEE, 0x3E, 0x15, 0x42, 0xA3, 0x01, 0xCB,
                                 0x41, 0x42, 0x43, 0x44, 0x30, 0x36, 0x00, 0x00, 0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x5F};
  ds2431_1.writeMemory(memory,sizeof(memory),0x00);

  Serial.println("Write Hex Data to page 1");
  constexpr uint8_t mem_1[] = { 0x4D, 0x75, 0x78, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x0B,
                                0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
  ds2431_1.writeMemory(mem_1, sizeof(mem_1), 1*32);

  Serial.println("Write Hex Data to page 2");
  constexpr uint8_t mem_2[] = { 0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x10, 0x27, 0x02, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
  ds2431_1.writeMemory(mem_2, sizeof(mem_2), 2*32);

  Serial.println("Write Hex Data to page 3");
  constexpr uint8_t mem_3[] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF,
                                0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
  ds2431_1.writeMemory(mem_3, sizeof(mem_3), 3*32);  

  hub.attach(ds2431_1); 
  hub.attach(ds2431_2);
  Serial.println("config done");
}

void loop() {
  // put your main code here, to run repeatedly:
   hub.poll();
}
