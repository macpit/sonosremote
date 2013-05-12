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

lcd.setCursor(0,1)

while True:

	tr=sonos.get_current_track_info()
	lcd.setCursor(0,0)
	lcd.message(tr['artist'])
	msg = tr['title']
	lcd.setCursor(0,1)
	lcd.message(msg)
	sleep (3)

