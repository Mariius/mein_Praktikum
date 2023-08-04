void ASCIIByteToHexByte(String c[], String res[] ){
  static int i=0;
     while(true) {
       /* code */
         if (c=="48") {res[i] = "0";}
         else if (c[i]=="48") {res[i] = "0";}
         else if (c[i]=="49") {res[i] = "1";}
         else if (c[i]=="50") {res[i] = "2";}
         else if (c[i]=="51") {res[i] = "3";}
         else if (c[i]=="52") {res[i] = "4";}
         else if (c[i]=="53") {res[i] = "5";}
         else if (c[i]=="54") {res[i] = "6";}
         else if (c[i]=="55") {res[i] = "7";}
         else if (c[i]=="56") {res[i] = "8";}
         else if (c[i]=="57") {res[i] = "9";}
         else if (c[i]=="65") {res[i] = "A";} // A
         else if (c[i]=="66") {res[i] = "B";} // B
         else if (c[i]=="67") {res[i] = "C";} // C
         else if (c[i]=="68") {res[i] = "D";} // D
         else if (c[i]=="69") {res[i] = "E";} // E
         else if (c[i]=="70") {res[i] = "F";} // F
         else {res[i] = "UN";}
         i+=1;
         if(i>sizeof(c)) break;

    }
}


int HexStringToBytes(const char *hexStr,
                 unsigned char *output,
                 unsigned int *outputLen) {
size_t len = strlen(hexStr);
if (len % 2 != 0) {
return -1;
}
size_t finalLen = len / 2;
*outputLen = finalLen;
for (size_t inIdx = 0, outIdx = 0; outIdx < finalLen; inIdx += 2, outIdx++) {
if ((hexStr[inIdx] - 48) <= 9 && (hexStr[inIdx + 1] - 48) <= 9) {
  goto convert;
} else {
  if ((hexStr[inIdx] - 65) <= 5 && (hexStr[inIdx + 1] - 65) <= 5) {
    goto convert;
  } else {
    *outputLen = 0;
    return -1;
  }
}
convert:
output[outIdx] =
    (hexStr[inIdx] % 32 + 9) % 25 * 16 + (hexStr[inIdx + 1] % 32 + 9) % 25;
}
output[finalLen] = '\0';
return 0;
}
