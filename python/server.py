from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import socket
import sys
from time import sleep
import time
import types
import os
from cgi import parse_header, parse_multipart
from sys import version as python_version

if python_version.startswith('3'):
    from urllib.parse import parse_qs
    from http.server import BaseHTTPRequestHandler
else:
    from urlparse import parse_qs
    from BaseHTTPServer import BaseHTTPRequestHandler

import serial
import require
import thread

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


board = require("./board.py")

b = board.Board(0,0)

b.homeOff()
b.awayOff()

b.showNum(0,0)
b.showNum(0,1)

# BUTTONS
########################################################################################################################################
def homeAddHandler():
	print "up home"
	b.changeHome(1, "add")

def homeMinusHandler():
	print "down home"
	b.changeHome(1, "minus")

def awayAddHandler():
	print "up away"
	b.changeAway(1, "add")

def awayMinusHandler():
	print "down away"
	b.changeAway(1, "minus")

def displayHandler():
	b.serialWriteColor(chr(b.redVal),chr(b.greenVal),chr(b.blueVal))

#TIMER SETTING HANDLER FUNCTIONS
def setTime(num1, num2, num3, num4):
    if b.clockMode == "timer" and not b.timerRunning:
        print "Time to set: ", num1, num2, num3, num4

        if num3 > 5:
            num3 = 5

	b.tenMinVal = num1
	b.tenSecVal = num2
	b.oneMinVal = num3
	b.oneSecVal = num4

        b.changeTime(b.tenMinVal, 4)
        b.changeTime(b.tenSecVal, 3)
        b.changeTime(b.oneMinVal, 2)
        b.changeTime(b.oneSecVal, 1)

'''
def timeAddOnesSecHandler():
	print "Time Add Ones Sec: "
	if b.clockMode == "timer" and not b.timerRunning:
		b.oneSecVal += 1
		if(b.oneSecVal == 10):
			b.oneSecVal = 0
		b.changeTime(b.oneSecVal, 1)

def timeMinusOnesSecHandler():
	print "Time Minus Ones Sec: "
	if b.clockMode == "timer" and not b.timerRunning:
		b.oneSecVal -= 1
		if b.oneSecVal == -1:
			b.oneSecVal = 9
		b.changeTime(b.oneSecVal, 1)

def timeAddTensSecHandler():
	print "Time Add Tens Sec: "
	if b.clockMode == "timer" and not b.timerRunning:
		b.tenSecVal += 1
		if(b.tenSecVal == 6):
			b.tenSecVal = 0
		b.changeTime(b.tenSecVal, 2)

def timeMinusTensSecHandler():
	print "Time Minus Tens Sec: ", state
	if b.clockMode == "timer" and not b.timerRunning:
		b.tenSecVal -= 1
		if(b.tenSecVal == -1):
			b.tenSecVal = 5
		b.changeTime(b.tenSecVal, 2)

def timeAddOnesMinHandler():
	print "Time Add Ones Min: "
	if b.clockMode == "timer" and not b.timerRunning:
		b.oneMinVal += 1
		if b.oneMinVal == 10:
			b.oneMinVal = 0
		b.changeTime(b.oneMinVal, 3)

def timeMinusOnesMinHandler():
	print "Time Minus Ones Min: "
	if b.clockMode == "timer" and not b.timerRunning:
		b.oneMinVal -= 1
		if(b.oneMinVal == -1):
			b.oneMinVal = 9
		b.changeTime(b.oneMinVal, 3)

def timeAddTensMinHandler():
	print "Time Add Tens Min: "
	if b.clockMode == "timer" and not b.timerRunning:
		b.tenMinVal += 1
		if(b.tenMinVal == 10):
			b.tenMinVal = 0
		b.changeTime(b.tenMinVal, 4)

def timeMinusTensMinHandler():
		print "Time Minus Tens Min: "
		if b.clockMode == "timer" and not b.timerRunning:
			b.tenMinVal -= 1
			if(b.tenMinVal == -1):
				b.tenMinVal = 9
			b.changeTime(b.tenMinVal, 4) '''

#BASIC TIMER FUNCTIONS######################################################
def setTimer0():
	if b.clockMode == "timer":
		b.serialWrite('T',chr(0)) # 0 indicates to set to 0
		b.timerRunning = False
		b.oneSecVal = 0
		b.tenSecVal = 0
		b.oneMinVal = 0
		b.tenMinVal = 0

def startStopTimer():
	if not(b.timerRunning) and b.clockMode == "timer":
		b.serialWrite('T',chr(1)) # 1 indicates to start the timer
		b.timerRunning = True
	elif b.timerRunning and b.clockMode == "timer":
		b.serialWrite('T',chr(9)) # 9 indicates to stop
		b.timerRunning = False

def setClockMode():
	b.timerRunning = False
	b.clockMode = "clock"
	b.serialWrite('C',chr(0))

	h = time.localtime()[3]
	if h > 12:
		h -= 12
		b.serialWrite('H',chr(h),'M',chr(time.localtime()[4]),'S',chr(0))

def setTimerMode():
	b.clockMode = "timer"
	b.serialWrite('C',chr(1));


#FADERS
#################################################################################
def redHandler():
    b.redVal=int(args[0])

def greenHandler():
    b.greenVal=int(args[0])

def blueHandler():
    b.blueVal=int(args[0])


#Fancy display stuff################################################################################
def fancyFlash():
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

# list holding all clients
clients = []

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		if clients.count(self.client_address[0]) == 0:
			clients.append(self.client_address[0])

		self.path = "/home/pi/Desktop/scoreboard-api/build" + self.path

		if self.path=="/home/pi/Desktop/scoreboard-api/build/":
			self.path="/home/pi/Desktop/scoreboard-api/build/index.html"

		if self.path == "/home/pi/Desktop/scoreboard-api/build/favicon.ico":
			return

		if self.path.endswith(".html"):
			mimetype = 'text/html'
		if self.path.endswith(".js"):
			mimetype = 'application/javascript'

		f = open(self.path)
		self.send_response(200)
		self.send_header('Content-type',mimetype)
		self.end_headers()
		# Send the html message
		self.wfile.write(f.read())
		f.close()

def updateClock():
	print "started clock tick..."

	while True:
		h = time.localtime()[3]
		m = time.localtime()[4]

		if h > 12:
			h -= 12

		time.sleep(1) # thread updates every second
		print "tick"

		if b.clockMode == "clock":
			b.serialWrite('H',chr(h),'M',chr(m),'S',chr(0))

def handleMessage(message):
	if message == "clockMode/true":
		setClockMode()
	elif message == "clockMode/false":
		setTimerMode()
	elif message == "home/+1":
		homeAddHandler()
	elif message == "home/-1":
		homeMinusHandler()
	elif message == "away/+1":
		awayAddHandler()
	elif message == "away/-1":
		awayMinusHandler()
	elif message == "setTimer0":
		setTimer0()
	elif message == "timer":
		startStopTimer()
	elif message.find("setTime/") >= 0:
		time = message[8:]
		print time
		setTime(int(time[0]), int(time[1]), int(time[2]), int(time[3]))

class WSHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		return True

	def open(self):
		print 'New connection was opened'

	def on_message(self, message):
		print 'Incoming message:', message
		handleMessage(message)

	def on_close(self):
		print 'Connection was closed...'

def runWebsocket():
        print 'started WebSocket listener...'
	application = tornado.web.Application([
  		(r'/ws', WSHandler),
	])

	socket_server = tornado.httpserver.HTTPServer(application)
  	socket_server.listen(8888)
  	tornado.ioloop.IOLoop.instance().start()


try:
	#Create a web server and define the handler to manage the
	#incoming request

	server = HTTPServer(("192.168.1.60", 8000), myHandler)
	print 'started httpserver on port ' , 8000

	thread.start_new_thread(updateClock, ())
	thread.start_new_thread(runWebsocket, ())
	server.serve_forever()


except KeyboardInterrupt:
	print '\nshutting down the web server'
	server.socket.close()
