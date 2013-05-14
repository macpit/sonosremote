#!/usr/bin/python

# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp

import logging
logging.basicConfig(level=logging.INFO)

import thread
import random
from time import sleep

from Adafruit_I2C import Adafruit_I2C
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate()
lcd.begin(16, 2)
lcd.clear()

col = (('Red' , lcd.RED) , ('Yellow', lcd.YELLOW), ('Green' , lcd.GREEN),
       ('Teal', lcd.TEAL), ('Blue'  , lcd.BLUE)  , ('Violet', lcd.VIOLET))

from core import SoCo
from core import SonosDiscovery

sonosip = SonosDiscovery()
iplist=sonosip.get_speaker_ips()
#ip=iplist[random.randint(0, len(iplist))]
ip=iplist[0]


def keys(ip, iplist):
	sonos = SoCo(ip)
	vol = sonos.volume()
	bas = sonos.bass()

	print ip
	print iplist

	# Init display
	msg = 'Vol %s' % vol
	lcd.setCursor(0,0)
	lcd.message(msg)
	msg = 'Bass %s' % bas
	lcd.setCursor(8,0)
	lcd.message(msg)

	while True:
		if lcd.buttonPressed(lcd.UP):
			for i in iplist:
				sonos = SoCo(ip)
				sonos.volume(vol)
			vol += 1
			msg = 'Vol %s' % vol
			lcd.setCursor(0,0)
			lcd.message(msg)

		if lcd.buttonPressed(lcd.DOWN):
			for i in iplist:
				sonos = SoCo(ip)
				sonos.volume(vol)
			vol -= 1
			msg = 'Vol %s' % vol
			lcd.setCursor(0,0)
			lcd.message(msg)

		if lcd.buttonPressed(lcd.LEFT):
			for i in iplist:
				sonos = SoCo(ip)
				sonos.bass(bas)
			bas -= 1
			msg = 'Bass %s' % bas
			lcd.setCursor(8,0)
			lcd.message(msg)

		if lcd.buttonPressed(lcd.RIGHT):
			for i in iplist:
				sonos = SoCo(ip)
				sonos.bass(bas)
			bas += 1
			msg = 'Bass %s' % bas
			lcd.setCursor(8,0)
			lcd.message(msg)

	sleep(0.1)

def display (ip):
	sonos = SoCo(ip)
	lcd.setCursor(0,1)

	while True:
		try:
			tr=sonos.get_current_track_info()
			msg = msg=tr['artist']+" , "+tr['title']+" "
			mlen=len(msg)
		except:
			pass

		for i in range (0, len(msg)):
			lcd.setCursor(0,1)
			str = msg[i:(i+16)]
			lcd.message(str)
			# Wait for text is start scrolling
			if i == 0:
				sleep (2)
			sleep (0.4)

thread.start_new_thread(keys,(ip, iplist,))
thread.start_new_thread(display,(ip,))

while True:
	pass
	# title=sonos.get_current_track_info()
	# msg="Song: "+title['title']+" Artist: "+title['artist']

