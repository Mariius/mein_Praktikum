// PL600 Serialnumber and IP Tool
// Version 1.5

#include <Arduino.h>
#include <U8glib.h>
#include <U8x8lib.h>
#include <stdio.h>
//#include <wire.h>

// constructor for display
U8X8_SSD1322_NHD_256X64_3W_HW_SPI u8x8(/* cs=*/3);

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif

#define ENABLE_SW 500	// time until buttons enabled
#define DEBOUNCE 30		// debouncing time

// -------------------- globals ---------------------------
unsigned stage = 0;		// initial stage (= info screen)
char sub_stage = 'z';	// initial sub_stage, runs before 'a'

// custom ip (default values)
int ip_a = 192;
int ip_b = 168;
int ip_c = 1;
int ip_d = 217;

char custom_ip[25] = "";
char changed_ip_message[25] = "please reconnect arduino";

bool changed_ip = false;	// ip changed flag

char sA[5];
char sB[5];
char sC[5];
char sD[5];

int state = 0;	// returned button state

bool detect_type = false;
bool detect_ip = false;
bool detect_sn = false;
bool dev_authenticated = false;

String inData;
String devType;
String ip;
String sn;
String confirmation = "ACK: device authenticated as Pl600";
//int ledPin = 13;

void initDisplay() {
	// ------------------------------ display init. ---------------------------------
	u8x8.begin();
	u8x8.setPowerSave(0);
	u8x8.setFlipMode(180);
	u8x8.setContrast(200);
	u8x8.clearDisplay();
	u8x8.setFont(u8x8_font_artosserif8_r);

	// ------------------------------ Rohmann Ascii Script --------------------------
	u8x8.drawString(0, 0, "");
	u8x8.drawString(0, 1, " ___  __ _  _ ____ ___ _  _ _  _");
	u8x8.drawString(0, 2, "|__/ |  ||__| | | ||__||\\ | |\\ |");
	u8x8.drawString(0, 3, "|  \\_|__||  | | | ||  || \\| | \\|");
	u8x8.drawString(0, 4, "");
	u8x8.drawString(0, 5, "              GmbH ");
	//u8x8.drawString(0, 7, "    connect to PL600 device!");
}

void setup() {
	pinMode(LED_BUILTIN, OUTPUT);
	pinMode(PIN_A6, INPUT);	   // S3
	pinMode(PIN_A7, INPUT);    // S2
	pinMode(2, INPUT_PULLUP);  // S1 (digital)

	Serial.begin(115200);
	Serial.println("Serial connection established ...");
	initDisplay();
	u8x8.setFont(u8x8_font_artossans8_r);
	/*
	 u8x8.clearDisplay();
	 u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
	 int k = 0;
	 for (int i = 0; i < 8; i = i + 2) {
	 for (int j = 0; j < 30; j++) {
	 u8x8.drawGlyph(j, i, '@' + k);
	 k++;
	 }
	 }
	 */
	//u8x8.drawString(2, 0, "nopqrstuvwxyz");
	//u8x8.drawString(4, 0, "ABCDEFGHIJKLM");
	//u8x8.drawString(6, 0, "NOPQRSTUVWXYZ");
	//u8x8.drawString(8, 0, "123456789");
}

// ------------------- prototypes --------------------------
int btnS1pressed();
int btnS2pressed();
int btnS3pressed();

void draw_ip();
void drawSetBtn();
void drawCancelBtn();

void drawAfieldMarker();
void drawBfieldMarker();
void drawCfieldMarker();
void drawDfieldMarker();
void drawSetMarker();
void drawCancelMarker();

void loop() {
	while (Serial.available() > 0) {
		char recieved = Serial.read();
		inData += recieved;	  //     <PL600_INFO_IP_SN>[123.123.123.123](ABC123)

		// Process message when new line character is recieved
		if (recieved == '\n') {
			Serial.print("Arduino Received: ");
			Serial.print(inData);
			digitalWrite(LED_BUILTIN, HIGH);

			// You can put some if and else here to process the message juste like that:
			/*
			 if (inData == "OFF\n") { // DON'T forget to add "\n" at the end of the string.
			 Serial.println("LED OFF");
			 digitalWrite(LED_BUILTIN, LOW);
			 }
			 */
			if (!dev_authenticated) {
				int openingDI = inData.lastIndexOf('<');
				int closingDI = inData.lastIndexOf('>');
				devType = inData.substring(openingDI + 1, closingDI);

				if (devType.equals("PL600_INFO_IP_SN")) {
					detect_type = true;
					Serial.println(devType);

					u8x8.drawGlyph(27, 0, '.');	// show connection indicator 1
					delay(800);

					// extract ip
					int openingIP = inData.lastIndexOf('[');
					int closingIP = inData.lastIndexOf(']');
					ip = inData.substring(openingIP + 1, closingIP);

					if (ip.length() > 0) {
						Serial.println(ip);
						detect_ip = true;

						u8x8.drawGlyph(28, 0, '.');	// show connection indicator 2
						delay(800);

					} else {
						Serial.println("invalid or unknown IP detected!");
					}

					// extract sn
					int openingSN = inData.lastIndexOf('(');
					int closingSN = inData.lastIndexOf(')');
					sn = inData.substring(openingSN + 1, closingSN);

					if (sn.length() > 0) {
						Serial.println(sn);
						detect_sn = true;

						u8x8.drawGlyph(29, 0, '.');	// show connection indicator 3
						delay(800);
					} else {
						Serial.println("invalid or unknown SN detected!");
					}

					// set authentication flag
					if (detect_type && detect_ip && detect_sn) {
						dev_authenticated = true;
						Serial.println(confirmation);

						//u8x8.clearDisplay();
						u8x8.clearLine(0);
						u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
						u8x8.drawGlyph(30, 0, '@' + 24);// show that arduino is now connected
						u8x8.setFont(u8x8_font_artossans8_r);

						delay(1000);
					}
				}
			}
			inData = ""; // Clear recieved buffer
		}

		// ============================= DEV INFO STAGE =============================== (INIT. STAGE)
		while (dev_authenticated) {
			if ((stage == 0) && (changed_ip)) {
				Serial.end();	// close port
				u8x8.clearDisplay();
				u8x8.draw1x2String(2, 0, " Device-client will restart ");
				u8x8.draw1x2String(2, 2, "      in a few seconds !    ");
				u8x8.draw1x2String(2, 4, "Please re-connect Arduino to");
				u8x8.draw1x2String(2, 6, "   refresh IP information   ");
				while (1);
			}

			if (stage == 0) {
				u8x8.clearDisplay();
				u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
				u8x8.drawGlyph(30, 0, '@' + 24); // show that arduino is now connected
				u8x8.setFont(u8x8_font_artossans8_r);

				u8x8.draw2x2String(0, 0, "DEV: ");
				u8x8.draw2x2String(8, 0, "PL600");

				u8x8.draw1x2String(0, 3, "   IP:");
				u8x8.draw1x2String(8, 3, ip.c_str()); // if ip hasn't changed, show the actual device ip

				u8x8.draw1x2String(0, 6, "   SN:");
				u8x8.draw1x2String(8, 6, sn.c_str());

				// show navigation button
				u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
				u8x8.drawGlyph(27, 7, '@' + 6);
				u8x8.setFont(u8x8_font_artossans8_r);

				delay(ENABLE_SW);
				while (stage == 0) {
					if (btnS3pressed()) {
						stage = 1;
						Serial.println("stage_1"); // switch to dynamic ip screen (stage_1)
						u8x8.clearDisplay();
					}
				}
			}

			// ============================= DYNAMIC IP STAGE ===============================
			if (stage == 1) {

				u8x8.drawString(0, 4, "Set IP-Mode: dynamic _");
				u8x8.drawString(0, 5, "                      \\");
				u8x8.drawString(0, 6, "                       \\");
				// show navigation and SET dynamic button
				u8x8.setInverseFont(1);
				u8x8.drawString(23, 7, "  ");
				u8x8.setInverseFont(0);

				u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
				u8x8.drawGlyph(27, 7, '@' + 6);
				u8x8.setFont(u8x8_font_artossans8_r);

				// ---------------------------------------------- show navigation buttons
				delay(ENABLE_SW);
				while (stage == 1) {
					if (btnS2pressed()) {		// pressed
						Serial.println("set_dynamic");
						changed_ip = true;
						sub_stage = 'z';
						stage = 0;
						delay(1000);
					}
					if (btnS3pressed()) {// switch to static ip screen (stage_2)
						stage = 2;
						Serial.println("stage_2");
						u8x8.clearLine(4);

						u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
						u8x8.drawGlyph(30, 0, '@' + 24); // show that arduino is now connected
						u8x8.setFont(u8x8_font_artossans8_r);
					}
				}

			}

			// ============================= STATIC IP STAGE ===============================
			if (stage == 2) {

				u8x8.drawString(0, 4, "Set IP-Mode: static __");
				u8x8.drawString(0, 5, "                      \\");
				u8x8.drawString(0, 6, "--> 192.168.1.217      \\");
				// show navigation and SET static button
				u8x8.setInverseFont(1);
				u8x8.drawString(23, 7, "  ");
				u8x8.setInverseFont(0);

				u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
				u8x8.drawGlyph(27, 7, '@' + 6);
				u8x8.setFont(u8x8_font_artossans8_r);

				delay(ENABLE_SW);
				while (stage == 2) {
					if (btnS2pressed()) {		// set the default static ip
						Serial.println("set_static");
						changed_ip = true;
						sub_stage = 'z';
						stage = 0;
						delay(1000);
					}
					if (btnS3pressed()) {// switch to custom ip screen (stage_3)
						stage = 3;
						sub_stage = 'z';
						Serial.println("stage_3");

					}
				}
			}

			// ============================= CUSTOM IP STAGE ===============================
			if (stage == 3) {//    <PL600_INFO_IP_SN>[123.123.123.123](ABC123)

				if (sub_stage == 'z') {	// sub_stage z (init. for sub_stage a)
					u8x8.clearLine(4);
					u8x8.clearLine(5);
					u8x8.clearLine(6);
					u8x8.clearLine(7);

					// show navigation, decrease and increase buttons
					// ->
					u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
					u8x8.drawGlyph(27, 7, '@' + 6);
					// ^
					u8x8.drawGlyph(24, 7, '@' + 12);
					// v
					u8x8.drawGlyph(20, 7, '@' + 15);
					u8x8.setFont(u8x8_font_artossans8_r);

					// --------------------------------------- switch to ip field A
					delay(ENABLE_SW);
					sub_stage = 'a';
					draw_ip();
					drawAfieldMarker();
					Serial.println("stage_3__sub_stage_a");

				}
				// while ip field a is active
				while (sub_stage == 'a') {
					if (btnS1pressed()) {				// increase
						if (ip_a < 256)
							ip_a++;
						else
							ip_a = 0;
						draw_ip();
					}

					if (btnS2pressed()) {				// decrease
						if (ip_a > 1)
							ip_a--;
						else
							ip_a = 255;
						draw_ip();
						//continue;
					}

					if (btnS3pressed()) {			// switch to next sub_stage
						sub_stage = 'b';
						Serial.println("stage_3__sub_stage_b");
						drawBfieldMarker();
						delay(ENABLE_SW);
						break;
					}
				}

				// while ip field b is active
				while (sub_stage == 'b') {
					if (btnS1pressed()) {				// increase
						if (ip_b < 256)
							ip_b++;
						else
							ip_b = 0;
						draw_ip();
					}

					if (btnS2pressed()) {				// decrease
						if (ip_b > 1)
							ip_b--;
						else
							ip_b = 255;
						draw_ip();
						//continue;
					}

					if (btnS3pressed()) {				// next sub_stage
						sub_stage = 'c';
						Serial.println("stage_3__sub_stage_c");
						drawCfieldMarker();
						delay(ENABLE_SW);
						break;
					}
				}

				// while ip field c is active
				while (sub_stage == 'c') {
					if (btnS1pressed()) {				// increase
						if (ip_c < 256)
							ip_c++;
						else
							ip_c = 0;
						draw_ip();
					}

					if (btnS2pressed()) {				// decrease
						if (ip_c > 1)
							ip_c--;
						else
							ip_c = 255;
						draw_ip();
						//continue;
					}

					if (btnS3pressed()) {				// next sub_stage
						sub_stage = 'd';
						Serial.println("stage_3__sub_stage_d");
						drawDfieldMarker();
						delay(ENABLE_SW);
						break;
					}
				}

				// while ip field d is active
				while (sub_stage == 'd') {
					if (btnS1pressed()) {				// increase
						if (ip_d < 256)
							ip_d++;
						else
							ip_d = 0;
						draw_ip();
					}

					if (btnS2pressed()) {				// decrease
						if (ip_d > 1)
							ip_d--;
						else
							ip_d = 255;
						draw_ip();
						//	continue;
					}

					if (btnS3pressed()) {				// next sub_stage
						sub_stage = 'e';
						Serial.println("stage_3__sub_stage_e");
						drawSetMarker();
						delay(ENABLE_SW);
						break;
					}
				}

				// while ip field e (SET) is active
				while (sub_stage == 'e') {
					//	if (btnS1pressed())						// increase
					//		ip_c++;
					//	continue;
					if (btnS2pressed()) {

						//delay(500);
						sprintf(custom_ip, "set_custom_%d.%d.%d.%d\n", ip_a,
								ip_b, ip_c, ip_d);
						Serial.println(custom_ip);// send "set_custom_xxx.xxx.xxx.xxx"

						changed_ip = true;
						sub_stage = 'z';
						stage = 0;
						delay(1000);
						u8x8.clearDisplay();
						//break;
					}

					if (btnS3pressed()) {				// next sub_stage
						sub_stage = 'f';
						Serial.println("stage_3__sub_stage_f");
						drawCancelMarker();
						delay(ENABLE_SW);
						//break;
					}
				}

				// while ip field f (CANCEL) is active
				while (sub_stage == 'f') {
					if (btnS2pressed()) {
						Serial.println("stage_0");
						sub_stage = 'z';
						stage = 0;
						delay(ENABLE_SW);
						break;
					}
					if (btnS3pressed()) {// next sub_stage (initial sub_stage)
						sub_stage = 'z';
						Serial.println("stage_3__sub_stage_a");
						drawAfieldMarker();
						delay(ENABLE_SW);
						//break;
					}
				}
			}

			if ((stage == 0) && (sub_stage == 'z')) {
				continue;
			}
		}
	}
}

// ========================================= METHODS =====================================================

// ----------------------------------------- buttons -----------------------------------------------------
int btnS1pressed() {
	state = 0;
	if (!digitalRead(2)) {
		delay(DEBOUNCE + DEBOUNCE);				// debounce
		//if (digitalRead(2)) {
		//delay(DEBOUNCE);				// debounce
		state = 1;
		//}
	}
	return state;
}

int btnS2pressed() {
	state = 0;
	if (!analogRead(PIN_A6)) {			// pressed
		delay(DEBOUNCE);			// debounce
		if (analogRead(PIN_A6)) {		// released
			delay(DEBOUNCE);		// debounce
			state = 1;
		}
	}
	return state;
}

int btnS3pressed() {
	state = 0;
	if (!analogRead(PIN_A7)) {			// pressed
		delay(DEBOUNCE);			// debounce
		if (analogRead(PIN_A7)) {		// released
			delay(DEBOUNCE);		// debounce
			state = 1;
		}
	}
	return state;
}

// ------------------------------------------- display drawings -------------------------------------------
void draw_ip() {

	sprintf(sA, "%d", ip_a);
	Serial.println(sA);
	sprintf(sB, "%d", ip_b);
	Serial.println(sB);
	sprintf(sC, "%d", ip_c);
	Serial.println(sC);
	sprintf(sD, "%d", ip_d);
	Serial.println(sD);

	u8x8.clearLine(2);
	u8x8.clearLine(3);
	u8x8.draw1x2String(0, 2, sA);		//xxx
	u8x8.draw1x2String(3, 2, ".");		//   .
	u8x8.draw1x2String(4, 2, sB);		//    xxx
	u8x8.draw1x2String(7, 2, ".");		//       .
	u8x8.draw1x2String(8, 2, sC);		//        xxx
	u8x8.draw1x2String(11, 2, ".");		//           .
	u8x8.draw1x2String(12, 2, sD);		//            xxx

	drawSetBtn();
	drawCancelBtn();
}

void drawSetBtn() {

	u8x8.draw1x2String(19, 2, "SET");
}

void drawCancelBtn() {
	u8x8.draw1x2String(26, 2, "CANCEL");
}

// ---------------------------- markers
void drawAfieldMarker() {
	u8x8.clearLine(4);
	u8x8.clearLine(5);
	u8x8.clearLine(6);		// from previous cancel
	u8x8.draw1x2String(0, 4, "===");		// mark active field
}

void drawBfieldMarker() {
	u8x8.clearLine(4);
	u8x8.clearLine(5);
	u8x8.draw1x2String(4, 4, "===");		// mark active field
}
void drawCfieldMarker() {
	u8x8.clearLine(4);
	u8x8.clearLine(5);
	u8x8.draw1x2String(8, 4, "===");		// mark active field
}
void drawDfieldMarker() {
	u8x8.clearLine(4);
	u8x8.clearLine(5);
	u8x8.draw1x2String(12, 4, "===");		// mark active field
}

void drawSetMarker() {
	u8x8.clearLine(4);
	u8x8.clearLine(5);
	u8x8.clearLine(7);
	u8x8.setInverseFont(1);

	u8x8.drawString(23, 7, "  ");	// draw empty rectangle for sw2
	u8x8.setInverseFont(0);

	u8x8.setFont(u8x8_font_open_iconic_arrow_1x1);
	u8x8.drawGlyph(27, 7, '@' + 6);
	u8x8.setFont(u8x8_font_artossans8_r);
	u8x8.drawString(19, 4, "___");			// mark active field
	u8x8.drawString(20, 5, "  \\");
	u8x8.drawString(20, 6, "   \\");
}

void drawCancelMarker() {
	u8x8.clearLine(4);
	u8x8.clearLine(5);
	u8x8.clearLine(6);
	u8x8.drawString(26, 4, "______");		// mark active field
	u8x8.drawString(25, 5, "/");
	u8x8.drawString(24, 6, "/");
}
