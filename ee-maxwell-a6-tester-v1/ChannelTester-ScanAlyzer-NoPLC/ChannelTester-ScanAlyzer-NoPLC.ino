/*
#include <Arduino.h>
#include <U8x8lib.h>
#include <SPI.h>
#define BIT(n) (1 << n)

U8X8_SSD1322_NHD_256X64_3W_HW_SPI u8x8( 3);

struct coordinate_ty { int x, y; };
struct rect_ty { coordinate_ty start, stop; };





// -------------------------------------------------------------------------------------------------------------------------
// --- modify here if needed >>> -------------------------------------------------------------------------------------------





const int max_counts_x              = 3600;  // maximum counts in x-direction -> reset pulse (=y-count-pulse) will be issued after each line
const int max_counts_y              =  100;  // line within a scan (including lines without tston or ppres)
const int wait_after_nReset         =    2;  // time betwenn falling edge of reset and rising edge of globa on in seconds
const int wait_after_global_on      =    2;  // time betwenn rising edge of global on and first pulse in x direction in seconds
const int wait_after_cylce_complete =    5;  // wait time between falling edge of global on and rising egde of global on (next cycle) in seconds

// initialize a rectangle with: 
// [INDEX] = { left X, upper Y, right X, lower Y };
// INDEX must be consecutive within an array

// high side switch and low side switch do both affect the eddy current signal in the same way
// in zones where high and low side are active the effect is doubled compare to the zone where only one side is acitve
rect_ty rect_high[ ] = {               // rectangles as zones of high side switch enable
  [0] = {  550,10 ,  650,14 } , 
  [1] = {  575, 9 ,  625,15 } ,  
  
  [2] = { 1750,10 , 1850,14 } , 
  [3] = { 1775, 9 , 1825,15 } , 
    
  [4] = { 2950,10 , 3050,14 } ,
  [5] = { 2975, 9 , 3025,15 } ,
    
  [6] = { 1900,12 , 1905,12 } 
};

rect_ty rect_low[ ] = {                // rectangles as zones of low side switch enable
  [0] = {  575,10 ,  625,14 } , 
  [1] = { 1775,10 , 1825,14 } , 
  [2] = { 2975,10 , 3025,14 } ,
};





rect_ty rect_ntston[ ] = {              // zones as rectangles where NO tston signal is active
    [0] = {  -2, 35, max_counts_x, 45 } // use -2 to be sure the comparison with counter x returns 'inside rectangle'
};





rect_ty rect_nppres[ ] = {              // zones as rectangles where NO part present signal is active. 
    [0] = {  -2, 40, max_counts_x, 50 } // use only whole lines to separate two testing zones from each other
};





// --- <<< modify here if needed -------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------------------------





// calculate sizes of array to simplify loops over all elements
const int nr_rects_high   = sizeof ( rect_high )   / 8;
const int nr_rects_low    = sizeof ( rect_low )    / 8;
const int nr_rects_ntston = sizeof ( rect_ntston ) / 8;
const int nr_rects_nppres = sizeof ( rect_nppres ) / 8;

// interface to
const int pl600_input_sig_glbon = 0;
const int pl600_input_sig_ppres = 1;
const int pl600_input_sig_tston = 2;
const int pl600_input_sig_x     = 3;
const int pl600_input_sig_y     = 4;







coordinate_ty cnt     = {            0,            0 };
coordinate_ty cnt_max = { max_counts_x, max_counts_y };



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


int is_inside_rectangle( rect_ty rect )
{
  int ret = 0;
  if (( rect.start.x <= (cnt.x-1) ) && ( (cnt.x-1) <= rect.stop.x ) &&
      ( rect.start.y <= (cnt.y-1) ) && ( (cnt.y-1) <= rect.stop.y ) )
    ret = 1;

  return ret;
}


void cycle_start ( )
{
  io_pl600.in |=  BIT( pl600_input_sig_glbon ); 
  update_pl600_inputs ( );
  u8x8.drawString(0, 6, "Cycle start (global on)"); 
  delay ( wait_after_global_on );
  
  u8x8.setCursor(0, 6);  
  u8x8.print("Line:   "); 
  u8x8.print(cnt.y);
  u8x8.print(" / ");
  u8x8.print(cnt_max.y);

  return;
}


void cycle_stop ( )
{
  cnt.y = 0; 
  cnt.x = 0;

  u8x8.drawString(0, 6, "Cycle complete.            ");

  io_pl600.in =  0;
  update_pl600_inputs ( );
  delay ( wait_after_cylce_complete );

  return;
}



void draw_progress_bar ( int current, int max, char c)
{
  char progress[33] = "[------------------------------]";

  int current_temp = (current * 3000) / max;
  current_temp /= 100;
  for (int i=1; i<current_temp; i++)
  {
      progress[i] = c;
  }
  u8x8.drawString(0, 7, progress);
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
  u8x8.drawString ( 4, 0,"A6-Channel Test Adapter" );
  uint8_t c;
  for(c = 0; c < 32; c++ )
  {
    u8x8.setCursor ( c, 1 );
    u8x8.print ( "_" );
  }
  u8x8.drawString ( 0, 3," ScanAlyzer Simulator is running " );  

// --- Debug output -------------------
//  u8x8.setCursor(0, 7);
//  u8x8.print(nr_rects_high);
//  u8x8.print(" ");
//  u8x8.print(rect_high[3].start.x);
//  u8x8.print(" ");
//  u8x8.print(rect_high[3].start.y);
//  u8x8.print(" ");
//  u8x8.print(rect_high[3].stop.x);
//  u8x8.print(" ");
//  u8x8.print(rect_high[3].stop.y);

}

// === ============================================================================================
// === ============================================================================================







void loop() 
{


  if ( digitalRead( pin_pl600_out0 ) != 0 )
  {
    cycle_stop();
    u8x8.drawString(0, 6, "Tester in RESET State             ");

    while ( digitalRead( pin_pl600_out0 ) != 0 ); // wait here for ping to go low
    delay ( wait_after_nReset * 1000 );
    cycle_start();

    return;
  }

  
  if ( ( io_pl600.in & BIT( pl600_input_sig_glbon ) ) == 0 )
  {
    io_pl600.in |=  BIT( pl600_input_sig_glbon ); 
  }
  
  // --- pulses for x-position --------------------------------------------------------------------
  {
    io_pl600.in |=  BIT(pl600_input_sig_x);    
    update_pl600_inputs ( );
    cnt.x++;
  }


  // --- pulses for y-position --------------------------------------------------------------------
  if ( cnt.x >= cnt_max.x )
  {
    cnt.x = 0;

    io_pl600.in |=  BIT ( pl600_input_sig_y );
    update_pl600_inputs ( );
    cnt.y++;
    u8x8.setCursor(0, 6);  
    u8x8.print("Line:   "); 
    u8x8.print(cnt.y);
    u8x8.print(" / "); 
    u8x8.print(cnt_max.y);
    draw_progress_bar( cnt.y, cnt_max.y, '|');
  }


  // --- begin/end of test cycle ------------------------------------------------------------------
  if ( cnt.y >= cnt_max.y )
  {
    cycle_stop ( );
    cycle_start ( );
  }


  // --- rectangles for high side switch receiver A ----------------------
  {
    unsigned int match = 0;
    for ( unsigned int i=0; i<nr_rects_high; i++ )
    {
      match |= ( is_inside_rectangle ( rect_high[i] ) );
    }
  
    if ( match != 0 )
      io_pl600.rec_a |= 2;
    else
      io_pl600.rec_a &= 1;
  }
    

  // --- rectangles for low side switch receiver A -----------------------
  {
    unsigned int match = 0;
    for ( unsigned int i=0; i<nr_rects_low; i++ )
    {
      match |= ( is_inside_rectangle ( rect_low[i] ) );
    }

    if ( match )
      io_pl600.rec_a |= 1;
    else
      io_pl600.rec_a &= 2;
  }


  update_pl600_receivers();



  // --- rectangles for tston -------------------------------------------
  {
    unsigned int match = 0;
    for ( unsigned int i=0; i<nr_rects_ntston; i++ )
    {
      match |= ( is_inside_rectangle ( rect_ntston[i] ) );
    }

    if ( match != 0 )
      io_pl600.in &= ~BIT( pl600_input_sig_tston );
    else
      io_pl600.in |=  BIT( pl600_input_sig_tston );
  }


  // --- rectangles for ppres -------------------------------------------
  {
    unsigned int match = 0;
    for ( unsigned int i=0; i<nr_rects_nppres; i++ )
    {
      match |= ( is_inside_rectangle ( rect_nppres[i] ) );
    }

    if ( match != 0 )
    {
      io_pl600.in &= ~BIT( pl600_input_sig_ppres );
      io_pl600.in &= ~BIT( pl600_input_sig_tston );
    }
    else
      io_pl600.in |=  BIT( pl600_input_sig_ppres );
  }


  io_pl600.in &= ~BIT ( pl600_input_sig_x );    
  io_pl600.in &= ~BIT ( pl600_input_sig_y );
  update_pl600_inputs ( );
  
}
*/
