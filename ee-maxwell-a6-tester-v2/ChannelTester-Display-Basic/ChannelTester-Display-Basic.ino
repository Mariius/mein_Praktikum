#include <Arduino.h>
#include <U8x8lib.h>

// constructor for display
U8X8_SSD1322_NHD_256X64_3W_HW_SPI u8x8(/* cs=*/3);

const uint16_t display_width  = 256;
const uint16_t display_height = 64;

void initDisplay() {
  u8x8.begin();
  u8x8.clearDisplay();
  u8x8.setPowerSave(0);
  u8x8.setFlipMode(1);                        // rotate text 180°
  u8x8.setContrast(255);                      // 0= low contrast, 255 = max contrast
  u8x8.setFont(u8x8_font_artossans8_r);  
}

void setup() {
  initDisplay();
  u8x8.drawString(0, 1, "nopqrstuvwxyz");
  u8x8.drawString(0, 2, "ABCDEFGHIJKLM");
  u8x8.drawString(0, 3, "NOPQRSTUVWXYZ");
  u8x8.drawString(0, 4, "123456789");
}


uint8_t contrast = 1;
int8_t  dir = 1;

// breathe effect on text
void loop() {
  if (( contrast == 0xFF ) || ( contrast == 0x00 ))
    dir *= -1;
  contrast += dir;

  u8x8.setCursor(0,6); 
  u8x8.print(contrast); 
  u8x8.print("  "); 
  u8x8.setContrast ( contrast );
  delay ( contrast ? 1 : 200 );
}
