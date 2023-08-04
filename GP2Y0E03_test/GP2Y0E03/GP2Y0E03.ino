#include <Wire.h>

#define DISTANCE_ADRS 0x5E
#define SENSOR1_ADRS   0x00
#define SENSOR2_ADRS   0x40
#define output_pin A0
#define output_pin2 A2

void setup() {
  // put your setup code here, to run once:
  Wire.begin();      // initialize I2C communication
  delay(1000);
  Serial.begin(9600);    //initialize serial Monitor

}

void loop() {
  // put your main code here, to run repeatedly:

  double distance1;
  byte data0[2]; // to read the Values of distance from the PG2Y0E03 (int = 2 bytes)
  double distance2;
  byte data1[2]; // to read the Values of distance from the PG2Y0E03 (int = 2 bytes)

 //commnunication with sensor 1
  Wire.beginTransmission(byte(SENSOR1_ADRS));  // start communication with GP2Y0E03
  Wire.write(byte(DISTANCE_ADRS));            // Adresse wo den Abstand gespeichert weden soll
  Wire.write(0x5F);
  distance1 = Wire.endTransmission();
  delay(200);
 
  
 //commnunication with sensor 2
  Wire.beginTransmission(byte(SENSOR2_ADRS));  // start communication with GP2Y0E03
  Wire.write(byte(DISTANCE_ADRS));            // Adresse wo den Abstand gespeichert weden soll
  Wire.write(0x5F);
  distance2 = Wire.endTransmission();
  delay(200);
  
  if(distance1==0)
  {
    // die daten von dem Abstand, die in der adresse DISTANCE_ADRS gespeichert wurden, werden gelesen und in data[2] gespeichert
    distance1= Wire.requestFrom(SENSOR1_ADRS,2); // daten vom Sensor anfordern
    data0[0]=Wire.read();    //read the 11th to 4th bits of data  (Distance[11:4], 0x5E)
    data0[1]=Wire.read();    //read the 3th to 0th bits of data   (Distance[4:0] , 0x05F)

    distance1= ((data0[0]*16 + data0[1])/16)/4;  // berechnung des Abstand aus den Daten

    Serial.print("Abstand1 = ");
    Serial.print(distance1);
    Serial.println("cm"); 
    Serial.println((data0[0]*16 + data0[1]));
    int sensorWert = analogRead(output_pin);
    //Serial.print("Wert = ");
    //Serial.println(sensorWert);
    
    delay(1000);

  } 
 else
 {
   Serial.print("error dist = ");
   Serial.println(distance1);
 }
 
 if(distance2==0)
  {
    // die daten von dem Abstand, die in der adresse DISTANCE_ADRS gespeichert wurden, werden gelesen und in data[2] gespeichert
    distance2= Wire.requestFrom(SENSOR2_ADRS,2); // daten vom Sensor anfordern
    data1[0]=Wire.read();    //read the 11th to 4th bits of data  (Distance[11:4], 0x5E)
    data1[1]=Wire.read();    //read the 3th to 0th bits of data   (Distance[4:0] , 0x05F)

    distance2= ((data1[0]*16 + data1[1])/16)/4;  // berechnung des Abstand aus den Daten

    Serial.print("Abstand2 = ");
    Serial.print(distance2);
    Serial.println("cm"); 
    Serial.println((data1[0]*16 + data1[1]));
    
    
    delay(10);

  } 
 else
 {
   Serial.print("error dist2 = ");
   Serial.println(distance2);
 }
 /*
  int sensorWert = analogRead(output_pin2);
  Serial.print("Wert = ");
  Serial.println(sensorWert);
   */
  delay(200);               
  

}
