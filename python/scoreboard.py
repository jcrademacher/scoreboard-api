import OSC
from board import Board
from OSC import OSCServer,OSCClient, OSCMessage
import sys
from time import sleep
import time
import types
import os
import serial

b = Board(0,0)

b.homeOff()
b.awayOff()

b.showNum(0,0)
b.showNum(0,1)

serverAddr = ("192.168.86.41",8000)
#This has to be the IP of the RaspberryPi on the network
server = OSCServer(serverAddr)

def handle_timeout(self):
    '''print ("I'm IDLE")'''

#This here is just to do something while the script recieves no information....
server.handle_timeout = types.MethodType(handle_timeout, server)

# BUTTONS
########################################################################################################################################
def homeAddHandler(path, tags, args, source):
    state=int(args[0])
    b.changeHome(state, "add")

def homeMinusHandler(path, tags, args, source):
    state=int(args[0])
    b.changeHome(state, "minus")

def awayAddHandler(path, tags, args, source):
    state=int(args[0])
    b.changeAway(state, "add")

def awayMinusHandler(path, tags, args, source):
    state=int(args[0])
    b.changeAway(state, "minus")

def displayHandler(path,tags,args,source):
    state=int(args[0])
    if(state == 1):
        b.serialWriteColor(chr(b.redVal),chr(b.greenVal),chr(b.blueVal))

#TIMER SETTING HANDLER FUNCTIONS
def timeAddOnesSecHandler(path,tags,args,source):
    state=int(args[0])
    print "Time Add Ones Sec: ", state
    if(state == 1 and b.clockMode == "timer" and not b.timerRunning):
        b.oneSecVal += 1
        if(b.oneSecVal == 10):
            b.oneSecVal = 0
        b.changeTime(b.oneSecVal, 1)

def timeMinusOnesSecHandler(path,tags,args,source):
    state=int(args[0])
    print "Time Minus Ones Sec: ", state
    if(state == 1 and b.clockMode == "timer" and not b.timerRunning):
        b.oneSecVal -= 1
        if(b.oneSecVal == -1):
            b.oneSecVal = 9
        b.changeTime(b.oneSecVal, 1)

def timeAddTensSecHandler(path,tags,args,source):
    state=int(args[0])
    print "Time Add Tens Sec: ", state
    if(state == 1 and b.clockMode == "timer" and not b.timerRunning):
        b.tenSecVal += 1
        if(b.tenSecVal == 6):
            b.tenSecVal = 0
        b.changeTime(b.tenSecVal, 2)

def timeMinusTensSecHandler(path,tags,args,source):
    state=int(args[0])
    print "Time Minus Tens Sec: ", state
    if(state == 1 and b.clockMode == "timer" and not b.timerRunning):
        b.tenSecVal -= 1
        if(b.tenSecVal == -1):
            b.tenSecVal = 5
        b.changeTime(b.tenSecVal, 2)

def timeAddOnesMinHandler(path,tags,args,source):
    state=int(args[0])
    print "Time Add Ones Min: ", state
    if(state == 1 and b.clockMode == "timer" and not b.timerRunning):
        b.oneMinVal += 1
        if(b.oneMinVal == 10):
            b.oneMinVal = 0
        b.changeTime(b.oneMinVal, 3)

def timeMinusOnesMinHandler(path,tags,args,source):
    state=int(args[0])
    print "Time Minus Ones Min: ", state
    if(state == 1 and b.clockMode == "timer" and not b.timerRunning):
        b.oneMinVal -= 1
        if(b.oneMinVal == -1):
            b.oneMinVal = 9
        b.changeTime(b.oneMinVal, 3)

def timeAddTensMinHandler(path,tags,args,source):
    state=int(args[0])
    print "Time Add Tens Min: ", state
    if(state == 1 and b.clockMode == "timer" and not b.timerRunning):
        b.tenMinVal += 1
        if(b.tenMinVal == 10):
            b.tenMinVal = 0
        b.changeTime(b.tenMinVal, 4)

def timeMinusTensMinHandler(path,tags,args,source):
    state=int(args[0])
    print "Time Minus Tens Min: ", state
    if(state == 1 and b.clockMode == "timer" and not b.timerRunning):
        b.tenMinVal -= 1
        if(b.tenMinVal == -1):
            b.tenMinVal = 9
        b.changeTime(b.tenMinVal, 4)

#BASIC TIMER FUNCTIONS######################################################
def setTimer0(path,tags,args,source):
    state=int(args[0])
    if state == 1 and b.clockMode == "timer":
        b.serialWrite('T',chr(0)) # 0 indicates to set to 0
        b.timerRunning = False
        b.oneSecVal = 0
        b.tenSecVal = 0
        b.oneMinVal = 0
        b.tenMinVal = 0

def startStopTimer(path,tags,args,source):
    state=int(args[0])
    if state == 1 and not(b.timerRunning) and b.clockMode == "timer":
        b.serialWrite('T',chr(1)) # 1 indicates to start the timer
        b.timerRunning = True
    elif state == 1 and b.timerRunning and b.clockMode == "timer":
        b.serialWrite('T',chr(9)) # 9 indicates to stop
        b.timerRunning = False

def setClockMode(path,tags,args,source):
    state=int(args[0])
    if state == 1:
        b.timerRunning = False
        b.clockMode = "clock"
        b.serialWrite('C',chr(0))
	h = time.localtime()[3]
	if h > 12:
	    h -= 12
        b.serialWrite('H',chr(h),'M',chr(time.localtime()[4]),'S',chr(0))

def setTimerMode(path,tags,args,source):
    state=int(args[0])
    if state == 1:
        b.clockMode = "timer"
        b.serialWrite('C',chr(1));

#FADERS
#################################################################################
def redHandler(path, tags, args, source):
    if(args[0] > 200): #preserving the white color for LEDS (power issue)
        b.redVal=200
    else:
        b.redVal=int(args[0])

def greenHandler(path, tags, args, source):
    if(args[0] > 200):  #preserving the white color for LEDS (power issue)
        b.greenVal=200
    else:
        b.greenVal=int(args[0])

def blueHandler(path, tags, args, source):
    b.blueVal=int(args[0])

#Fancy display stuff################################################################################
def fancyFlash(path, tags, args, source):
    state=int(args[0])

    if state == 1:
        b.homeOff()
        b.awayOff()
        for i in range(0,5):
            b.on(b.HOME_BOTTOM_LEFT)
            b.on(b.AWAY_BOTTOM_LEFT)
            time.sleep(0.1)
            b.off(b.HOME_BOTTOM_LEFT)
            b.off(b.AWAY_BOTTOM_LEFT)

            b.on(b.HOME_TOP_LEFT)
            b.on(b.AWAY_TOP_LEFT)
            time.sleep(0.1)
            b.off(b.HOME_TOP_LEFT)
            b.off(b.AWAY_TOP_LEFT)

            b.on(b.HOME_TOP)
            b.on(b.AWAY_TOP)
            time.sleep(0.1)
            b.off(b.HOME_TOP)
            b.off(b.AWAY_TOP)

            b.on(b.HOME_TOP_RIGHT)
            b.on(b.AWAY_TOP_RIGHT)
            time.sleep(0.1)
            b.off(b.HOME_TOP_RIGHT)
            b.off(b.AWAY_TOP_RIGHT)

            b.on(b.HOME_BOTTOM_RIGHT)
            b.on(b.AWAY_BOTTOM_RIGHT)
            time.sleep(0.1)
            b.off(b.HOME_BOTTOM_RIGHT)
            b.off(b.AWAY_BOTTOM_RIGHT)

            b.on(b.HOME_BOTTOM)
            b.on(b.AWAY_BOTTOM)
            time.sleep(0.1)
            b.off(b.HOME_BOTTOM)
            b.off(b.AWAY_BOTTOM)

        #resets score
        b.showNum(b.homeScore, 0)
        b.showNum(b.awayScore, 1)


#These are all the add-ons that you can name in the TouchOSC layout designer (you can set the values and directories)
server.addMsgHandler("/homeAdd", homeAddHandler)
server.addMsgHandler("/homeMinus", homeMinusHandler)
server.addMsgHandler("/awayAdd", awayAddHandler)
server.addMsgHandler("/awayMinus", awayMinusHandler)

server.addMsgHandler("/redval", redHandler)
server.addMsgHandler("/greenval", greenHandler)
server.addMsgHandler("/blueval", blueHandler)
server.addMsgHandler("/displayColor", displayHandler)

server.addMsgHandler("/plusonessec", timeAddOnesSecHandler)
server.addMsgHandler("/minusonessec", timeMinusOnesSecHandler)
server.addMsgHandler("/plustenssec", timeAddTensSecHandler)
server.addMsgHandler("/minustenssec", timeMinusTensSecHandler)
server.addMsgHandler("/plusonesmin", timeAddOnesMinHandler)
server.addMsgHandler("/minusonesmin", timeMinusOnesMinHandler)
server.addMsgHandler("/plustensmin", timeAddTensMinHandler)
server.addMsgHandler("/minustensmin", timeMinusTensMinHandler)

server.addMsgHandler("/set0", setTimer0)
server.addMsgHandler("/startstop", startStopTimer)

server.addMsgHandler("/clock", setClockMode)
server.addMsgHandler("/timer", setTimerMode)

server.addMsgHandler("/displays/1/1", fancyFlash)

#The way that the MSG Handlers work is by taking the values from set accessory, then it puts them into a function
#The function then takes the values and separates them according to their class (args, source, path, and tags)

x = 0
prevH = 0
prevM = 0

while True:
    server.handle_request()

    h = time.localtime()[3]
    m = time.localtime()[4]

    if h > 12:
	h -= 12

    x += 1
    if x == 0 or x % 5 == 0 and b.clockMode == "clock":
        b.serialWrite('H',chr(h),'M',chr(m),'S',chr(0))
        prevH = h
        prevM = m

server.close()
#This will kill the server when the program ends
