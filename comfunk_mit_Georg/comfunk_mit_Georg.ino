void setup() {
  // put your setup code here, to run once:
   Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  communicate();

}
 
void communicate()
{

    bool DATA_IN=false;

    if(Serial.available()>0){

      String cmdInput = Serial.readStringUntil('\n');
      
      const int maxLength=190; // the three first position are for the command(write, read,..), start position of writing or reading, 
                              // length of byte to write or read and the rest of the buffer ist for the mamory content.

      //String cmdbuffer[maxLength];  
      uint16_t cmdbuffer[maxLength];                   
      int index = 0;
      
      //Serial.print(cmdInput);
      while (cmdInput.length() > 0) {
        DATA_IN=true;
        
        int spaceIndex = cmdInput.indexOf(' ');
        if (spaceIndex != -1) {
          // Extract the part of the string up to the space character
          cmdbuffer[index] = cmdInput.substring(0, spaceIndex).toInt();
          cmdInput = cmdInput.substring(spaceIndex + 1);
          index++;
        }
        else{
          // Save last part of string if no further space is present
          cmdbuffer[index] = cmdInput.toInt();
          break;
        }
      }
    
      
      if(DATA_IN){
        DATA_IN=false;

        for (int i = 0; i < index ; i++) {
            Serial.print(cmdbuffer[i]);
            Serial.print(" ");
        }
        Serial.println(); 
        
        

        if (cmdbuffer[0]==00) {
        //if (cmdbuffer[0]=="wm") {
            Serial.print("write command received\n");

            //int pos=cmdbuffer[1].toInt();
            int pos=cmdbuffer[1];
            Serial.print("Start position: ");
            Serial.println(pos);
            //int length=cmdbuffer[2].toInt();
            int length=cmdbuffer[2];
            Serial.print("length: ");
            Serial.println(length);
            uint8_t memory[length];
            Serial.print("content: ");
            for(int i = 0; i < length; i++){
              
              //memory[i]=strtoul(cmdbuffer[i+3].c_str(), NULL,16);
              memory[i]=cmdbuffer[i+3];
              Serial.print( memory[i]);
              Serial.print(" ");
                
            }
            Serial.println();

            Serial.print("write menory...\n");
              //  m_chip.writeMemory();
            Serial.print("done!\n");
              
        }

        else if (cmdbuffer[0]==01) {
        //else if (cmdbuffer[0]=="rm") {
            Serial.print("read command received\n");

            //int pos=cmdbuffer[1].toInt();
            int pos=cmdbuffer[1];
            Serial.print("Start position: ");
            Serial.println(pos);
            //int length=cmdbuffer[2].toInt();
            int length=cmdbuffer[2];
            Serial.print("length: ");
            Serial.println(length);
            uint8_t readmemory[length];

            Serial.print("read menory...\n");
              //  m_chip->readMemory(readmemory, len, pos);

            for (int j=0; j<length; j++){
                    char str[length];
                    sprintf(str, "%d", readmemory[j]);
                    if (strlen(str)==1) {
                      Serial.print("0");
                    }
                    Serial.print(readmemory[j], HEX);
                    Serial.print(" ");
                  //  if ((len>0) & ((len%32)==0)) {m_serial->print("\n");}
                }  
            Serial.print("done!\n");
              
        }
        else if (cmdbuffer[0]==02) {
        //else if (cmdbuffer[0]=="cl") {
            Serial.print("clear command received\n");
            Serial.print("clear menory...\n");
              //  m_chip.clearMemory();
            Serial.print("done!\n");
            }

        else{
            Serial.print("the command given is incorrect!\n");
            Serial.print("*To read the memory content, please enter 'read memory'.\n");
            Serial.print("*To write the memory, please enter 'write memory'..\n");
            Serial.print("*To clear the memory, please enter 'clear'..\n");

            for (int i = 0; i < index; i++) {
              Serial.print(cmdbuffer[i]);
              Serial.print(" ");
          }
          Serial.println(); 
          
          }
      }
      for(int i=0;i < sizeof(cmdbuffer); i++){
        cmdbuffer[i]=0;
      }
  }
}
