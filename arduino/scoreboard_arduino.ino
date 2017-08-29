#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN_1 3
#define PIN_2 5
#define PIN_3 6
#define PIN_4 9
#define PIN_5 10

Adafruit_NeoPixel num1 = Adafruit_NeoPixel(35, PIN_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel num2 = Adafruit_NeoPixel(35, PIN_2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel num3 = Adafruit_NeoPixel(35, PIN_3, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel num4 = Adafruit_NeoPixel(35, PIN_4, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pins = Adafruit_NeoPixel(2, PIN_5, NEO_GRB + NEO_KHZ800);

int red = 0;
int green = 235;
int blue = 235;

int oneSecVal = 0;
int tenSecVal = 0;
int oneMinVal = 0;
int tenMinVal = 0;

int clockMode = 0; // 0 indicates clock, 1 indicates timer
boolean timerRunning = false;

long prevMillis = 0;
long curMillis = 0;

void offNum(Adafruit_NeoPixel &strip) {
  for(int i=0; i<strip.numPixels(); i++)
    strip.setPixelColor(i, strip.Color(0,0,0));

  strip.show();
}

void showNum(int value, Adafruit_NeoPixel &strip) {
  offNum(strip); // shuts off all pixels on specified strip

  switch(value) {
    case 0: // each case # is value to be displayed
      // case only goes to 30 because 0 goes round the pixels
      for(int i=0; i<35; i++) {
        if(i>=30) // skips last middle segment
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;

    case 1:
      for(int i=0; i<35; i++) {
        if(i>=0 && i<15 || i >= 25)
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;

    case 2:
      for(int i=0; i<35; i++) {
        if(i>=5 && i<10 || i>=20 && i<25)
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;

    case 3:
      for(int i=0; i<35; i++) {
        if(i<10)
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;

    case 4:
      for(int i=0; i<35; i++) {
        if(i>=0 && i<5 || i>=10 && i<15 || i>=25 && i<30)
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;

    case 5:
      for(int i=0; i<35; i++) {
        if(i>=0 && i<5 || i>=15 && i<20)
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;
    case 6:
      for(int i=0; i<35; i++) {
        if(i>=15 && i<20)
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;

    case 7:
      for(int i=0; i<35; i++) {
        if(i>=0 && i<10 || i>=25)
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;

    case 8:
      for(int i=0; i<35; i++)
        strip.setPixelColor(i, strip.Color(red,green,blue));

      break;

    case 9:
      for(int i=0; i<35; i++) {
        if(i>=0 && i<5 || i>=25 && i<30)
          continue;

        strip.setPixelColor(i, strip.Color(red,green,blue));
      }
      break;

    default:
      break;
  }

  strip.show(); // displays whatever pixels were turned on in code above
}

void displayNums() {
  if(tenMinVal <= 0 && oneMinVal > 0) {
    offNum(num1);
    showNum(oneMinVal, num2);
    showNum(tenSecVal, num3);
    showNum(oneSecVal, num4);
  }

  else if(tenMinVal <= 0 && oneMinVal <= 0 && tenSecVal > 0) {
    offNum(num1);
    offNum(num2);
    showNum(tenSecVal, num3);
    showNum(oneSecVal, num4);
  }

  else if(tenMinVal <= 0 && tenSecVal <= 0 && oneMinVal <= 0 && oneSecVal > 0) {
    offNum(num1);
    offNum(num2);
    offNum(num3);
    showNum(oneSecVal, num4);
  }

  else {
    showNum(tenMinVal, num1);
    showNum(oneMinVal, num2);
    showNum(tenSecVal, num3);
    showNum(oneSecVal, num4);
  }
}

void handleData(int data[]) {
  // ends function if data is not fully sent
  if(data[5] == -1)
    return;

  if(data[0] == 'R' && data[2] == 'G' && data[4] == 'B') {
    red = data[1];
    green = data[3];
    blue = data[5];

    displayNums();
  }

  if(data[0] == 'N' && data[2] == 'P') {
    switch(data[3]) {
      case 1:
        oneSecVal = data[1];
        showNum(oneSecVal, num4);
        break;
      case 2:
        tenSecVal = data[1];
        showNum(tenSecVal, num3);
        break;
      case 3:
        oneMinVal = data[1];
        showNum(oneMinVal, num2);
        break;
      case 4:
        tenMinVal = data[1];
        showNum(tenMinVal, num1);
        break;
      default:
        break;
    }
  }

  if(data[0] == 'H' && data[2] == 'M') {
    if(String(data[1]).length() == 1) {
      offNum(num1);
      oneMinVal = String(data[1])[0] - '0';

      showNum(oneMinVal, num2);
    }
    else {
      tenMinVal = String(data[1])[0] - '0'; // process takes int value, converts to string, gets first char, and
                                            // converts to corresponding int value
      oneMinVal = String(data[1])[1] - '0'; // gets second char

      showNum(tenMinVal, num1);
      showNum(oneMinVal, num2);
    }
    //Serial.println(String(tenMinVal)[0] - '0' + " test");

    if(String(data[3]).length() == 1) {
      tenSecVal = 0;
      oneSecVal = String(data[3])[0] - '0';

      showNum(tenSecVal, num3);
      showNum(oneSecVal, num4);
    }
    else {
      tenSecVal = String(data[3])[0] - '0';
      oneSecVal = String(data[3])[1] - '0';

      showNum(tenSecVal, num3);
      showNum(oneSecVal, num4);
    }
  }

  if(data[0] == 'C') {
    if(data[1] == 0)
      timerRunning = false;
    clockMode = data[1];
  }

  if(data[0] == 'T') {
    // set clock to 0
    if(data[1] == 0 && !timerRunning) {
      showNum(0, num1);
      showNum(0, num2);
      showNum(0, num3);
      showNum(0, num4);

      oneSecVal = 0;
      oneMinVal = 0;
      tenSecVal = 0;
      tenMinVal = 0;
    }

    if(data[1] == 1)
      timerRunning = true;
    if(data[1] == 9)
      timerRunning = false;
  }
}

void doTimerTick() {
  curMillis = millis();

  // doing this achieves a form of concurrency
  if(!timerRunning || curMillis - prevMillis < 1000)
    return;

  prevMillis = curMillis;

  oneSecVal--;

  if(oneSecVal == -1 && tenSecVal >= 0) {
    oneSecVal = 9;
    tenSecVal--;
  }

  if(tenSecVal == -1 && oneMinVal >= 0) {
    tenSecVal = 5;
    oneMinVal--;
  }

  if(oneMinVal == -1 && tenMinVal >= 0) {
    oneMinVal = 9;
    tenMinVal--;
  }

  if(oneSecVal == 0 && tenSecVal == 0 && oneMinVal == 0 && tenMinVal == 0) {
    timerRunning = false;

    oneSecVal = 0;
    tenSecVal = 0;
    oneMinVal = 0;
    tenMinVal = 0;

    red = 235;
    green = 0;
    blue = 0;

    showNum(tenMinVal, num1);
    showNum(oneMinVal, num2);
    showNum(tenSecVal, num3);
    showNum(oneSecVal, num4);

    return;
  }

  displayNums();
}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait, Adafruit_NeoPixel &strip) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void allOn(uint32_t c, Adafruit_NeoPixel &strip) {
  for(uint16_t i=0; i<strip.numPixels(); i++)
    strip.setPixelColor(i,c);

  strip.show();
}

void showGo() {

  for(int x = 0; x < 235; x++) {
    /*** fades in "GO" ***/
    for(int i = 0; i < 35; i++) {
      if(i < 15 || (i >= 20 && i < 30) || i >= 33)
        num2.setPixelColor(i,num2.Color(x,x,0));

      if(i < 30)
        num3.setPixelColor(i,num3.Color(x,x,0));

    }

    num2.show();
    num3.show();
  }
  
  delay(5);

  for(int x = 235; x > 0; x--) {
    /*** fades out "GO" ***/
    for(int i = 0; i < 35; i++) {
      if(i < 15 || (i >= 20 && i < 30) || i >= 33)
        num2.setPixelColor(i,num2.Color(x,x,0));

      if(i < 30)
        num3.setPixelColor(i,num3.Color(x,x,0));

    }

    num2.show();
    num3.show();
  }
}

void showBlue() {

  for(int x = 0; x < 235; x++) {
    /*** fades in "BLUE" ***/
    for(int i = 0; i < 35; i++) {
      if(i < 10 || (i >= 25 && i < 30)) {
        num1.setPixelColor(i,num1.Color(0,0,x));
        num2.setPixelColor(i,num2.Color(0,0,x));
        num3.setPixelColor(i,num3.Color(0,0,x));
        num4.setPixelColor(i,num4.Color(0,0,x));
      }

      if(i >= 15 && i < 25)
        num3.setPixelColor(i,num3.Color(0,0,x));

      if(i >= 30 || (i >= 10 && i < 15))
        num4.setPixelColor(i,num4.Color(0,0,x));

      if(i >= 10 && i < 19 || i >= 21 && i < 25 || i >= 30 && i < 34)
        num1.setPixelColor(i,num1.Color(0,0,x));
    }

    num1.show();
    num2.show();
    num3.show();
    num4.show();
  }

  for(int x = 235; x > 0; x--) {
    /*** fades out "BLUE" ***/
    for(int i = 0; i < 35; i++) {
      if(i < 10 || (i >= 25 && i < 30)) {
        num1.setPixelColor(i,num1.Color(0,0,x));
        num2.setPixelColor(i,num2.Color(0,0,x));
        num3.setPixelColor(i,num3.Color(0,0,x));
        num4.setPixelColor(i,num4.Color(0,0,x));
      }

      if(i >= 15 && i < 25)
        num3.setPixelColor(i,num3.Color(0,0,x));

      if(i >= 30 || (i >= 10 && i < 15))
        num4.setPixelColor(i,num4.Color(0,0,x));

      if(i >= 10 && i < 19 || i >= 21 && i < 25 || i >= 30 && i < 34)
        num1.setPixelColor(i,num1.Color(0,0,x));
    }

    num1.show();
    num2.show();
    num3.show();
    num4.show();
  }
}

void initLEDS() {

  for(int i = 0; i < 2; i++) {
    showGo();
    showBlue();
  }


  /*
  for(int i = 30; i < 35; i++) {
    num1.setPixelColor(i,num1.Color(235,235,235));
    num2.setPixelColor(i,num2.Color(235,235,235));
    num3.setPixelColor(i,num3.Color(235,235,235));
    num4.setPixelColor(i,num4.Color(235,235,235));

    num1.show();
    num2.show();
    num3.show();
    num4.show();

    delay(100);
  }

  offNum(num1);
  offNum(num2);
  offNum(num3);
  offNum(num4);
  offNum(pins);

  // shows "J"
  for(int i = 15; i < 30; i++)
    num1.setPixelColor(i,num1.Color(0,0,235));

  // shows "R"
  for(int i = 0; i < 35; i++) {
    if(i >= 25 && i < 30 || i == 34 || i == 19 || i == 20)
      continue;
    num2.setPixelColor(i,num1.Color(0,0,235));
  }

  // shows "A"
  for(int i = 0; i < 35; i++) {
    if(i >= 25 && i < 30)
      continue;
    num3.setPixelColor(i,num1.Color(0,0,235));
  }

  // shows "D"
  for(int i = 0; i < 30; i++) {
    if(i == 14 || i == 15 || i == 24 || i == 25)
      continue;
    num4.setPixelColor(i,num1.Color(0,0,235));
  }*/

  num1.show();
  num2.show();
  num3.show();
  num4.show();
}

void setup() {
  Serial.begin(115200);
  num1.begin();
  num2.begin();
  num3.begin();
  num4.begin();
  pins.begin();

  num1.show();
  num2.show();
  num3.show();
  num4.show();
  pins.show();

  initLEDS();
}

void loop() {
  int data[6] = {0,0,0,0,0,-1};
  int a = 0;
  int dataSize = 6;

  pins.setPixelColor(0,pins.Color(235,235,235));
  pins.setPixelColor(1,pins.Color(235,235,235));
  pins.show();

  while(data[5] == -1){
    if(Serial.available()) {
      data[a] = Serial.read();
      a++;
    }

    handleData(data);
    doTimerTick();
  }
}
