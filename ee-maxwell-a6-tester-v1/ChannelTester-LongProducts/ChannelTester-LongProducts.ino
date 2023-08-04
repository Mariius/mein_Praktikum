#include <Arduino.h>
#include <U8x8lib.h>
#include <SPI.h>

// constructor for display
U8X8_SSD1322_NHD_256X64_3W_HW_SPI u8x8(/* cs=*/3);

#define BIT(n) (1 << n)

// --- ---------------------------------------------------------------------------------------

struct io_ty 
{
  int sflt   = 0;
  int rec_a  = 0;
  int rec_b  = 0;
  int trg    = 0;
  int in     = 0;
  int out    = 0;
} io_pl600;

const int pin_cs_port_ext       = 10;  // CS1
//const int pin_cs_oled_displ     =  3;  // CS0
const int pin_reca_high         =  6;  // switch_reca_high
const int pin_reca_low          =  7;  // switch_reca_low
const int pin_recb_high         =  8;  // switch_recb_high
const int pin_recb_low          =  9;  // switch_recb_low
const int pin_trg               =  5;  // CHM600_SNS_TRG+
const int pin_pushbutton1       =  2;  // SW1
const int pin_pushbutton2       = A6;  // SW2
const int pin_pushbutton3       = A7;  // SW3
const int pin_pl600_out0        = A0;  // CHM_OUT_0
const int pin_pl600_out1        = A1;  // CHM_OUT_1
const int pin_pl600_out2        = A2;  // CHM_OUT_2
const int pin_pl600_out3        = A3;  // CHM_OUT_3
const int pin_pl600_out4        = A4;  // CHM_OUT_4
const int pin_pl600_out5        = A5;  // CHM_OUT_5

// --- ---------------------------------------------------------------------------------------


void isr_pushbutton1 ( )
{
  Serial.println( "Button SW1 Pressed" );
  return;
}


void isr_pl600_out0 ( )
{
  
  return;
}

void isr_pl600_out1 ( )
{
  
  return;
}

void isr_pl600_out2 ( )
{
  
  return;
}

void isr_pl600_out3 ( )
{
  
  return;
}

void isr_pl600_out4 ( )
{
  
  return;
}

void isr_pl600_out5 ( )
{
  
  return;
}


void isr_init ( )
{
  attachInterrupt(digitalPinToInterrupt(pin_pushbutton1), isr_pushbutton1, FALLING);
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out0) , isr_pl600_out0,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out1) , isr_pl600_out1,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out2) , isr_pl600_out2,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out3) , isr_pl600_out3,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out4) , isr_pl600_out4,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out5) , isr_pl600_out5,  RISING );

  return;
}

void display_init ( )
{
  u8x8.begin();
  u8x8.clearDisplay();
  u8x8.setPowerSave(0);
  u8x8.setFlipMode(1);                        // rotate text 180°
  u8x8.setContrast(255);                      // 0= low contrast, 255 = max contrast
  u8x8.setFont(u8x8_font_artossans8_r);  
}



void pins_init ( )
{
  pinMode(pin_reca_high   , OUTPUT);
  pinMode(pin_reca_low    , OUTPUT);
  pinMode(pin_recb_high   , OUTPUT);
  pinMode(pin_recb_low    , OUTPUT);
  
  pinMode(pin_trg         , OUTPUT);
  pinMode(pin_pushbutton1 ,  INPUT_PULLUP); // pressed -> digital read = 0; ISR
  pinMode(pin_pushbutton2 ,  INPUT);        // pressed -> analog  read < 100
  pinMode(pin_pushbutton3 ,  INPUT);        // pressed -> analog  read < 100
  pinMode(pin_pl600_out0  ,  INPUT);
  pinMode(pin_pl600_out1  ,  INPUT);
  pinMode(pin_pl600_out2  ,  INPUT);
  pinMode(pin_pl600_out3  ,  INPUT);
  pinMode(pin_pl600_out4  ,  INPUT);
  pinMode(pin_pl600_out5  ,  INPUT);  

  isr_init ( );
  return;   
}





// --- ---------------------------------------------------------------------------------------

void port_ext_init (  ) 
{
  SPI.setClockDivider(SPI_CLOCK_DIV2);
  pinMode ( pin_cs_port_ext, OUTPUT );
  digitalWrite ( pin_cs_port_ext, HIGH );

  digitalWrite ( pin_cs_port_ext, LOW );
  delay ( 1 );
  SPI.transfer ( 0x40 ); 
  SPI.transfer ( 0x09 );
  SPI.transfer ( (BIT(5) + BIT(6)) );
  delay ( 1 );
  digitalWrite ( pin_cs_port_ext, HIGH );

  delay ( 1 );
    
  digitalWrite ( pin_cs_port_ext, LOW );
  delay ( 1 );
  SPI.transfer ( 0x40 ); 
  SPI.transfer ( 0x00 );
  SPI.transfer ( 0x00 );
  delay ( 1 );
  digitalWrite ( pin_cs_port_ext, LOW );
  
  return;
}

// --- ---------------------------------------------------------------------------------------

/*
void oled_displ_init ( )
{
  pinMode ( pin_cs_oled_displ, OUTPUT );
  digitalWrite ( pin_cs_oled_displ, HIGH );  
  return;
}
*/

// --- ---------------------------------------------------------------------------------------


void update_pl600_inputs ( )
{
    uint8_t data = ( (io_pl600.in   & BIT(0)) ? BIT(4) :  0 ) + 
                 ( (io_pl600.in   & BIT(1)) ? BIT(3) :  0 ) +
                 ( (io_pl600.in   & BIT(2)) ? BIT(2) :  0 ) +
                 ( (io_pl600.in   & BIT(3)) ? BIT(1) :  0 ) +
                 ( (io_pl600.in   & BIT(4)) ? BIT(0) :  0 ) +
                 ( (io_pl600.sflt & BIT(0)) ?      0 : (BIT(5) + BIT(6)) ) ;
  
  digitalWrite ( pin_cs_port_ext, LOW );
  SPI.transfer ( 0x40 ); 
  SPI.transfer ( 0x09 );
  SPI.transfer ( data );
  digitalWrite ( pin_cs_port_ext, HIGH );
  
  return;  
}





void update_pl600_outputs ( ) 
{
  io_pl600.out = ( digitalRead ( A0 ) * BIT ( 0 ) ) +
                 ( digitalRead ( A1 ) * BIT ( 1 ) ) +
                 ( digitalRead ( A2 ) * BIT ( 2 ) ) +
                 ( digitalRead ( A3 ) * BIT ( 3 ) ) +
                 ( digitalRead ( A4 ) * BIT ( 4 ) ) +
                 ( digitalRead ( A5 ) * BIT ( 5 ) ) ;
  return;
}





void update_pl600_receivers ( )
{
  digitalWrite( 7 , (io_pl600.rec_a & 1) );
  digitalWrite( 6 , (io_pl600.rec_a & 2) >> 1 );

  digitalWrite( 9 , (io_pl600.rec_b & 1) );
  digitalWrite( 8 , (io_pl600.rec_b & 2) >> 1 );  
  return;
}





void update_ios( ) 
{
  update_pl600_inputs ( );
  update_pl600_receivers ( );
  update_pl600_outputs ( );
  return;
}





// === =======================================================================================
// ### #######################################################################################
// === =======================================================================================

uint32_t counter = 0;

const uint32_t value_counter_max = 10000;
// io_pl600.in3,4 == wayA, wayB

const uint32_t value_global_on_start =     0;  // io_pl600.in0
const uint32_t value_refon_start     =  1000;  // io_pl600.in1

const uint32_t value_rec_a_start     = 10000;  // io_pl600.rec_a
const uint32_t value_rec_a_end       = 15000;  // io_pl600.rec_a

  
const uint32_t value_refon_end       = 6000;
const uint32_t value_global_on_end   = value_counter_max - 1;


void setup() 
{
  delay ( 2000 ); // always put a delay here
  Serial.begin ( 9600 );
  //SPI.begin ( );  
  u8x8.begin(); // Display
  port_ext_init ( );
  //oled_displ_init ( );
  pins_init ( );
  delay ( 2000 ); // always put a delay here  
  display_init ( );
  
  u8x8.setCursor(0,0); 
  u8x8.print("Long Products Test is running");  
  u8x8.setCursor(0,5); 
  u8x8.print("Cnt:");
  u8x8.setCursor(16,5); 
  u8x8.print(" / ");
  u8x8.print( value_counter_max );
  u8x8.print("          ");
}

// === =======================================================================================
// === =======================================================================================




void loop() 
{
  io_pl600.in    = 0;
  io_pl600.in   += ((counter >= value_global_on_start ) && ( counter < value_global_on_end )) ? BIT(0) : 0;
  io_pl600.in   += ((counter >= value_refon_start     ) && ( counter < value_refon_end     )) ? BIT(1) : 0;
  io_pl600.rec_a = ((counter >= value_rec_a_start     ) && ( counter < value_rec_a_end     )) ?      3 : 0;
  

 
  io_pl600.in +=  BIT(3);
  update_pl600_inputs ( );
  
  io_pl600.in +=  BIT(4);
  update_pl600_inputs ( );
  
  io_pl600.in -=  BIT(3);
  update_pl600_inputs ( );

  io_pl600.in -=  BIT(4);
  update_pl600_inputs ( );
  
//delayMicroseconds (100); // max 16383

  counter += 1;
  if ( counter >= value_counter_max )
  {
    counter = 0;
    delay(1000);
  }
  u8x8.setCursor(9,5); 
  u8x8.print(counter);

  u8x8.setCursor(14,7); 
  if ((counter >= value_refon_start ) && ( counter < value_refon_end ))
    u8x8.print("Ref On");  
  else
    u8x8.print("      ");  
}
