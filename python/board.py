import RPi.GPIO as GPIO
import serial
import time

class Board:

    HOME_BOTTOM_LEFT = 2
    HOME_TOP_LEFT = 3
    HOME_TOP = 4
    HOME_TOP_RIGHT = 14
    HOME_BOTTOM_RIGHT = 15
    HOME_BOTTOM = 18
    HOME_MIDDLE = 17
    HOME_ONE = 27

    AWAY_BOTTOM_LEFT = 22
    AWAY_TOP_LEFT = 23
    AWAY_TOP = 24
    AWAY_TOP_RIGHT = 10
    AWAY_BOTTOM_RIGHT = 9
    AWAY_BOTTOM = 11
    AWAY_MIDDLE = 25
    AWAY_ONE = 8

    # inits all gpio pins to OUT
    def __init__(self, hScore, aScore):
        self.homeScore = hScore
        self.awayScore = aScore

        self.redVal = 235
        self.greenVal = 235
        self.blueVal = 235

        self.oneSecVal = 0
        self.tenSecVal = 0
        self.oneMinVal = 0
        self.tenMinVal = 0

        self.clockMode = "clock"
        self.timerRunning = False
        
        self.serial = serial.Serial('/dev/ttyACM0', 115200)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.HOME_BOTTOM_LEFT,GPIO.OUT)
        GPIO.setup(self.HOME_TOP_LEFT,GPIO.OUT)
        GPIO.setup(self.HOME_TOP,GPIO.OUT)
        GPIO.setup(self.HOME_TOP_RIGHT,GPIO.OUT)
        GPIO.setup(self.HOME_BOTTOM_RIGHT,GPIO.OUT)
        GPIO.setup(self.HOME_BOTTOM,GPIO.OUT)
        GPIO.setup(self.HOME_MIDDLE,GPIO.OUT)
        GPIO.setup(self.HOME_ONE,GPIO.OUT)

        GPIO.setup(self.AWAY_BOTTOM_LEFT,GPIO.OUT)
        GPIO.setup(self.AWAY_TOP_LEFT,GPIO.OUT)
        GPIO.setup(self.AWAY_TOP,GPIO.OUT)
        GPIO.setup(self.AWAY_TOP_RIGHT,GPIO.OUT)
        GPIO.setup(self.AWAY_BOTTOM_RIGHT,GPIO.OUT)
        GPIO.setup(self.AWAY_BOTTOM,GPIO.OUT)
        GPIO.setup(self.AWAY_MIDDLE,GPIO.OUT)
        GPIO.setup(self.AWAY_ONE,GPIO.OUT)

    # turns off all pins
    def homeOff(self):
        GPIO.output(self.HOME_BOTTOM_LEFT,GPIO.LOW)
        GPIO.output(self.HOME_TOP_LEFT,GPIO.LOW)
        GPIO.output(self.HOME_TOP,GPIO.LOW)
        GPIO.output(self.HOME_TOP_RIGHT,GPIO.LOW)
        GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.LOW)
        GPIO.output(self.HOME_BOTTOM,GPIO.LOW)
        GPIO.output(self.HOME_MIDDLE,GPIO.LOW)
        GPIO.output(self.HOME_ONE,GPIO.LOW)

    def awayOff(self):
        GPIO.output(self.AWAY_BOTTOM_LEFT,GPIO.LOW)
        GPIO.output(self.AWAY_TOP_LEFT,GPIO.LOW)
        GPIO.output(self.AWAY_TOP,GPIO.LOW)
        GPIO.output(self.AWAY_TOP_RIGHT,GPIO.LOW)
        GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.LOW)
        GPIO.output(self.AWAY_BOTTOM,GPIO.LOW)
        GPIO.output(self.AWAY_MIDDLE,GPIO.LOW)
        GPIO.output(self.AWAY_ONE,GPIO.LOW)

    # turns on all pins
    def allOn(self):
        GPIO.output(self.HOME_BOTTOM_LEFT,GPIO.HIGH)
        GPIO.output(self.HOME_TOP_LEFT,GPIO.HIGH)
        GPIO.output(self.HOME_TOP,GPIO.HIGH)
        GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
        GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
        GPIO.output(self.HOME_BOTTOM,GPIO.HIGH)
        GPIO.output(self.HOME_MIDDLE,GPIO.HIGH)
        GPIO.output(self.HOME_ONE,GPIO.HIGH)

        GPIO.output(self.AWAY_BOTTOM_LEFT,GPIO.HIGH)
        GPIO.output(self.AWAY_TOP_LEFT,GPIO.HIGH)
        GPIO.output(self.AWAY_TOP,GPIO.HIGH)
        GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
        GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
        GPIO.output(self.AWAY_BOTTOM,GPIO.HIGH)
        GPIO.output(self.AWAY_MIDDLE,GPIO.HIGH)
        GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def changeHome(self, state, direction): 
        if state == 1 and direction == "add":
            self.homeScore += 1
        if state == 1 and direction == "minus":
            self.homeScore -= 1

        if self.homeScore == -1:
            self.homeScore = 19
        if self.homeScore == 20:
            self.homeScore = 0

        self.showNum(self.homeScore, 0)

    def changeAway(self, state, direction): 
        if state == 1 and direction == "add":
                self.awayScore += 1
        if state == 1 and direction == "minus":
                self.awayScore -= 1

        if self.awayScore == -1:
                self.awayScore = 19
        if self.awayScore == 20:
                self.awayScore = 0

        self.showNum(self.awayScore, 1)

    def serialWrite(self, val1, val2, val3=chr(0), val4=chr(0), val5=chr(0), val6=chr(0)):
        self.serial.write(val1)
	time.sleep(0.1)
        self.serial.write(val2)
	time.sleep(0.1)
        self.serial.write(val3)
	time.sleep(0.1)
        self.serial.write(val4)
	time.sleep(0.1)
        self.serial.write(val5)
	time.sleep(0.1) # these delays are here to not overflow the arduino buffer
        self.serial.write(val6)
        
    #writes 6-value color data to arduino
    def serialWriteColor(self, val1, val2, val3):
        self.serialWrite('R',val1,'G',val2,'B',val3)
    
    def show0(self, team, place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def show1(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def show2(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_MIDDLE,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_MIDDLE,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def show3(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_MIDDLE,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_MIDDLE,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def show4(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_MIDDLE,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_MIDDLE,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def show5(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_MIDDLE,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_MIDDLE,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def show6(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_MIDDLE,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_LEFT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_MIDDLE,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_LEFT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)
            
    def show7(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
            
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def show8(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_BOTTOM,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_MIDDLE,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_BOTTOM,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_MIDDLE,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    def show9(self,team,place):
        if(team == 0):
            self.homeOff()
            GPIO.output(self.HOME_MIDDLE,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.HOME_TOP,GPIO.HIGH)
            GPIO.output(self.HOME_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.HOME_BOTTOM_RIGHT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.HOME_ONE,GPIO.HIGH)
        elif(team == 1):
            self.awayOff()
            GPIO.output(self.AWAY_MIDDLE,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_LEFT,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP,GPIO.HIGH)
            GPIO.output(self.AWAY_TOP_RIGHT,GPIO.HIGH)
            GPIO.output(self.AWAY_BOTTOM_RIGHT,GPIO.HIGH)
            if place == 1:
                GPIO.output(self.AWAY_ONE,GPIO.HIGH)

    #num is number to display
    #place in context of score is which team, place in context of time is
    #either secs, tenssecs, mins, or tensmins
    def showNum(self,num,place,section="score"):
        if(section == "score"):
            if(num == 0):
                self.show0(place,0)
            if(num == 1):
                self.show1(place,0)
            if(num == 2):
                self.show2(place,0)
            if(num == 3):
                self.show3(place,0)
            if(num == 4):
                self.show4(place,0)
            if(num == 5):
                self.show5(place,0)
            if(num == 6):
                self.show6(place,0)
            if(num == 7):
                self.show7(place,0)
            if(num == 8):
                self.show8(place,0)
            if(num == 9):
                self.show9(place,0)
            if(num == 10):
                self.show0(place,1)
            if(num == 11):
                self.show1(place,1)
            if(num == 12):
                self.show2(place,1)
            if(num == 13):
                self.show3(place,1)
            if(num == 14):
                self.show4(place,1)
            if(num == 15):
                self.show5(place,1)
            if(num == 16):
                self.show6(place,1)
            if(num == 17):
                self.show7(place,1)
            if(num == 18):
                self.show8(place,1)
            if(num == 19):
                self.show9(place,1)

        #serial write here writes 'N' indicating subsequent value is num
        # to go on board, and 'P' indicating which place (second/min) to go to
        elif section == "time":
            self.serialWrite('N', chr(num),'P', chr(place))

    def changeTime(self, value, place):
        self.showNum(value,place,"time")

    def on(self,pin):
        GPIO.output(pin,GPIO.HIGH)

    def off(self,pin):
        GPIO.output(pin,GPIO.LOW)
