#include <Arduino.h>
#include <U8x8lib.h>
#include <SPI.h>
#define BIT(n) (1 << n)

U8X8_SSD1322_NHD_256X64_3W_HW_SPI u8x8(/* cs=*/ 3);

// -------------------------------------------------------------------------------------------------------------------------
// --- modify here if needed >>> -------------------------------------------------------------------------------------------
static int cnt_cycles_max=1000;
int cnt_cycles=0;
int cnt_good=0;
int cnt_bad=0;
int cnt_eval_total=0;
int cnt_eval_good=0;
int cnt_eval_bad=0;

// --- <<< modify here if needed -------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------------------------










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


void isr_pushbutton1 ( )
{
  // Serial.println( "Button SW1 Pressed" );
 
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





void evaluate( )
{
  do
  {
    update_pl600_outputs ( );
  } while ( (io_pl600.out & 0x08) == 0 );

  delay(2); // avoid race conditions;
  update_pl600_outputs ( );
  if ( (io_pl600.out & 0x30) == 0x30 )
    cnt_eval_good++;
  else
    cnt_eval_bad++;
  
  do
  {
    update_pl600_outputs ( );
  } while ( (io_pl600.out & 0x08) != 0 );
  
  return;
}





void air( )
{
  io_pl600.rec_a=0;
  update_pl600_receivers();
  return;
}





void good_part( )
{
  io_pl600.rec_a=1;
  update_pl600_receivers();
  delay(1000);
  air();
  //delay(2000);
  cnt_good++;
  u8x8.setCursor ( 15, 5 );
  u8x8.print( (cnt_good+cnt_bad) );
  u8x8.setCursor ( 15, 6 );
  u8x8.print( cnt_good );
  
  evaluate();
  u8x8.setCursor ( 25, 5 );
  u8x8.print( cnt_eval_good + cnt_eval_bad );  
  u8x8.setCursor ( 25, 6 );
  u8x8.print( cnt_eval_good );  
  return;  
}





void bad_part( )
{
  io_pl600.rec_a=3;
  update_pl600_receivers();
  delay(5);
  air();

  cnt_bad++;
  u8x8.setCursor ( 15, 5 );
  u8x8.print( (cnt_good+cnt_bad) );
  u8x8.setCursor ( 15, 7 );
  u8x8.print( cnt_bad );

  evaluate();
  u8x8.setCursor ( 25, 5 );
  u8x8.print( cnt_eval_good + cnt_eval_bad );  
  u8x8.setCursor ( 25, 7 );
  u8x8.print( cnt_eval_bad );  
  return;  
}




// === =======================================================================================
// ### #######################################################################################
// === =======================================================================================


void setup ( ) 
{
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
  
  uint8_t c;
  u8x8.setCursor ( c, 1 );
  for(c = 0; c < 32; c++ )
  {
    u8x8.print ( "_" );
  }


  air();


/*
  // Debug output
  u8x8.setCursor(0, 7);
  u8x8.print(nr_rects_high);
  u8x8.print(" ");
  u8x8.print(rect_high[3].start.x);
  u8x8.print(" ");
  u8x8.print(rect_high[3].start.y);
  u8x8.print(" ");
  u8x8.print(rect_high[3].stop.x);
  u8x8.print(" ");
  u8x8.print(rect_high[3].stop.y);
*/
  cnt_cycles = cnt_cycles_max;
}

// === ============================================================================================
// === ============================================================================================


int wait=100;
void loop() 
{

  
   while (pin_pushbutton1 == LOW )  
   {
    isr_pushbutton1 ( ); 
    //wait+=1000;
    io_pl600.in=1;
 update_pl600_inputs ( );
 delay(wait);
io_pl600.in=2;
 update_pl600_inputs ( );
 delay(wait);    
   }
 
/*
 else
   {
     u8x8.drawString ( 7, 3, "                   " ); 
   }
   */
  

  
  


  return;
}
