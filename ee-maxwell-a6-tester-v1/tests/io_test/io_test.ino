#include <Arduino.h>
#include <U8x8lib.h>
#include <SPI.h>
#define BIT(n) (1 << n)

U8X8_SSD1322_NHD_256X64_3W_HW_SPI u8x8(/* cs=*/ 3);

const int pin_cs_port_ext       = 10;  // CS1
//const int pin_cs_oled_displ   =  3;  // CS0
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

struct io_ty 
{
  int sflt   = 0;
  int rec_a  = 0;
  int rec_b  = 0;
  int trg    = 0;
  int in     = 0;
  int out    = 0;
} io_pl600;

// --- ---------------------------------------------------------------------------------------

int compCounter = 1;

void stop_pushbutton1 ( )
{    
  bool old_value = HIGH;
  bool new_value = digitalRead(pin_pushbutton1);

  if(new_value)
  {
    //u8x8.drawString (7, 3,"SW1 NOT PRESSED");
    TIMSK1 |= 1<<OCIE1A;  // activate interrupt for timer 1: Lauflicht
  }
  else 
  {
   //u8x8.drawString (7, 3,"SW1 PRESSED    ");
   TIMSK1 = 0;   // deactivate interrupt for timer 1: Lauflicht
             
  }  
   
  return;
}

void decreaseSpeed_pushbutton2 ( )
{
  static int old_value0_b2 = 0;                    // 2. Wert
  static int old_value1_b2 = 0;                   // 3. Wert
  int level= 500;     
  int new_value_b2 = analogRead(pin_pushbutton2); // 1. Wert
  //static int static_pressed = 0;
  //static int edge_pressed = 0;
  //static int edge_unpressed = 0;
  
  //stattic not pressed
  if((new_value_b2 > level) & (old_value0_b2 > level) & (old_value1_b2 > level))
   {
    //u8x8.drawString (7, 4,"SW2 NOT PRESSED");      
   }
  //static pressed 
  else if((new_value_b2 < level) & (old_value0_b2 <level) && (old_value1_b2 <level))
  {          
    //u8x8.drawString (7, 4,"SW2 PRESSED    ");  
  }
  // edge pressed
  else if((new_value_b2 < level) & (old_value0_b2 < level) & (old_value1_b2 > level))
    { 
     //edge_pressed++;
     //Serial.print("SW2 edge_pressed:  " );  
     //Serial.println(edge_pressed);          
     compCounter+=1;                            //increase the value of compCounter to decrease the speed of LEDS
     Serial.println( "dec" );
     //Serial.print( compCounter );
     //Serial.println( "ms,  " );       
    }
  // edge unpressed
  else if((new_value_b2 > level) & (old_value0_b2 > level) & (old_value1_b2 < level))
    { 
     //edge_unpressed++;
     //Serial.print("SW2 edge_unpressed:  " );  
     //Serial.println(edge_unpressed);    
    }

  // save old values  
  old_value1_b2 = old_value0_b2;  
  old_value0_b2 = new_value_b2;
  
  return;
}
void increaseSpeed_pushbutton3 ( )
{
  static int old_value0 = 0;                   // 2. Wert
  static int old_value1 = 0;                   // 3. Wert
  int level = 500;     
  int new_value = analogRead(pin_pushbutton3); // 1. Wert
  //static int static_pressed = 0;
  //static int edge_pressed = 0;
  //static int edge_unpressed = 0;
      
  // static not pressed
  if((new_value > level) & (old_value0 > level) & (old_value1 > level) )
   {
    //u8x8.drawString (7, 5,"SW3 NOT PRESSED"); 
   }
  // static pressed
  else if((new_value < level) & (old_value0 < level) & (old_value1 < level))
    {      
     //static_pressed++;
     //Serial.print("static_pressed:  " );  
     //Serial.println(static_pressed);
     //u8x8.drawString (7, 5,"SW3 PRESSED    ");            
    }
  // edge pressed
  else if((new_value < level) & (old_value0 < level) & (old_value1 > level))
    { 
     //edge_pressed++;
     //Serial.print("SW3 edge_pressed:  " );  
     //Serial.println(edge_pressed);          
     compCounter-=1;                                //decrease the value of compCounter to increase the speed of LEDS
     Serial.println( "inc" );
     //Serial.print( compCounter );
     //Serial.println( "ms,  " );       
    }
  // edge unpressed
  else if((new_value > level) & (old_value0 > level) & (old_value1 < level))
    { 
     //edge_unpressed++;
     //Serial.print("SW3 edge_unpressed:  " );  
     //Serial.println(edge_unpressed);    
    }

  // save old values  
  old_value1 = old_value0;  
  old_value0 = new_value;
   
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
  //attachInterrupt(digitalPinToInterrupt(pin_pushbutton1), isr_pushbutton1, FALLING);  
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out0) , isr_pl600_out0,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out1) , isr_pl600_out1,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out2) , isr_pl600_out2,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out3) , isr_pl600_out3,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out4) , isr_pl600_out4,  RISING );
//attachInterrupt(digitalPinToInterrupt(pin_pl600_out5) , isr_pl600_out5,  RISING );

  return;
}


// Timer 1 ISR: Lauflicht
ISR(TIMER1_COMPA_vect)
{
  static int counter=0; 
  counter++;
  if (compCounter < 1)
  {
    compCounter = 1;  
  }
  else if (compCounter > 200)
  {
    compCounter = 200;  
  }

  if (counter >= compCounter) //control the speed of LEDs
   {
      // lauflicht 
      static int index=1;   
      io_pl600.in=index;
      index=index*2;
      if(index>=32) // index= [1, 2, 4,8,16] bit von LED zustände.
      {
         index=1;
      }      
      update_pl600_inputs ( );
      
      //counter zusrücksetzen
      counter=0;
    }
}

 


// Timer 2 ISR: Entprellung
ISR(TIMER2_COMPA_vect)
{
  stop_pushbutton1();
  decreaseSpeed_pushbutton2();
  increaseSpeed_pushbutton3();  
}



void pins_init ( )
{
  pinMode(pin_reca_high   , OUTPUT);
  pinMode(pin_reca_low    , OUTPUT);
  pinMode(pin_recb_high   , OUTPUT);
  pinMode(pin_recb_low    , OUTPUT);
  
  pinMode(pin_trg          , OUTPUT);
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
  SPI.transfer ( 0x42 ); 
  SPI.transfer ( 0x09 );
  SPI.transfer ( (BIT(5) + BIT(6)) );
  delay ( 1 );
  digitalWrite ( pin_cs_port_ext, HIGH );

  delay ( 1 );
    
  digitalWrite ( pin_cs_port_ext, LOW );
  delay ( 1 );
  SPI.transfer ( 0x42 ); 
  SPI.transfer ( 0x00 );
  SPI.transfer ( 0x00 );
  delay ( 1 );
  digitalWrite ( pin_cs_port_ext, LOW );
  
  return;
}

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
  SPI.transfer ( 0x42 ); 
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

void setup() {
  delay ( 2000 );                             // always put a delay here, power up components
  Serial.begin ( 9600 );
  u8x8.begin ( );                             // Display
  port_ext_init ( );
  pins_init ( );
  delay ( 2000 );                             // always put a delay here  
  
  u8x8.setPowerSave ( 0 );
  u8x8.setFlipMode ( 180 );                      // rotate display 180°
  u8x8.setContrast ( 200 );  
  u8x8.setFont ( u8x8_font_artossans8_r );
  u8x8.drawString ( 7, 0, "FastSort Simulator" );  

  digitalWrite(pin_pushbutton1, HIGH);
  //digitalWrite(pin_pushbutton3, HIGH);

  uint8_t c;
  u8x8.setCursor ( c, 1 );
  for(c = 0; c < 32; c++ )
  {
    u8x8.print ( "_" );
  }
 //--------------------------------------------------------------
 cli(); //noInterrupts();

 //configure timer 1 interrupt: timer1 = 16bit: Lauflicht
 TCCR1A = 0;  // Reset entire TCCR1A to 0 
 TCCR1B = 0;  // Reset entire TCCR1B to 0
 TCCR1B |= 1<<CS12 |0<<CS11 |1<<CS10;   // Set CS12 to 1 and CS10 to 0 so we get prescalar 1024
 TCCR1B |= 1<<WGM12;                    // Set WGM12 to 1 so we get CTC Mode
 TCNT1  = 0;  // Reset counter
 TIMSK1 |= 1<<OCIE1A;                 // activate interrupt for timer 1
 // OCR1A = ((F_clock / prescaler) / Fs) - 1 = 1561 with Fs=10Hz and F_clock=16MHz
 OCR1A = 1561; // timer 10Hz --> 100ms

 //--------------------------------------------------------------


 //configure timer 2 interrupt: timer2 = 8bit: Entprellung
 TCCR2A = 0;          // Reset entire TCCR2A to 0 
 TCCR2A |= 1<<WGM21;  // Set WGM20 to 1 so we get CTC Mode
 TCCR2B = 0;          // Reset entire TCCR2B to 0
 TCCR2B |= 1<<CS22 |1<<CS21 |1<<CS20;  // Set CS12 to 1 so we get prescalar 1024
 TCNT2 = 0;          // Reset counter
 // OCR2A = ((F_clock / prescaler) / Fs) - 1 = 155 with Fs=61Hz
 OCR2A = 255; //timer 61Hz --> 16ms
 TIMSK2 |= 1<<OCIE2A;  // activate interrupt for timer 2

 sei(); //interrupts()

}

void loop() {
 
  


}

