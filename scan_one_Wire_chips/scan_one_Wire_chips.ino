#include <OneWire.h>

#define chipPin 2

OneWire ds(chipPin);
   byte addr[8];
void scanBus(){

  if (ds.search(addr)){
    Serial.print("One-Wire Bauteil gefunden! Adresse: ");
    for(byte i=0; i<8; i++){
      if(addr[i]<16){
        Serial.print("0");
      }
      Serial.print(addr[i],HEX);
      if(i<7){
       Serial.print("-");
      }
    }

    Serial.println();
  }
  else
  {
    Serial.println("no device found ");
  }

  ds.reset_search();
  delay(1000);
 
}


void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
   
}

void loop() {
  // put your main code here, to run repeatedly:
 scanBus();
 
}
