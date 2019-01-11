#include "FastLED.h"

#define PIN_1 3
#define PIN_2 5
#define PIN_3 6
#define PIN_4 9
#define PIN_5 10

const byte NUM_LEDS = 70;
const byte LPS = 10;

CRGB num1[NUM_LEDS];
CRGB num2[NUM_LEDS];
CRGB num3[NUM_LEDS];
CRGB num4[NUM_LEDS];
CRGB pins[NUM_LEDS];

const byte MAX_COLOR_VAL = 200;
byte red = 0;
byte green = MAX_COLOR_VAL;
byte blue = MAX_COLOR_VAL;

int oneSecVal = 0;
int tenSecVal = 0;
int oneMinVal = 0;
int tenMinVal = 0;

int clockMode = 0; // 0 indicates clock, 1 indicates timer
boolean timerRunning = false;

long prevMillis = 0;
long curMillis = 0;

void showNum(CRGB *strip, byte NUM_LEDS, byte value) {
  fill_solid(strip, NUM_LEDS, CRGB(red,green,blue));
  
  for(int i=0; i<NUM_LEDS; i++) {
    switch(value) {
      case 0: // each case # is value to be displayed
        if(i>=NUM_LEDS - LPS) 
          strip[i] = CRGB(0,0,0);
        break;
        
      case 1:
        if(i>=0 && i<3*LPS || i >= 5*LPS) 
          strip[i] = CRGB(0,0,0);
        break;

      case 2:
        if(i>=LPS && i<2*LPS || i>=4*LPS && i<5*LPS)
          strip[i] = CRGB(0,0,0);
        break;
  
      case 3:
        if(i<2*LPS)
          strip[i] = CRGB(0,0,0);
        break;
  
      case 4:
      
        if(i>=0 && i<LPS || i>=2*LPS && i<3*LPS || i>=5*LPS && i<6*LPS)
          strip[i] = CRGB(0,0,0);
        break;
  
      case 5:
        if(i>=0 && i<LPS || i>=3*LPS && i<4*LPS)
          strip[i] = CRGB(0,0,0);
        break;
        
      case 6:
        if(i>=3*LPS && i<4*LPS)
          strip[i] = CRGB(0,0,0);
        break;
  
      case 7:
        if(i>=0 && i<2*LPS || i>=5*LPS)
          strip[i] = CRGB(0,0,0);
        break;

      // does nothing since all have already been filled
      case 8:
        break;
  
      case 9:
        if(i>=0 && i<LPS || i>=5*LPS && i<6*LPS)
          strip[i] = CRGB(0,0,0);
        break;
  
      default:
        break;
    }
  }
}

void displayNums() {
  if(tenMinVal <= 0 && oneMinVal > 0) {
    fill_solid(num1, NUM_LEDS, CRGB(0,0,0));
    showNum(num2, NUM_LEDS, oneMinVal);
    showNum(num3, NUM_LEDS, tenSecVal);
    showNum(num4, NUM_LEDS, oneSecVal);
  }

  else if(tenMinVal <= 0 && oneMinVal <= 0 && tenSecVal > 0) {
    fill_solid(num1, NUM_LEDS, CRGB(0,0,0));
    fill_solid(num2, NUM_LEDS, CRGB(0,0,0));
    showNum(num3, NUM_LEDS, tenSecVal);
    showNum(num4, NUM_LEDS, oneSecVal);
  }

  else if(tenMinVal <= 0 && tenSecVal <= 0 && oneMinVal <= 0 && oneSecVal > 0) {
    fill_solid(num1, NUM_LEDS, CRGB(0,0,0));
    fill_solid(num2, NUM_LEDS, CRGB(0,0,0));
    fill_solid(num3, NUM_LEDS, CRGB(0,0,0));
    showNum(num4, NUM_LEDS, oneSecVal);
  }

  else {
    showNum(num1, NUM_LEDS, tenMinVal);
    showNum(num2, NUM_LEDS, oneMinVal);
    showNum(num3, NUM_LEDS, tenSecVal);
    showNum(num4, NUM_LEDS, oneSecVal);
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
        showNum(num4, NUM_LEDS, oneSecVal);
        break;
      case 2:
        tenSecVal = data[1];
        showNum(num3, NUM_LEDS, tenSecVal);
        break;
      case 3:
        oneMinVal = data[1];
        showNum(num2, NUM_LEDS, oneMinVal);
        break;
      case 4:
        tenMinVal = data[1];
        showNum(num1, NUM_LEDS, tenMinVal);
        break;
      default:
        break;
    }
  }

  if(data[0] == 'H' && data[2] == 'M') {
    if(String(data[1]).length() == 1) {
      fill_solid(num1, NUM_LEDS, CRGB(0,0,0));
      oneMinVal = String(data[1])[0] - '0';

      showNum(num2, NUM_LEDS, oneMinVal);
    }
    else {
      tenMinVal = String(data[1])[0] - '0'; // process takes int value, converts to string, gets first char, and
                                            // converts to corresponding int value
      oneMinVal = String(data[1])[1] - '0'; // gets second char

      showNum(num1, NUM_LEDS, tenMinVal);
      showNum(num2, NUM_LEDS, oneMinVal);
    }
    //Serial.println(String(tenMinVal)[0] - '0' + " test");

    if(String(data[3]).length() == 1) {
      tenSecVal = 0;
      oneSecVal = String(data[3])[0] - '0';

      showNum(num3, NUM_LEDS, tenSecVal);
      showNum(num4, NUM_LEDS, oneSecVal);
    }
    else {
      tenSecVal = String(data[3])[0] - '0';
      oneSecVal = String(data[3])[1] - '0';

      showNum(num3, NUM_LEDS, tenSecVal);
      showNum(num4, NUM_LEDS, oneSecVal);
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
      showNum(num1, NUM_LEDS, 0);
      showNum(num2, NUM_LEDS, 0);
      showNum(num3, NUM_LEDS, 0);
      showNum(num4, NUM_LEDS, 0);

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

    red = MAX_COLOR_VAL;
    green = 0;
    blue = 0;

    showNum(num1, NUM_LEDS, tenMinVal);
    showNum(num2, NUM_LEDS, oneMinVal);
    showNum(num3, NUM_LEDS, tenSecVal);
    showNum(num4, NUM_LEDS, oneSecVal);

    return;
  }

  displayNums();
}

void showGo() {
/*
  for(int x = 0; x < 235; x++) {
   
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

    for(int i = 0; i < 35; i++) {
      if(i < 15 || (i >= 20 && i < 30) || i >= 33)
        num2.setPixelColor(i,num2.Color(x,x,0));

      if(i < 30)
        num3.setPixelColor(i,num3.Color(x,x,0));

    }

    num2.show();
    num3.show();
  }
  */
}


void showBlue() {
/*
  for(int x = 0; x < 235; x++) {
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

  for(int x = 235; x > 0; x--) {\
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
  */
}

void initLEDS() {
  fill_solid(num1, NUM_LEDS, CRGB(0,0,0));
  fill_solid(num2, NUM_LEDS, CRGB(0,0,0));
  fill_solid(num3, NUM_LEDS, CRGB(0,0,0));
  fill_solid(num4, NUM_LEDS, CRGB(0,0,0));
  
  for(int i = 0; i < NUM_LEDS; i++) {
    num1[i] = CRGB(100, 0, 100);
    delay(10);
    FastLED.show();
  }

  for(int i = 0; i < NUM_LEDS; i++) {
    num2[i] = CRGB(100, 0, 100);
    delay(10);
    FastLED.show();
  }

  for(int i = 0; i < NUM_LEDS; i++) {
    num3[i] = CRGB(100, 0, 100);
    delay(10);
    FastLED.show();
  }

  for(int i = 0; i < NUM_LEDS; i++) {
    num4[i] = CRGB(100, 0, 100);
    delay(10);
    FastLED.show();
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

  fill_solid(num1);
  fill_solid(num2);
  fill_solid(num3);
  fill_solid(num4);
  fill_solid(pins);

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

  FastLED.show();
}

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<NEOPIXEL, PIN_1>(num1, NUM_LEDS); 
  FastLED.addLeds<NEOPIXEL, PIN_2>(num2, NUM_LEDS); 
  FastLED.addLeds<NEOPIXEL, PIN_3>(num3, NUM_LEDS); 
  FastLED.addLeds<NEOPIXEL, PIN_4>(num4, NUM_LEDS); 
  FastLED.addLeds<NEOPIXEL, PIN_5>(pins, NUM_LEDS); 

  FastLED.show();

  initLEDS();
}

void loop() {
  int data[6] = {0,0,0,0,0,-1};
  int a = 0;
  int dataSize = 6;

  fill_solid(pins, 2, CRGB(MAX_COLOR_VAL, MAX_COLOR_VAL, MAX_COLOR_VAL));
  
  while(data[5] == -1){
    if(Serial.available()) {
      data[a] = Serial.read();
      a++;
    }

    handleData(data);
    doTimerTick();

  }

  FastLED.show();
}
