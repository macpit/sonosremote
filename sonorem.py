#!/usr/bin/python

# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp

import logging
logging.basicConfig(level=logging.INFO)

import thread

from Adafruit_I2C import Adafruit_I2C
from time import sleep

from core import SoCo
from core import SonosDiscovery
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate()
lcd.begin(16, 2)

col = (('Red' , lcd.RED) , ('Yellow', lcd.YELLOW), ('Green' , lcd.GREEN),
       ('Teal', lcd.TEAL), ('Blue'  , lcd.BLUE)  , ('Violet', lcd.VIOLET))

lcd.clear()
lcd.message("SonoS Controll System.")

lcd.clear()

def keys():

	sonos = SoCo('10.0.1.205')
	sonosp = SonosDiscovery()
	sonos_sp = sonosp.get_speaker_ips()
	vol = sonos.volume()
	bas = sonos.bass()


	while True:

		if lcd.buttonPressed(lcd.UP):
			for ip in sonos_sp:
				sonos = SoCo(ip)
				sonos.volume(vol)
			vol += 1
			msg = 'Vol %s' % vol
			lcd.setCursor(0,0)
			lcd.message(msg)

		if lcd.buttonPressed(lcd.DOWN):
			for ip in sonos_sp:
				sonos = SoCo(ip) 
				sonos.volume(vol)
			vol -= 1
			msg = 'Vol %s' % vol
			lcd.setCursor(0,0)
			lcd.message(msg)

		if lcd.buttonPressed(lcd.LEFT):
			for ip in sonos_sp:
				sonos = SoCo(ip)
				sonos.bass(bas)
			bas -= 1
			msg = 'Bass %s' % bas
			lcd.setCursor(8,0)
			lcd.message(msg)

		if lcd.buttonPressed(lcd.RIGHT):
			for ip in sonos_sp:
				sonos = SoCo(ip)
				sonos.bass(bas)
			bas += 1
			msg = 'Bass %s' % bas
			lcd.setCursor(8,0)
			lcd.message(msg)

	sleep(0.1)

def display ():

	sonos = SoCo('10.0.1.205')
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
			if i == 0:
				sleep (2)
			sleep (0.4)

thread.start_new_thread(keys,())
thread.start_new_thread(display,())

while True:
	pass
	# title=sonos.get_current_track_info()
	# msg="Song: "+title['title']+" Artist: "+title['artist']

