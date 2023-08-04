// #include "OneWireCom.h"


OneWireCom::OneWireCom(OneWireItem& ds24,  HardwareSerial& serial)
{
        m_chip= &ds24;
        m_serial=&serial;
}

void OneWireCom::communicate()
{

if(m_serial->available()>0){

  String cmd = m_serial->readString();
  cmd.trim();                           //löscht Leerzeichen vor und nach der Eingabe

  // char cmd=m_serial->read();

    if (cmd=="write memory") {
        m_serial->print("write command received\n");


        m_serial->print("Enter the position: ");
        while (!m_serial->available()>0) {
          // Warte auf die Eingabe des Benutzers
        }
        String p = m_serial->readString();
        int pos=p.toInt();
        m_serial->print(pos);
        m_serial->print("\n");

        uint8_t memory[8]={};
        int bufferSize = 24;
        char inputBuffer[bufferSize];

        m_serial->print("Memory content, separated by spaces: ");
        while (!m_serial->available()>0) {
          // Warte auf die Eingabe des Benutzers
        }
        int bytesRead = Serial.readBytesUntil('\n', inputBuffer, bufferSize - 1);
        // inputBuffer[bytesRead] = '\0';

        uint8_t list[8];
        char* token;

        token = strtok(inputBuffer, " ");
        for (int i = 0; i < 8; i++) {
          list[i] = strtoul(token, NULL, 16);
          token = strtok(NULL, " ");
        }

        // Printing the values to verify the conversion
        for (int i = 0; i < 8; i++) {
          Serial.print("0x");
          if(strlen(String(list[i]).c_str())==1) Serial.print("0");
          Serial.print(list[i],HEX);
          Serial.print(" ");
        }
        for (int i = 0; i < 8; i++) {
          memory[i]=(list[i]);
        }

        m_serial->print("\n");
        m_serial->print("writing menory...\n");
        m_chip->writeMemory(memory,sizeof(memory),pos);
        m_serial->print("done \n");

       }

      else if (cmd=="read memory") {
         m_serial->print("read command received\n");
          // read the a part of the memory content
         m_serial->print("Enter the position: ");
         while (!m_serial->available()>0) {
           // Warte auf die Eingabe des Benutzers
         }
         String p = m_serial->readString();
         int pos=p.toInt();
         m_serial->print(pos);
         m_serial->print("\n");


         m_serial->print("how many Byte do you want to read?: ");
         while (!m_serial->available()>0) {
           // Warte auf die Eingabe des Benutzers
         }
         String l = m_serial->readString();
         int len=l.toInt();
         m_serial->print(len);
         m_serial->print("\n");

         uint8_t readmemory[len];
         m_serial->print("reading menory...\n");
         m_chip->readMemory(readmemory, len, pos);

         for (int j=0; j<len; j++){
              char str[len];
              sprintf(str, "%d", readmemory[j]);
              if (strlen(str)==1) {
                m_serial->print("0");
              }
              m_serial->print(readmemory[j], HEX);
              m_serial->print(" ");
            //  if ((len>0) & ((len%32)==0)) {m_serial->print("\n");}
          }

          for (size_t i = 0; i < count; i++) {
            /* code */
          }



         // // read the complete memory content
         //
         // for (int i = 0; i < 128; i+=32) {
         //   /* code */
         //   uint8_t readmemory[32];
         //   m_chip->readMemory(readmemory, 32, i );
         //
         //   for (int j=0; j<32; j++){
         //
         //      char str[50];
         //      sprintf(str, "%d", readmemory[j]);
         //      if (strlen(str)==1) {
         //        m_serial->print("0");
         //      }
         //      m_serial->print(readmemory[j], HEX);
         //      m_serial->print(" ");
         //  }
         //  m_serial->print("\n");
         // }

         m_serial->print("\n");
         m_serial->print("done!\n");
       }
       else if (cmd=="clear") {
         m_serial->print("clear command received\n");
         m_serial->print("clear menory...\n");
         m_chip->clearMemory();
         m_serial->print("done!\n");
       }
       else{
         m_serial->print("the command given is incorrect!\n");
         m_serial->print("*To read the memory content, please enter 'read memory'.\n");
         m_serial->print("*To write the memory, please enter 'write memory'..\n");
         m_serial->print("*To clear the memory, please enter 'clear'..\n");
       }
}
}

OneWireCom::~OneWireCom()
{
}

// communicate fonction V1
void OneWireCom::communicate()
{
  if(m_serial->available()>0){

  String cmdInput = m_serial->readStringUntil('\n');

  int maxLength=32; // the three first position are for the command(write, read,..), the start position of writing or reading,
                          // and length of byte to write or read. the rest of the buffer ist for the mamory content.

  String cmdbuffer[maxLength];
  int index = 0;

  while (cmdInput.length() > 0) {

    int spaceIndex = cmdInput.indexOf(' ');
    if (spaceIndex != -1) {
      // Extract the part of the string up to the space character
     cmdbuffer[index] = cmdInput.substring(0, spaceIndex);
      cmdInput = cmdInput.substring(spaceIndex + 1);
      index++;
    }
    else{
      // Save last part of string if no further space is present
     cmdbuffer[index] = cmdInput;
      break;
    }
  }
  m_serial->print("command: ");
  for (int i = 0; i <= index; i++) {
      m_serial->print(cmdbuffer[i]);
      m_serial->print(" ");
    }
    m_serial->println();

  if (cmdbuffer[0]=="wm") {
      m_serial->print("write command received\n");

      int pos=cmdbuffer[1].toInt();
      m_serial->print("Start position: ");
      m_serial->println(pos);
      int length=cmdbuffer[2].toInt();
      m_serial->print("length: ");
      m_serial->println(length);
      uint8_t memory[length];
      m_serial->print("content: ");
      for(int i = 0; i < length; i++){

        memory[i]=strtoul(cmdbuffer[i+3].c_str(), NULL,16);
        m_serial->print( memory[i],HEX);
        m_serial->print(" ");

      }
      m_serial->println();

      m_serial->print("write menory...\n");
      m_chip->writeMemory(memory,length,pos);
      m_serial->print("done!\n");

  }

  else if (cmdbuffer[0]=="rm") {
      m_serial->print("read command received\n");

      int pos=cmdbuffer[1].toInt();
      m_serial->print("Start position: ");
      m_serial->println(pos);
      int length=cmdbuffer[2].toInt();
      m_serial->print("length: ");
      m_serial->println(length);
      uint8_t readmemory[length];

      m_serial->print("read menory...\n");
      m_chip->readMemory(readmemory, length, pos);
      m_serial->print("content: \n");
      for (int j=0; j<length; j++){
              char str[length];
              sprintf(str, "%d", readmemory[j]);
              if (strlen(str)==1) {
                m_serial->print("0");
              }
              m_serial->print(readmemory[j], HEX);
              m_serial->print(" ");
            //  if ((len>0) & ((len%32)==0)) {m_serial->print("\n");}
          }
      m_serial->println();
      m_serial->print("done!\n");

  }
  else if (cmdbuffer[0]=="cm") {
       m_serial->print("clear command received\n");
       m_serial->print("clear menory...\n");
       m_chip->clearMemory();
       m_serial->print("done!\n");
       }
  else{
      m_serial->print("the command given is incorrect!\n");
      m_serial->print("*To read the memory content, please enter 'read memory'.\n");
      m_serial->print("*To write the memory, please enter 'write memory'..\n");
      m_serial->print("*To clear the memory, please enter 'clear'..\n");
       }
}
