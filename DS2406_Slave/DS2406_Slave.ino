/*
  Beispielcode um zwei DS2431 1K-Bit One-Wire EEPROM auf dem Arduino Nano als slave zu emulieren  
  getestet mit dem Maxim DS9481R-3C7+ USB-to-1-Wire-Adapter und OneWireViewer
  
  Verbindung zun Master Gerät:
  * OneWire pin vom arduino Nano (hier pin 10) mit dem Daten Pin verbinden
  * Ground von arduino nano mit Ground von Master Verbinden

  der Code simuliert gleichzeitzig zwei DS2431-Chip (ds2431_1 und ds2431_2) als OneWire Slave 
  und schreibt Daten in den Hauptspeicher von ds2431_1    
  
*/


#include <OneWireHub.h>
#include <DS2431.h>
#include <DS2406.h>
#include <OneWire.h>
constexpr uint8_t pin_onewire  { 10 };


auto hub = OneWireHub(pin_onewire);
auto ds2431_1 = DS2431(DS2431::family_code, 0x00, 0x00, 0x31, 0x24, 0xDA, 0x00);
auto ds2406   = DS2406(DS2406::family_code,  0x00, 0x00, 0x31, 0x24, 0xDA, 0x00);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("OneWire-Hub DS2431");
  Serial.println("Write Hex Data to the first DS2431 (ds2431_1)");

  Serial.println("Write Hex Data to page 0");
  constexpr uint8_t memory[] = { 0xD6, 0x10, 0x8C, 0xB0, 0x57, 0x4D, 0x74, 0x67, 0x2E, 0xEE, 0x3E, 0x15, 0x42, 0xA3, 0x01, 0xCB,
                                 0x41, 0x42, 0x43, 0x44, 0x30, 0x36, 0x00, 0x00, 0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x5F};
  ds2406.writeMemory(memory,sizeof(memory),0x00);

  Serial.println("Write Hex Data to page 1");
  constexpr uint8_t mem_1[] = { 0x4D, 0x75, 0x78, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x0B,
                                0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
  ds2406.writeMemory(mem_1, sizeof(mem_1), 1*32);

  Serial.println("Write Hex Data to page 2");
  constexpr uint8_t mem_2[] = { 0x44, 0x65, 0x66, 0x61, 0x75, 0x6C, 0x74, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x0A, 0x00, 0x10, 0x27, 0x02, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
  ds2406.writeMemory(mem_2, sizeof(mem_2), 2*32);

  Serial.println("Write Hex Data to page 3");
  constexpr uint8_t mem_3[] = { 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF,
                                0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
  ds2406.writeMemory(mem_3, sizeof(mem_3), 3*32);  
  

   // Test-Cases: the following code is just to show basic functions, can be removed any time
    Serial.println("Test - set State of switch 0");
    Serial.println(ds2406.getPinState(0));
    ds2406.setPinState(0,1);
    Serial.println(ds2406.getPinState(0));

    Serial.println("Test - set State of switch 1");
    ds2406.setPinState(1,1);
    Serial.println(ds2406.getPinState(1));

    Serial.println("Test - set Latch of switch 1");
    Serial.println(ds2406.getPinLatch(1));
    ds2406.setPinLatch(1,1);
    Serial.println(ds2406.getPinLatch(1)); // latch is set

    Serial.println("Test - check State of switch 1");
    Serial.println(ds2406.getPinState(1)); // will be zero because of latching
    ds2406.setPinState(1,1);
    Serial.println(ds2406.getPinState(1)); // still zero

    Serial.println("Test - disable latch and set State of switch 1");
    ds2406.setPinLatch(1,0);
    ds2406.setPinState(1,1);
    Serial.println(ds2406.getPinState(1)); // works again, no latching
  // ds2431.clearMemory(); // begin fresh after doing some work

  // Setup OneWire
  hub.attach(ds2431_1);
  hub.attach(ds2406);  
  Serial.println("config done");
   const uint8_t add[]={DS2406::family_code,  0x00, 0x00, 0x31, 0x24, 0xDA, 0x00};
    const uint8_t add1[]={DS2431::family_code,  0x00, 0x00, 0x31, 0x24, 0xDA, 0x00};
   Serial.println(ds2406.crc16(add,16,0x0))   ;
   Serial.println(ds2406.crc16(add1,16,0x0))   ;

}

void loop() {
  // put your main code here, to run repeatedly:
   hub.poll();
 
  
}
