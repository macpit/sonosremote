import logging
import time

logging.basicConfig(level=logging.DEBUG)

from time import sleep

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate()

from core import SoCo
from core import SonosDiscovery

sonos = SoCo('10.0.1.205')


lcd.begin(16, 2)

lcd.clear()

# MAX 40 / Scroll MAX 24 
msg="Sonos controller by Marc"

mlen=0
lcd.setCursor(0,0)
lcd.message("Marc Sonos")
lcd.setCursor(0,1)

t=0

pressed_time = None
print lcd.buttonPressed(lcd.UP)

while True:

	if lcd.buttonPressed(lcd.UP):
		st = time.time()
		print "UP Start"
		while True:
			#sleep (0.5)
			if lcd.buttonPressed(lcd.UP) == 0:
				zeit = time.time() - st
				print zeit
				if zeit <= 1:
					print "Funktion 1sek"
					break
				elif zeit <= 2:
					print "Funktion 2sek"
					break
				elif zeit <= 3:
					print "Funktion 3sek"
					break


	if lcd.buttonPressed(lcd.SELECT):
		if pressed_time is None:
			# just pressed
			pressed_time = time.time()
		elif time.time() - pressed_time >= 3.0:
			print "3 sec"
			break # it's been pressed for 3 seconds
		elif time.time() - pressed_time >= 1.0:
			print "1 sec"
			break
	else:
		# not pressed
		pressed_time = None
