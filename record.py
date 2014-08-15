#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import RPi.GPIO as GPIO
from Odyssey import Odyssey

# basic settings
os.putenv('SDL_VIDEODRIVER', 'fbcon'                 )
os.putenv('SDL_FBDEV'      , '/dev/fb1'              )
os.putenv('SDL_MOUSEDRV'   , 'TSLIB'                 )
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

odyssey = Odyssey()

def switch_preview(channel):
    odyssey.switch_preview()

# GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.RISING, callback=switch_preview, bouncetime=1000)

try:
    while True:
        pass
        # TODO do something with camera

except KeyboardInterrupt:
    print 'Abort...'

except:
    print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]

finally:
    odyssey.stop()
    GPIO.cleanup()
    print 'Done'
