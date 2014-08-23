#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Maps each tactile button and corresponding function here
# so other modules don't have to deal with GPIO.
import sys
import os
import RPi.GPIO as GPIO
from Odyssey import Odyssey
from daemon import daemon
from daemon.pidlockfile import PIDLockFile

def run():

    os.putenv('SDL_VIDEODRIVER', 'fbcon'                 )
    os.putenv('SDL_FBDEV'      , '/dev/fb1'              )
    os.putenv('SDL_MOUSEDRV'   , 'TSLIB'                 )
    os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

    os.putenv('GPSD_PORT', '2947')

    odyssey = Odyssey()
    odyssey.cameraController.show_preview()

    def switch_preview(channel):
        odyssey.switch_preview()

    def switch_record(channel):
        odyssey.switch_record()

    # GPIO settings
    GPIO.setmode(GPIO.BCM)

    # On/Off preview display
    # leftmost tactile switch
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.RISING, callback=switch_preview, bouncetime=1000)

    # Start/Stop video recording
    # second from left
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(22, GPIO.RISING, callback=switch_record, bouncetime=1000)

    try:
        while True:
            pass

    except KeyboardInterrupt:
        print 'Abort...'

    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]

    finally:
        odyssey.stop()
        GPIO.cleanup()
        print 'Done'

with daemon.DaemonContext(pidfile=PIDLockFile('/var/run/odyssey.pid')):
    run()