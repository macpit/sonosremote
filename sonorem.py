#!/usr/bin/python

import logging

logging.basicConfig()

import thread
import time

from time import sleep

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate()
lcd.begin(16, 2)
lcd.clear()

col = (('Red', lcd.RED), ('Yellow', lcd.YELLOW), ('Green', lcd.GREEN),
       ('Teal', lcd.TEAL), ('Blue', lcd.BLUE), ('Violet', lcd.VIOLET))

from core import SoCo
from core import SonosDiscovery


def get_master_ip():
    _sonosip = SonosDiscovery()
    _getsp = _sonosip.get_speaker_ips()

    for i in _getsp:
        try:
            _tst = SoCo(i)
            #print _tst.get_speaker_info()['zone_name']
            if _tst.get_current_transport_info()['current_transport_state'] == 'PLAYING':
                #print "Playing --> ",i
                if _tst.get_current_track_info()['duration'] != 'NOT_IMPLEMENTED':
                    #print _tst.get_current_track_info()
                    _ip = i
        except:
            pass
    return _ip


def get_master_iplist():
    _iplist = []
    _sonosip = SonosDiscovery()
    _getsp = _sonosip.get_speaker_ips()

    for i in _getsp:
        try:
            _tst = SoCo(i)
            _tst.get_speaker_info()['zone_name']
            _iplist.append(i)
        except:
            pass
    return _iplist


def set_speaker_default():
    for i in get_master_iplist():
        try:
            print "Setup -->", i
            sonos = SoCo(i)
            sonos.mute(False)
            sonos.volume(35)
            sonos.bass(5)
            sonos.set_loudness(True)
        except:
            pass


def keys():
    """


    """
    _sonos = SoCo(get_master_ip())
    vol = _sonos.volume()
    bas = _sonos.bass()

    # Init display
    msg = 'Vol %s' % vol
    lcd.setCursor(0, 0)
    lcd.message(msg)
    msg = 'Bass %s' % bas
    lcd.setCursor(8, 0)
    lcd.message(msg)

    _iplist = get_master_iplist()

    def set_bas(bas):
        for i in _iplist:
            sonos = SoCo(i)
            sonos.bass(bas)
        msg = 'Bass %s' % bas
        lcd.setCursor(8, 0)
        lcd.message(msg)

    def set_vol(vol):
        for i in _iplist:
            sonos = SoCo(i)
            sonos.volume(vol)
        msg = 'Vol %s' % vol
        lcd.setCursor(0, 0)
        lcd.message(msg)

    while True:
        if lcd.buttonPressed(lcd.UP):
            vol += 1
            set_vol(vol)

        if lcd.buttonPressed(lcd.DOWN):
            vol -= 1
            set_vol(vol)

        if lcd.buttonPressed(lcd.LEFT):
            bas -= 1
            set_bas(bas)

        if lcd.buttonPressed(lcd.RIGHT):
            bas += 1
            set_bas(bas)

        if lcd.buttonPressed(lcd.SELECT):
            _time = time.time()
            while True:
                if lcd.buttonPressed(lcd.SELECT) == 0:
                    _start = time.time() - _time
                    if _start <= 1:
                        lcd.backlight(lcd.BLUE)
                        break
                    elif _start <= 2:
                        lcd.backlight(lcd.RED)
                        break
                    elif _start <= 3:
                        lcd.backlight(lcd.OFF)
                        break

    sleep(0.1)


def scroll_display():
    _sonos = SoCo(get_master_ip())
    lcd.setCursor(0, 1)

    while True:
        try:
            tr = _sonos.get_current_track_info()
            msg = msg = tr['artist'] + " , " + tr['title'] + " "
            mlen = len(msg)
        except:
            pass

        for i in range(0, len(msg)):
            lcd.setCursor(0, 1)
            str = msg[i:(i + 16)]
            lcd.message(str)
            # Wait for text is start scrolling
            if i == 0:
                sleep(2)
            sleep(0.4)


set_speaker_default()
thread.start_new_thread(keys, (), )
thread.start_new_thread(scroll_display, (), )

while True:
    pass

