
#include <OneWireHub.h>
#include <DS2431.h>
#include <DS2406.h>
#include <OneWireCom.h>


constexpr uint8_t pin_onewire  { 10 };



auto hub = OneWireHub(pin_onewire);
auto ds2431 = DS2431(DS2431::family_code, 0x00, 0x00, 0x31, 0x24, 0xDA, 0x00);
auto ds2406 = DS2406(DS2406::family_code, 0x00, 0x00, 0x31, 0x24, 0xF6, 0x00);
// auto dscom=Com(ds2406); 
auto dscom2=OneWireCom(ds2406, Serial);

void setup() {
  pinMode(2, HIGH);
  while(!Serial);
  Serial.begin(9600); // Serielle Kommunikation mit einer Baudrate von 9600 starten
  // hub.attach(ds2431); 
  hub.attach(ds2406); 
  pinMode(2, LOW);
}

void loop() {
  hub.poll();
  dscom2.communicate();
  
}
