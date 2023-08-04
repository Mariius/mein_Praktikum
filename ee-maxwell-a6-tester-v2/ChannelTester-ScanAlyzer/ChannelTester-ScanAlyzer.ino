#include <Arduino.h>
#include <U8x8lib.h>
#include <SPI.h>
#define BIT(n) (1 << n)

U8X8_SSD1322_NHD_256X64_3W_HW_SPI u8x8(/* cs=*/ 3);

struct coordinate_ty { int x, y; };
struct rect_ty { int zone_idx; coordinate_ty start, stop; };





// -------------------------------------------------------------------------------------------------------------------------
// --- modify here if needed >>> -------------------------------------------------------------------------------------------





const int max_counts_x              = 3600;  // maximum counts in x-direction -> reset pulse (=y-count-pulse) will be issued after each line
const int max_zones                 =    2;
const int wait_after_nReset         =    2;  // time betwenn falling edge of reset and rising edge of globa on in seconds
const int wait_after_global_on      =    2;  // time betwenn rising edge of global on and first pulse in x direction in seconds
const int wait_after_ZONE_START     =    1;  // wait time between falling edge of global on and rising egde of global on (next cycle) in seconds
const int lines_after_zone_complete =    4;

// initialize a rectangle with: 
// [INDEX] = { left X, upper Y, right X, lower Y };
// INDEX must be consecutive within an array

// high side switch and low side switch do both affect the eddy current signal in the same way
// in zones where high and low side are active the effect is doubled compare to the zone where only one side is acitve

const int max_counts_y [ ] =  // line within a zone (including lines without tston or ppres), defines also how many zones are available;
{
  [ 0] = 30,
  [ 1] = 30
}; 

// rectangles as zones of high side switch enable
rect_ty rect_high [ ] = 
{
  // zone 0
  [ 0] = { 0,  550,10 ,  650,14 } , 
  [ 1] = { 0,  575, 9 ,  625,15 } ,  
  [ 2] = { 0, 1750,10 , 1850,14 } , 
  [ 3] = { 0, 1775, 9 , 1825,15 } , 
  [ 4] = { 0, 2950,10 , 3050,14 } ,
  [ 5] = { 0, 2975, 9 , 3025,15 } ,
  [ 6] = { 0, 1900,12 , 1905,12 } ,

  // zone 1
  [ 7] = { 1,  550,10 ,  650,14 } , 
  [ 8] = { 1,  575, 9 ,  625,15 } ,  
  [ 9] = { 1, 1750,10 , 1850,14 } , 
  [10] = { 1, 1775, 9 , 1825,15 } , 
  [11] = { 1, 2950,10 , 3050,14 } ,
  [12] = { 1, 2975, 9 , 3025,15 } ,
};

rect_ty rect_low[ ] = {                // rectangles as zones of low side switch enable
  // zone 0
  [0] = { 0,  575,10 ,  625,14 } , 
  [1] = { 0, 1775,10 , 1825,14 } , 
  [2] = { 0, 2975,10 , 3025,14 } ,
  
  // zone 1
  [3] = { 1,  575,10 ,  625,14 } , 
  [4] = { 1, 1775,10 , 1825,14 } , 
  [5] = { 1, 2975,10 , 3025,14 } ,
};





rect_ty rect_tston[ ] = {              // zones as rectangles where NO tston signal is active
    // use -2 to be sure the comparison with counter x returns 'inside rectangle'
    // zone 0
    [0] = { 0,  -2, 2, max_counts_x, 25 },
    // zone 1
    [1] = { 1,  -2, 2, max_counts_x, 25 }
};





rect_ty rect_ppres[ ] = {               // zones as rectangles where NO part present signal is active. 
    // use only whole lines to separate two testing zones from each other
    // zone 0
    [0] = { 0,  -2, 0, max_counts_x, 30 },
    // zone 1
    [1] = { 1,  -2, 0, max_counts_x, 30 }
};





// --- <<< modify here if needed -------------------------------------------------------------------------------------------
// -------------------------------------------------------------------------------------------------------------------------



int       zone_idx = 0;
enum {
    state_idle,
    state_reset,
    state_active,
    state_zone_complete,
    state_bad_zone
};
int state = state_idle;


// calculate sizes of array to simplify loops over all elements
const int nr_rects_high  = sizeof ( rect_high  ) / 10;
const int nr_rects_low   = sizeof ( rect_low   ) / 10;
const int nr_rects_tston = sizeof ( rect_tston ) / 10;
const int nr_rects_ppres = sizeof ( rect_ppres ) / 10;

// interface to PL600
const int pl600_input_sig_glbon = 0;
const int pl600_input_sig_ppres = 1;
const int pl600_input_sig_tston = 2;
const int pl600_input_sig_x     = 3;
const int pl600_input_sig_y     = 4;







coordinate_ty cnt     = {            0, 0 };
coordinate_ty cnt_max = { max_counts_x, 0 };



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
  if ( rect.zone_idx == zone_idx )
  {
    if (( rect.start.x <= (cnt.x-1) ) && ( (cnt.x-1) <= rect.stop.x ) &&
        ( rect.start.y <= (cnt.y-1) ) && ( (cnt.y-1) <= rect.stop.y ) )
      ret = 1;
  }
  return ret;
}



void tester_idle ( )
{
    cnt.x = 0;
    cnt.y = 0;
    io_pl600.in = 0;
    update_pl600_inputs ( );
}



void zone_start ( )
{
  update_pl600_outputs ( );
  zone_idx = (io_pl600.out >> 2);

  if ( zone_idx >= (sizeof(max_counts_y)/2) )
  {
    u8x8.print(" ");
    u8x8.print(zone_idx);
    u8x8.print(" ");
    u8x8.print((sizeof(max_counts_y)/2));
    state = state_bad_zone;
    delay(1000);
    return;
  }
  cnt_max.y = max_counts_y[zone_idx];
  cnt.y     = 0;
  cnt.x     = 0;
  
  io_pl600.in = (zone_idx << 1);
  update_pl600_inputs ( );
  delay(1000);
  io_pl600.in = (zone_idx << 1) + 1 ;
  update_pl600_inputs ( );
  delay(1000);
  io_pl600.in = 1;
  update_pl600_inputs ( );
  delay(1000);


  u8x8.clearLine ( 5 );
  u8x8.setCursor( 0, 5 );  
  u8x8.print("Zone ");
  u8x8.print( zone_idx );
  delay( wait_after_ZONE_START*1000 );
  u8x8.print(" Line "); 
  u8x8.setCursor( 13, 5 );
  u8x8.print( cnt.y );
  u8x8.print(" / "); 
  u8x8.print( cnt_max.y );
  draw_progress_bar( cnt.y, cnt_max.y, '=' );
  state = state_active;
  return;
}


void zone_stop ( )
{
  io_pl600.in = 0;
  update_pl600_inputs ( );
  
  for (int i=0; i<lines_after_zone_complete; i++)
  {
    io_pl600.in |=  BIT(pl600_input_sig_y);
    update_pl600_inputs ( );
    io_pl600.in &=  ~BIT(pl600_input_sig_y);
    update_pl600_inputs ( );
    cnt.y++;
  }

  cnt.y = 0; 
  cnt.x = 0;  

  io_pl600.in = 0;
  update_pl600_inputs ( );

  return;
}



void draw_progress_bar ( int current, int max, char c)
{
// char progress[33] = "[                              ]";
   char progress[33] = "[..............................]";

  
  uint32_t current_temp = current;
  uint32_t max_temp     = max;
  uint32_t bar_position = (current_temp *30 / max_temp);
  
  for (int i=0; i<bar_position; i++)
  {
      progress[i+1] = c;
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
  u8x8.drawString ( 2, 0, "ScanAlyzer Simulator (w. PLC)" );  
  
  uint8_t c;
  u8x8.setCursor ( c, 1 );
  for(c = 0; c < 32; c++ )
  {
    u8x8.print ( "_" );
  }

state = state_idle;
// state = state_active;

u8x8.setCursor ( 0, 5 );
u8x8.clearLine ( 5 );
u8x8.print("Waiting for ZONE_START...");

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
}

// === ============================================================================================
// === ============================================================================================



void loop() 
{

  update_pl600_outputs ( );

  switch ( state )
  {
    case state_idle: 
    {
        if (( digitalRead( pin_pl600_out0 ) != 0 ) || ( digitalRead( pin_pushbutton1 ) == 0 ))
        {
          state = state_reset;
          u8x8.setCursor ( 0, 5 );
          u8x8.clearLine ( 5 );
          u8x8.print( "Waiting for RESET release..." );
          delay(5);
          return;
        }
        else if (( digitalRead( pin_pl600_out1 ) != 0 ) || ( analogRead( pin_pushbutton2 ) < 100 ))
        {
          delay(2);
          zone_start();
        }
        else
        {
          tester_idle ( );
        }

        break;
    } // end of case state_idle

    case state_reset:
    {
        if (( digitalRead( pin_pl600_out0) != 0 ) || ( digitalRead( pin_pushbutton1 ) == 0 ))
        {
          delay(2);
          tester_idle ( );
          return;
        }
        else if (( digitalRead( pin_pl600_out1) != 0 ) || ( analogRead( pin_pushbutton2 ) < 100 ))
        {
          delay(2);
          zone_start();
        }
        else
        {
          u8x8.setCursor ( 0, 5 );
          u8x8.clearLine ( 5 );
          u8x8.print("Waiting for ZONE_START...\n");
          state = state_idle;
        }
        break;
    } // end of case state_reset

    case state_bad_zone:
    {
      u8x8.drawString ( 26, 3, "  ZBAD" );
      if ( digitalRead( pin_pl600_out1) == 0 )
      {      
        state = state_idle;
      }    
      break;
    }

    case state_active:
    {
      if (( digitalRead( pin_pl600_out0) != 0 ) || ( digitalRead( pin_pushbutton1 ) == 0 ))
      {
          state = state_reset;
          u8x8.setCursor ( 0, 5 );
          u8x8.clearLine ( 5 );
          u8x8.print( "Waiting for RESET release..." );


          u8x8.clearLine ( 7 );
          u8x8.setCursor ( 0, 7 );
          u8x8.print( "Zone " );
          u8x8.print( zone_idx );
          u8x8.print(" aborted @ Line ");
          u8x8.print( cnt.y );
          delay(5);
        return;
      }
      // --- begin/end of test cycle ------------------------------------------------------------------
      if ( cnt.y >= cnt_max.y )
      {
        u8x8.setCursor ( 0, 5 );
        u8x8.clearLine ( 5 );
        u8x8.print("Waiting for ZONE_START...");

        u8x8.clearLine ( 7 );
        u8x8.setCursor ( 0, 7 );
        u8x8.print( "Zone " );
        u8x8.print( zone_idx );
        u8x8.print(" complete.");
        
        zone_stop ( );
        state = state_idle;
        return;
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

        u8x8.setCursor( 13, 5 );
        u8x8.print( cnt.y );
        u8x8.print(" / "); 
        u8x8.print( cnt_max.y );
        draw_progress_bar( cnt.y, cnt_max.y, '=' );
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
        for ( unsigned int i=0; i<nr_rects_tston; i++ )
        {
          match |= ( is_inside_rectangle ( rect_tston[i] ) );
        }

        if ( match != 0 )
          io_pl600.in |=  BIT( pl600_input_sig_tston );
        else
          io_pl600.in &= ~BIT( pl600_input_sig_tston );
      }


      // --- rectangles for ppres -------------------------------------------
      {
        unsigned int match = 0;
        for ( unsigned int i=0; i<nr_rects_ppres; i++ )
        {
          match |= ( is_inside_rectangle ( rect_ppres[i] ) );
        }

        if ( match != 0 )
          io_pl600.in |=  BIT( pl600_input_sig_ppres );
        else
        {
          io_pl600.in &= ~BIT( pl600_input_sig_ppres );
          io_pl600.in &= ~BIT( pl600_input_sig_tston );
        } 
      }


      io_pl600.in &= ~BIT ( pl600_input_sig_x );    
      io_pl600.in &= ~BIT ( pl600_input_sig_y );
      update_pl600_inputs ( );
      break;
    } // end of case state_active

  } // end of switch

  return;
}
