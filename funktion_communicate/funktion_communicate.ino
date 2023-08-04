
#include <OneWireHub.h>
#include <DS2431.h>
#include <DS2406.h>
#include <OneWireItem.h>
#include "com.h"

constexpr uint8_t pin_onewire  { 10 };

auto hub = OneWireHub(pin_onewire);
auto ds2431 = DS2431(DS2431::family_code, 0x00, 0x00, 0x31, 0x24, 0xDA, 0x00); 
Com c=Com(ds2431);
void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);
  
  hub.attach(ds2431);
  MCUSR=0;
  // wdt_disable(); 
}

void loop() {
  // put your main code here, to run repeatedly:
  // communicate(ds2431);
  c.communicate();
  hub.poll();
  

}
 
// void communicate(OneWireItem& d)
// {
//     if(Serial.available()>0){

//       const int maxLength=500; // the three first position are for the command(write, read,..), start position of writing or reading, 
//                               // length of byte to write or read and the rest of the buffer ist for the mamory content.
//       char inputbuffer[maxLength];

//       int readlength = Serial.readBytesUntil('\n', inputbuffer, maxLength - 1);    //readBytesUntil(...) Returns the number of characters to be read including spaces      
//       inputbuffer[readlength] = '\0';         
      
//       int cmdLength=((readlength+2)/3);
//       uint8_t cmdbuffer[cmdLength];
//       char* token;
//       token = strtok(inputbuffer, " ");
//       for (int i = 0; i < readlength; i++) {
//         cmdbuffer[i] = strtoul(token, NULL, 16);
//         token = strtok(NULL, " ");
//       }
//       Serial.println(readlength);
//       Serial.println(cmdLength);
//       Serial.print("command: ");
//       for (int i = 0; i < cmdLength; i++) {
     
//         if(strlen(String(cmdbuffer[i]).c_str())==1) Serial.print("0");
//         Serial.print(cmdbuffer[i],HEX);
//         Serial.print(" ");
//       }
//       Serial.println();
     
//       if (cmdbuffer[0]==00) {

//         Serial.print("write command received\n");

//         uint8_t pos=cmdbuffer[1];
//         Serial.print("Start position: ");
//         Serial.println(pos,HEX);
//         uint8_t length=cmdbuffer[2];
//         Serial.print("length: ");
//         Serial.println(length,HEX);
//         Serial.println(length);
//         uint8_t memory[length];
//         Serial.print("content: ");
//         int i=0;
//         while(i < cmdLength-3){
//           memory[i]=cmdbuffer[i+3];
//           Serial.print( memory[i], HEX);
//           Serial.print(" ");
//           // if (i==(length-1)) break;
//           i++;
//         }

//         Serial.println();

//         Serial.print("write menory...\n");
//         d.writeMemory(memory,length,pos);

//               uint8_t mem[length];
//               int compareCount=0;
//               d.readMemory(mem,length,pos);
//               for (size_t i = 0; i < length; i++) {
//                 if (mem[i]==memory[i]) {
//                   compareCount++;
//                 }
//               }
//               if (compareCount==length) {
//                 Serial.print("done!\n");
//               }
//               else{
//                 Serial.print("something went wrong while writing, please check the command!\n");
//               }
          
//       }

//       else if (cmdbuffer[0]==01) {

//         Serial.print("read command received\n");

//         uint8_t pos=cmdbuffer[1];
//         Serial.print("Start position: ");
//         Serial.println(pos, HEX);
//         uint8_t length=cmdbuffer[2];
//         Serial.print("length: ");
//         Serial.println(length, HEX);
//         uint8_t readmemory[length];

//         Serial.print("read menory...\n");
         

//         for (int j=0; j<length; j++){
//             char str[length];
//             // sprintf(str, "%d", readmemory[j]);
//             // if (strlen(str)==1) {
//             //   Serial.print("0");
//             // }
//             Serial.print(readmemory[j], HEX);
//             Serial.print(" ");
//               //  if ((len>0) & ((len%32)==0)) {Serial.print("\n");}
//             }
//         Serial.println();      
//         Serial.print("done!\n");
          
//       }
//       else if (cmdbuffer[0]==02) {
     
//         Serial.print("clear command received\n");
//         Serial.print("clear menory...\n");
//           //  m_chip.clearMemory();
//         Serial.print("done!\n");
//       }

//       else{
//         Serial.print("the command given is incorrect!\n");
//         Serial.print("*To read the memory content, please enter 'read memory'.\n");
//         Serial.print("*To write the memory, please enter 'write memory'..\n");
//         Serial.print("*To clear the memory, please enter 'clear'..\n");

//         Serial.print("command: ");
//        for (int i = 0; i < cmdLength; i++) {
     
//           if(strlen(String(cmdbuffer[i]).c_str())==1) Serial.print("0");
//           Serial.print(cmdbuffer[i],HEX);
//           Serial.print(" ");
//         }
//       Serial.println();
      
        
//         }
    
//     for(int i=0;i < sizeof(cmdbuffer); i++){
//       cmdbuffer[i]=0;
//     }
//   }
// }

