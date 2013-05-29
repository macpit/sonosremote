#!/usr/bin/python

import logging
logging.basicConfig()

import logging

logging.basicConfig(level=logging.INFO)

from core import SoCo
from core import SonosDiscovery

sonosip = SonosDiscovery()
_getsp = sonosip.get_speaker_ips()
iplist = []

for i in _getsp:
	try:
		_tst = SoCo(i)
		print _tst.get_speaker_info()['zone_name']
		if _tst.get_current_transport_info()['current_transport_state'] == 'PLAYING':
			ip=i
		iplist.append(i)
		print "IP ",i
	except:
		pass

print "Get sp list done ",iplist

try:
	print "Playing Master ",ip
	print SoCo(ip).get_current_track_info()
except:
	pass
