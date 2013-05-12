import logging
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

while True:

	tr=sonos.get_current_track_info()
	if tr['artist'] > '':
		msg=tr['artist']+" , "
	else:
		msg="None"+","
	msg += tr['title']
	msg += " "
	mlen=len(msg)

	for i in range (0, len(msg)):
		lcd.setCursor(0,1)
		str = msg[i:(i+15)]
		lcd.message(str)
		if i == 0:
			sleep (2)
		sleep (0.4)
