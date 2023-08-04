#include <Wire.h>

#define DISTANCE_ADRS 0x5E

#define SENSOR_ADRS   0x40

void setup() {
  // put your setup code here, to run once:
  Wire.begin();      // initialize I2C communication
  delay(1000);
  Serial.begin(9600);    //initialize serial Monitor

}

void loop() {
  // put your main code here, to run repeatedly:
  double distance1;
  byte data0[2]; //
  Wire.beginTransmission(byte(SENSOR_ADRS));  // start communication with GP2Y0E03
  Wire.write(byte(DISTANCE_ADRS));            // Adresse wo den Abstand gespeichert weden soll
  distance1 = Wire.endTransmission();
  delay(200); 
  if(distance1==0)
  {
    // die daten von dem Abstand, die in der adresse DISTANCE_ADRS gespeichert wurden, werden gelesen und in data[2] gespeichert
    distance1= Wire.requestFrom(SENSOR_ADRS,2); // daten vom Sensor anfordern
    data0[0]=Wire.read();    //read the 11th to 4th bits of data  (Distance[11:4], 0x5E)
    data0[1]=Wire.read();    //read the 3th to 0th bits of data   (Distance[4:0] , 0x05F)

    distance1= ((data0[0]*16 + data0[1])/16)/4;  // berechnung des Abstand aus den Daten

    Serial.print("Abstand1 = ");
    Serial.print(distance1);
    Serial.println("cm"); 
    Serial.println((data0[0]*16 + data0[1]));
    //  int sensorWert = analogRead(output_pin);
    //Serial.print("Wert = ");
    //Serial.println(sensorWert);
    
    delay(1000);

  } 
 else
 {
   Serial.print("error dist = ");
   Serial.println(distance1);
 }

}
